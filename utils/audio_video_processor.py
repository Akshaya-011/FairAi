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
import pyaudio

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
        audio_path = None
        video_path = None
        cap = None
        out = None
        p = None
        stream = None
        
        try:
            # Create temporary files
            audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            video_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.avi')
            audio_path = audio_temp.name
            video_path = video_temp.name
            audio_temp.close()
            video_temp.close()
            
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000  # 16kHz for better speech recognition
            CHUNK = 1024
            
            # Initialize camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Camera not available. Please check camera permissions.")
                return "", None, None
            
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 20)
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
            
            # Start audio stream
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            # Storage
            audio_frames = []
            transcription_parts = []
            
            # Real-time recognition setup
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            
            start_time = time.time()
            audio_buffer = []
            last_transcription_time = start_time
            buffer_duration = 3  # Transcribe every 3 seconds
            
            st.info(f"🎤 **Live Recording Started** - Speak clearly! ({duration}s)")
            
            # Create placeholders
            progress_bar = st.progress(0)
            status_text = st.empty()
            video_placeholder = st.empty()
            transcription_display = st.empty()
            
            while (time.time() - start_time) < duration:
                elapsed = time.time() - start_time
                progress = elapsed / duration
                progress_bar.progress(min(progress, 1.0))
                remaining = duration - elapsed
                
                # Display status with word count
                current_words = len(' '.join(transcription_parts).split())
                status_text.text(f"⏺️ Recording... {remaining:.1f}s remaining | Words: {current_words}")
                
                # Capture audio
                try:
                    audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
                    audio_frames.append(audio_chunk)
                    audio_buffer.append(audio_chunk)
                except Exception as e:
                    pass  # Continue on audio errors
                
                # Capture video
                ret, frame = cap.read()
                if ret:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
                    out.write(frame)
                
                # Real-time transcription every N seconds
                current_time = time.time()
                if (current_time - last_transcription_time) >= buffer_duration and len(audio_buffer) > 0:
                    # Create audio data from buffer
                    buffer_audio = b''.join(audio_buffer)
                    
                    # Try to transcribe
                    try:
                        audio_data = sr.AudioData(buffer_audio, RATE, p.get_sample_size(FORMAT))
                        text = recognizer.recognize_google(audio_data, language='en-US')
                        
                        if text and text.strip():
                            transcription_parts.append(text)
                            # Display real-time transcription
                            full_text = " ".join(transcription_parts)
                            transcription_display.success(f"📝 **Live Transcription:** {full_text}")
                    except sr.UnknownValueError:
                        pass  # No speech detected
                    except sr.RequestError as e:
                        st.warning(f"⚠️ Speech service error: {e}")
                    except Exception:
                        pass  # Continue on any error
                    
                    # Reset buffer
                    audio_buffer = []
                    last_transcription_time = current_time
                
                time.sleep(0.01)
            
            # Final transcription of remaining buffer
            if len(audio_buffer) > 0:
                try:
                    buffer_audio = b''.join(audio_buffer)
                    audio_data = sr.AudioData(buffer_audio, RATE, p.get_sample_size(FORMAT))
                    text = recognizer.recognize_google(audio_data, language='en-US')
                    if text and text.strip():
                        transcription_parts.append(text)
                except:
                    pass
            
            # Save complete audio file
            if len(audio_frames) > 0:
                wf = wave.open(audio_path, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(audio_frames))
                wf.close()
            
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
                        audio = recognizer.record(source)
                        final_transcription = recognizer.recognize_google(audio)
                        if final_transcription:
                            transcription_display.success(f"📝 **Transcription:** {final_transcription}")
                except Exception as e:
                    st.error(f"❌ Transcription failed: {str(e)}")
            
            # Verify we have transcription
            if not final_transcription or not final_transcription.strip():
                st.warning("⚠️ No speech detected. Please speak more clearly and try again.")
            
            return final_transcription, audio_path, video_path
            
        except Exception as e:
            st.error(f"❌ Recording error: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")
            return "", None, None
        
        finally:
            # Cleanup resources
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
            if p:
                try:
                    p.terminate()
                except:
                    pass
            if cap:
                try:
                    cap.release()
                except:
                    pass
            if out:
                try:
                    out.release()
                except:
                    pass
    
    def analyze_speech_patterns(self, audio_path):
        """Analyze recorded audio for speech patterns"""
        try:
            if not os.path.exists(audio_path):
                return {'success': False, 'error': 'Audio file not found'}
            
            file_size = os.path.getsize(audio_path)
            if file_size < 1000:
                return {'success': False, 'error': 'Audio file too small'}
            
            with wave.open(audio_path, 'rb') as wf:
                sample_rate = wf.getframerate()
                n_frames = wf.getnframes()
                audio_signal = wf.readframes(n_frames)
                audio_array = np.frombuffer(audio_signal, dtype=np.int16)
                
                duration = n_frames / sample_rate
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
                    'total_frames': n_frames
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_video_feed(self, video_path):
        """Analyze video for engagement and face detection"""
        try:
            if not os.path.exists(video_path):
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
        audio_path = None
        video_path = None
        p = None
        stream = None
        cap = None
        out = None
        
        try:
            # Create temporary files
            audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            video_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.avi')
            audio_path = audio_temp.name
            video_path = video_temp.name
            audio_temp.close()
            video_temp.close()
            
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            CHUNK = 1024
            
            # Initialize camera
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Could not access camera. Please check camera permissions.")
                return None, None
            
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_FPS, 20)
            
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
            
            # Audio frames storage
            audio_frames = []
            
            # Start audio stream
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            # Recording UI
            st.info(f"🎥 Recording for {duration} seconds... Speak now!")
            progress_bar = st.progress(0)
            status_text = st.empty()
            video_placeholder = st.empty()
            
            start_time = time.time()
            frame_count = 0
            
            while (time.time() - start_time) < duration:
                elapsed = time.time() - start_time
                progress = elapsed / duration
                progress_bar.progress(min(progress, 1.0))
                remaining = duration - elapsed
                status_text.text(f"⏺️ Recording... {remaining:.1f}s remaining")
                
                # Capture audio
                try:
                    audio_data = stream.read(CHUNK, exception_on_overflow=False)
                    audio_frames.append(audio_data)
                except Exception as e:
                    pass
                
                # Capture video frame
                ret, frame = cap.read()
                if ret:
                    frame_count += 1
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    video_placeholder.image(rgb_frame, channels="RGB", use_container_width=True)
                    out.write(frame)
                
                time.sleep(0.01)
            
            # Verify we recorded something
            if len(audio_frames) == 0:
                st.error("❌ No audio data captured!")
                return None, None
            
            if frame_count == 0:
                st.warning("⚠️ No video frames captured!")
            
            # Save audio
            wf = wave.open(audio_path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(audio_frames))
            wf.close()
            
            progress_bar.progress(1.0)
            status_text.text("✅ Recording complete!")
            
            # Verify files
            if os.path.exists(audio_path):
                st.success(f"✅ Audio: {os.path.getsize(audio_path) / 1024:.1f} KB, {len(audio_frames)} frames")
            if os.path.exists(video_path):
                st.success(f"✅ Video: {os.path.getsize(video_path) / 1024:.1f} KB, {frame_count} frames")
            
            time.sleep(1)
            video_placeholder.empty()
            
            return audio_path, video_path
            
        except Exception as e:
            st.error(f"❌ Recording error: {str(e)}")
            import traceback
            st.error(f"Details: {traceback.format_exc()}")
            return None, None
        
        finally:
            # Cleanup
            if stream:
                try:
                    stream.stop_stream()
                    stream.close()
                except:
                    pass
            if p:
                try:
                    p.terminate()
                except:
                    pass
            if cap:
                try:
                    cap.release()
                except:
                    pass
            if out:
                try:
                    out.release()
                except:
                    pass

    def speech_to_text(self, audio_path):
        """
        Convert speech to text using speech recognition
        Returns: (transcribed_text, success)
        """
        try:
            if not os.path.exists(audio_path):
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
            if not os.path.exists(audio_path):
                return {'success': False, 'error': 'Audio file not found'}
            
            file_size = os.path.getsize(audio_path)
            if file_size < 1000:
                return {'success': False, 'error': 'No audio data available'}
            
            with wave.open(audio_path, 'rb') as wf:
                sample_width = wf.getsampwidth()
                sample_rate = wf.getframerate()
                n_frames = wf.getnframes()
                audio_signal = wf.readframes(n_frames)
                
                if sample_width == 2:
                    audio_array = np.frombuffer(audio_signal, dtype=np.int16)
                elif sample_width == 4:
                    audio_array = np.frombuffer(audio_signal, dtype=np.int32)
                else:
                    audio_array = np.frombuffer(audio_signal, dtype=np.int8)
                
                duration = n_frames / sample_rate
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
                    'total_frames': n_frames
                }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_video_feed(self, video_path):
        """Analyze video feed for engagement"""
        try:
            if not os.path.exists(video_path):
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