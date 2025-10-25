"""
Complete audio_video_processor.py
Place this file in: utils/audio_video_processor.py
"""

import streamlit as st
import numpy as np
import speech_recognition as sr
import tempfile
import os
from datetime import datetime
import time
import cv2
import wave
import sounddevice as sd
import soundfile as sf

class RealtimeAudioVideoProcessor:
    """Real-time audio/video processor with live transcription"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        
    def start_realtime_recording(self, duration=30):
        """
        Real-time speech recognition with live transcription
        Returns: (final_transcription, audio_path, video_path)
        """
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_temp:
                audio_path = audio_temp.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='.avi') as video_temp:
                video_path = video_temp.name

            # Initialize camera
            cap = cv2.VideoCapture(0)
            camera_available = cap.isOpened()
            
            if not camera_available:
                st.warning("📷 Camera not available. Using audio-only mode.")
            
            # Initialize video writer if camera is available
            out = None
            if camera_available:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 20)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

            # Audio recording parameters
            SAMPLE_RATE = 16000
            CHUNK_DURATION = 3  # seconds per transcription chunk
            CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)
            
            # Storage
            all_audio_data = []
            transcription_parts = []
            current_audio_chunk = []
            
            start_time = time.time()
            last_transcription_time = start_time
            
            st.info(f"🎤 **Live Recording Started** - Speak clearly! ({duration}s)")
            
            # Create placeholders
            progress_bar = st.progress(0)
            status_text = st.empty()
            video_placeholder = st.empty()
            transcription_display = st.empty()
            
            def audio_callback(indata, frames, time, status):
                """Callback for real-time audio input"""
                if status:
                    st.warning(f"Audio status: {status}")
                current_audio_chunk.extend(indata.copy())
                all_audio_data.extend(indata.copy())
            
            # Start audio stream
            stream = sd.InputStream(
                callback=audio_callback,
                channels=1,
                samplerate=SAMPLE_RATE,
                blocksize=1024
            )
            
            with stream:
                while (time.time() - start_time) < duration:
                    elapsed = time.time() - start_time
                    progress = elapsed / duration
                    progress_bar.progress(min(progress, 1.0))
                    remaining = duration - elapsed
                    
                    # Display status
                    current_words = len(' '.join(transcription_parts).split())
                    status_text.text(f"⏺️ Recording... {remaining:.1f}s remaining | Words: {current_words}")
                    
                    # Capture video if camera available
                    if camera_available:
                        ret, frame = cap.read()
                        if ret:
                            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            video_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
                            out.write(frame)
                    
                    # Real-time transcription
                    current_time = time.time()
                    if (current_time - last_transcription_time) >= CHUNK_DURATION and len(current_audio_chunk) > 0:
                        try:
                            # Convert to audio data for speech recognition
                            audio_array = np.array(current_audio_chunk, dtype=np.float32)
                            audio_data = sr.AudioData(
                                (audio_array * 32767).astype(np.int16).tobytes(),
                                SAMPLE_RATE,
                                2  # sample width in bytes
                            )
                            
                            text = self.recognizer.recognize_google(audio_data, language='en-US')
                            
                            if text and text.strip():
                                transcription_parts.append(text)
                                full_text = " ".join(transcription_parts)
                                transcription_display.success(f"📝 **Live Transcription:** {full_text}")
                        except sr.UnknownValueError:
                            pass  # No speech detected
                        except sr.RequestError as e:
                            st.warning(f"⚠️ Speech service error: {e}")
                        except Exception as e:
                            st.warning(f"Transcription error: {e}")
                        
                        current_audio_chunk = []
                        last_transcription_time = current_time
                    
                    time.sleep(0.1)
            
            # Final transcription of remaining audio
            if len(current_audio_chunk) > 0:
                try:
                    audio_array = np.array(current_audio_chunk, dtype=np.float32)
                    audio_data = sr.AudioData(
                        (audio_array * 32767).astype(np.int16).tobytes(),
                        SAMPLE_RATE,
                        2
                    )
                    text = self.recognizer.recognize_google(audio_data, language='en-US')
                    if text and text.strip():
                        transcription_parts.append(text)
                except:
                    pass
            
            # Save complete audio file
            if len(all_audio_data) > 0:
                audio_array = np.array(all_audio_data, dtype=np.float32)
                sf.write(audio_path, audio_array, SAMPLE_RATE)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Recording complete!")
            
            # Display final transcription
            final_transcription = " ".join(transcription_parts)
            if final_transcription:
                transcription_display.success(f"📝 **Final Transcription ({len(final_transcription.split())} words):** {final_transcription}")
            
            time.sleep(1)
            video_placeholder.empty()
            
            # Fallback if no real-time transcription worked
            if not final_transcription and os.path.exists(audio_path):
                try:
                    st.info("🔄 Processing complete audio file...")
                    with sr.AudioFile(audio_path) as source:
                        audio = self.recognizer.record(source)
                        final_transcription = self.recognizer.recognize_google(audio)
                        if final_transcription:
                            transcription_display.success(f"📝 **Transcription:** {final_transcription}")
                except Exception as e:
                    st.error(f"❌ Final transcription failed: {str(e)}")
            
            # Verify we have transcription
            if not final_transcription or not final_transcription.strip():
                st.warning("⚠️ No speech detected. Please speak more clearly and try again.")
                final_transcription = "No speech detected in recording."
            
            return final_transcription, audio_path, video_path
            
        except Exception as e:
            st.error(f"❌ Recording error: {str(e)}")
            # Return fallback data
            return "Recording failed - please use text input instead.", None, None
        
        finally:
            # Cleanup in finally block to ensure it runs
            try:
                if 'cap' in locals():
                    cap.release()
                if 'out' in locals():
                    out.release()
                if 'stream' in locals():
                    stream.close()
            except:
                pass
    
    def analyze_speech_patterns(self, audio_path):
        """Analyze recorded audio for speech patterns"""
        try:
            if not audio_path or not os.path.exists(audio_path):
                return {'success': False, 'error': 'Audio file not found'}
            
            file_size = os.path.getsize(audio_path)
            if file_size < 1000:
                return {'success': False, 'error': 'Audio file too small'}
            
            # Load audio using soundfile
            audio_array, sample_rate = sf.read(audio_path)
            
            # Convert to mono if stereo
            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)
            
            duration = len(audio_array) / sample_rate
            if duration == 0:
                return {'success': False, 'error': 'Zero duration audio'}
            
            rms = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
            zcr = np.sum(np.abs(np.diff(np.signbit(audio_array)))) / len(audio_array)
            
            return {
                'success': True,
                'speaking_pace_wpm': float(min(200, max(80, zcr * 1000))),
                'pause_frequency': float(max(0.5, 5 - (zcr * 10))),
                'clarity_score': float(min(10, max(1, (rms / 1000) * 8))),
                'volume_level': float(rms),
                'audio_duration_seconds': float(duration),
                'sample_rate': sample_rate,
                'total_frames': len(audio_array)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_video_feed(self, video_path):
        """Analyze video for engagement and face detection"""
        try:
            if not video_path or not os.path.exists(video_path):
                return {'success': False, 'error': 'Video file not found'}
            
            file_size = os.path.getsize(video_path)
            if file_size < 1000:
                return {'success': False, 'error': 'Video file too small'}
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {'success': False, 'error': 'Cannot open video'}
            
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            total_frames = 0
            face_frames = 0
            engagement_scores = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                total_frames += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    face_frames += 1
                    for (x, y, w, h) in faces:
                        frame_center_x = frame.shape[1] // 2
                        frame_center_y = frame.shape[0] // 2
                        face_center_x = x + w // 2
                        face_center_y = y + h // 2
                        
                        dist_x = abs(face_center_x - frame_center_x) / frame_center_x
                        dist_y = abs(face_center_y - frame_center_y) / frame_center_y
                        
                        engagement = max(0, 1.0 - (dist_x + dist_y) / 2)
                        engagement_scores.append(engagement)
            
            cap.release()
            
            if total_frames == 0:
                return {'success': False, 'error': 'No frames in video'}
            
            face_detection_ratio = face_frames / total_frames
            avg_engagement = np.mean(engagement_scores) if engagement_scores else 0.5
            
            return {
                'success': True,
                'face_detection_ratio': float(face_detection_ratio),
                'engagement_score': float(avg_engagement),
                'facial_expression': 'engaged' if avg_engagement > 0.7 else 'neutral',
                'total_frames_analyzed': total_frames,
                'frames_with_face': face_frames,
                'analysis_confidence': min(1.0, face_detection_ratio * 1.5)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}


class AudioVideoProcessor:
    """Standard audio/video processor (record-then-transcribe)"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.audio_data = None
        self.video_data = None
        
    def record_audio_video(self, duration=30):
        """
        Record audio and video for specified duration
        Returns: (audio_path, video_path)
        """
        try:
            # Create temporary files
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as audio_temp:
                audio_path = audio_temp.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='.avi') as video_temp:
                video_path = video_temp.name

            # Initialize camera
            cap = cv2.VideoCapture(0)
            camera_available = cap.isOpened()
            
            if not camera_available:
                st.warning("📷 Camera not available. Recording audio only.")
            
            # Initialize video writer if camera available
            out = None
            if camera_available:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 20)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

            # Audio recording parameters
            SAMPLE_RATE = 16000
            recorded_audio = []
            
            # Recording UI
            st.info(f"🎥 Recording for {duration} seconds... Speak now!")
            progress_bar = st.progress(0)
            status_text = st.empty()
            video_placeholder = st.empty()
            
            def audio_callback(indata, frames, time, status):
                """Callback for audio recording"""
                if status:
                    st.warning(f"Audio status: {status}")
                recorded_audio.extend(indata.copy())
            
            start_time = time.time()
            frame_count = 0
            
            # Start audio recording
            with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE):
                while (time.time() - start_time) < duration:
                    elapsed = time.time() - start_time
                    progress = elapsed / duration
                    progress_bar.progress(min(progress, 1.0))
                    remaining = duration - elapsed
                    status_text.text(f"⏺️ Recording... {remaining:.1f}s remaining")
                    
                    # Capture video frame if camera available
                    if camera_available:
                        ret, frame = cap.read()
                        if ret:
                            frame_count += 1
                            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            video_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
                            out.write(frame)
                    
                    time.sleep(0.1)
            
            # Verify we recorded something
            if len(recorded_audio) == 0:
                st.error("❌ No audio data captured!")
                return None, None
            
            # Save audio file
            audio_array = np.array(recorded_audio, dtype=np.float32)
            sf.write(audio_path, audio_array, SAMPLE_RATE)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Recording complete!")
            
            # Verify files
            if os.path.exists(audio_path):
                st.success(f"✅ Audio: {os.path.getsize(audio_path) / 1024:.1f} KB, {len(recorded_audio)} samples")
            if camera_available and os.path.exists(video_path):
                st.success(f"✅ Video: {os.path.getsize(video_path) / 1024:.1f} KB, {frame_count} frames")
            
            time.sleep(1)
            video_placeholder.empty()
            
            return audio_path, video_path
            
        except Exception as e:
            st.error(f"❌ Recording error: {str(e)}")
            return None, None
        
        finally:
            # Cleanup
            try:
                if 'cap' in locals():
                    cap.release()
                if 'out' in locals():
                    out.release()
            except:
                pass

    def speech_to_text(self, audio_path):
        """
        Convert speech to text using speech recognition
        Returns: (transcribed_text, success)
        """
        try:
            if not audio_path or not os.path.exists(audio_path):
                return "Audio file not found", False
            
            file_size = os.path.getsize(audio_path)
            st.info(f"🔍 Processing audio file: {file_size / 1024:.1f} KB")
            
            if file_size < 1000:
                return "No audio data recorded (file too small)", False
            
            with sr.AudioFile(audio_path) as source:
                st.info("🔊 Loading audio...")
                
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                st.info("🎤 Extracting speech...")
                audio_data = self.recognizer.record(source)
                
                st.info("🤖 Transcribing speech...")
                try:
                    text = self.recognizer.recognize_google(audio_data)
                    
                    if text and len(text.strip()) > 0:
                        st.success(f"✅ Transcription complete: {len(text)} characters")
                        return text, True
                    else:
                        return "No speech detected in audio", False
                        
                except sr.UnknownValueError:
                    return "Could not understand audio - please speak more clearly", False
                except sr.RequestError as e:
                    return f"Speech recognition service error: {e}", False
                except Exception as e:
                    return f"Recognition error: {str(e)}", False
                    
        except Exception as e:
            return f"Transcription error: {str(e)}", False
    
    def analyze_speech_patterns(self, audio_path):
        """Analyze speech patterns from audio"""
        try:
            if not audio_path or not os.path.exists(audio_path):
                return {'success': False, 'error': 'Audio file not found'}
            
            file_size = os.path.getsize(audio_path)
            if file_size < 1000:
                return {'success': False, 'error': 'No audio data available'}
            
            # Load audio using soundfile
            audio_array, sample_rate = sf.read(audio_path)
            
            # Convert to mono if stereo
            if len(audio_array.shape) > 1:
                audio_array = np.mean(audio_array, axis=1)
            
            duration = len(audio_array) / sample_rate
            if duration == 0:
                return {'success': False, 'error': 'Zero duration audio'}
            
            rms = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
            zcr = np.sum(np.abs(np.diff(np.signbit(audio_array)))) / len(audio_array)
            
            speaking_pace = min(200, max(80, zcr * 1000))
            clarity = min(10, max(1, (rms / 1000) * 8))
            
            return {
                'success': True,
                'speaking_pace_wpm': float(speaking_pace),
                'pause_frequency': float(max(0.5, 5 - (zcr * 10))),
                'clarity_score': float(clarity),
                'volume_level': float(rms),
                'audio_duration_seconds': float(duration),
                'sample_rate': sample_rate,
                'total_frames': len(audio_array)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_video_feed(self, video_path):
        """Analyze video feed for engagement"""
        try:
            if not video_path or not os.path.exists(video_path):
                return {'success': False, 'error': 'Video file not found'}
            
            file_size = os.path.getsize(video_path)
            if file_size < 1000:
                return {'success': False, 'error': 'No video data available'}
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return {'success': False, 'error': 'Could not open video file'}
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            total_frames = 0
            face_frames = 0
            engagement_scores = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                total_frames += 1
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                if len(faces) > 0:
                    face_frames += 1
                    for (x, y, w, h) in faces:
                        frame_center_x = frame.shape[1] // 2
                        frame_center_y = frame.shape[0] // 2
                        face_center_x = x + w // 2
                        face_center_y = y + h // 2
                        
                        dist_x = abs(face_center_x - frame_center_x) / frame_center_x
                        dist_y = abs(face_center_y - frame_center_y) / frame_center_y
                        
                        engagement = max(0, 1.0 - (dist_x + dist_y) / 2)
                        engagement_scores.append(engagement)
            
            cap.release()
            
            if total_frames == 0:
                return {'success': False, 'error': 'No frames in video'}
            
            face_detection_ratio = face_frames / total_frames
            avg_engagement = np.mean(engagement_scores) if engagement_scores else 0.5
            
            return {
                'success': True,
                'face_detection_ratio': float(face_detection_ratio),
                'engagement_score': float(avg_engagement),
                'facial_expression': 'engaged' if avg_engagement > 0.7 else 'neutral',
                'total_frames_analyzed': total_frames,
                'frames_with_face': face_frames,
                'analysis_confidence': min(1.0, face_detection_ratio * 1.5)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Create singleton instances
realtime_av_processor = RealtimeAudioVideoProcessor()
av_processor = AudioVideoProcessor()