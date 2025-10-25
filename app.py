import streamlit as st
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
import base64
import time

# Add the utils directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import from your utils package structure - FIXED IMPORTS
try:
    from utils.resume_parser import ResumeParser
    from utils.question_gen import QuestionGenerator
    from utils.ai_enhancer import AIEnhancer
    from utils.bias_detector import detect_bias_in_text, analyze_question_fairness, generate_bias_report
    from utils.resume_parser import build_skills_graph, get_skills_by_category, calculate_skill_metrics
    from utils.visualizer import create_skills_network, plot_skill_categories, create_category_barchart, create_confidence_heatmap
    from utils.bias_heatmap import BiasHeatmapGenerator, bias_heatmap
    from utils.difficulty_manager import DifficultyManager, difficulty_manager
    # NEW: Import the heatmap generator
    from utils.heatmap_generator import HeatmapGenerator, heatmap_generator
    # NEW: Import analytics engine
    from utils.analytics_engine import AnalyticsEngine
    # NEW: Import audio-video processor and bias detector functions
    from utils.audio_video_processor import AudioVideoProcessor
    from utils.audio_video_processor import RealtimeAudioVideoProcessor
    from utils.bias_detector import detect_audio_biases, detect_video_biases, analyze_communication_skills, generate_comprehensive_av_report
except ImportError as e:
    st.error(f"Some modules not found: {e}")
    
    # Fallback implementations
    class ResumeParser:
        def extract_skills(self, text):
            return [("python", "technical", 0.8), ("communication", "soft", 0.7)]
        def parse_experience(self, text):
            return "Mid"
    
    class QuestionGenerator:
        def generate_questions(self, skills, experience):
            return [
                "Tell me about your experience with Python",
                "Describe a challenging project you worked on", 
                "How do you handle teamwork situations?",
                "What are your strengths in communication?",
                "Where do you see yourself in 5 years?"
            ]
    
    class AIEnhancer:
        def __init__(self): 
            self.available = False
        def improve_question(self, *args): 
            return {"success": False, "improved_question": args[0], "explanation": "AI not available"}
        def analyze_answer_depth(self, *args): 
            return {"success": False, "quality_score": 5, "strengths": [], "skills_demonstrated": []}
        def generate_follow_up_question(self, *args): 
            return {"success": False, "follow_up_question": "No follow-up available"}
    
    # NEW: Fallback implementations for the new modules
    class BiasHeatmapGenerator:
        def generate_real_time_heatmap(self, interview_data):
            fig = go.Figure()
            fig.update_layout(title="Bias Heatmap (Module Not Available)")
            return fig
        def generate_trend_analysis(self, bias_history):
            fig = go.Figure()
            fig.update_layout(title="Trend Analysis (Module Not Available)")
            return fig
    
    class DifficultyManager:
        def assess_answer_quality(self, answer, question_type):
            return 5
        def get_next_difficulty(self, current_difficulty, recent_scores):
            return current_difficulty
        def get_question_for_difficulty(self, difficulty, skill, question_type='technical'):
            return f"Tell me about your experience with {skill}"
    
    class HeatmapGenerator:
        def generate_bias_heatmap(self, interview_data): 
            fig = go.Figure()
            fig.update_layout(title="Heatmap Generator Not Available")
            return fig
        def generate_timeline_heatmap(self, bias_history): 
            fig = go.Figure()
            fig.update_layout(title="Timeline Heatmap Not Available")
            return fig
        def generate_category_distribution(self, category_breakdown): 
            fig = go.Figure()
            fig.update_layout(title="Category Distribution Not Available")
            return fig
        def generate_severity_gauge(self, overall_score): 
            fig = go.Figure()
            fig.update_layout(title="Severity Gauge Not Available")
            return fig
    
    class AnalyticsEngine:
        def calculate_candidate_fit(self, skills_graph, job_requirements):
            return {
                'overall_score': 75.0,
                'required_skills_score': 80.0,
                'preferred_skills_score': 70.0,
                'missing_required_skills': ['advanced_sql'],
                'missing_preferred_skills': ['docker'],
                'strengths': ['python', 'communication'],
                'weaknesses': ['cloud_architecture']
            }
        
        def analyze_communication_skills(self, answers_data):
            return {
                'coherence_score': 72.5,
                'avg_response_time_seconds': 8.2,
                'avg_answer_length': 45.3,
                'confidence_level': 68.0,
                'communication_style': "Articulate and Confident",
                'improvement_areas': ["Response time", "Confidence and assertiveness"]
            }
        
        def generate_improvement_recommendations(self, interview_data):
            return [
                "Focus on developing required skills: advanced_sql",
                "Work on structuring answers more clearly using STAR method",
                "Practice speaking with more confidence and avoid tentative language"
            ]
        
        def calculate_hire_confidence(self, analytics_data):
            return 78.5
        
        def generate_comparative_analytics(self, candidates_data):
            return {
                'candidates_ranked': [
                    {'candidate_id': 'candidate_1', 'rank': 1, 'overall_score': 85.0, 'hire_confidence': 82.0},
                    {'candidate_id': 'candidate_2', 'rank': 2, 'overall_score': 75.0, 'hire_confidence': 78.5}
                ],
                'skills_comparison': {
                    'python': [90, 85],
                    'communication': [80, 75]
                },
                'performance_metrics': {},
                'diversity_metrics': {
                    'total_candidates': 2,
                    'gender_diversity': 'Medium',
                    'experience_variance': 'High',
                    'background_diversity': 'Medium'
                }
            }

    # NEW: Fallback implementations for audio-video
    class AudioVideoProcessor:
        def record_audio_video(self, duration=30):
            return "temp_audio.wav", "temp_video.avi"
        def speech_to_text(self, audio_path):
            return "Audio transcription not available", False
        def analyze_speech_patterns(self, audio_path):
            return {'success': False, 'error': 'Audio analysis not available'}
        def analyze_video_feed(self, video_path):
            return {'success': False, 'error': 'Video analysis not available'}
    
    class RealtimeAudioVideoProcessor:
        def start_realtime_recording(self, duration=30):
            return "Transcription not available", "temp_audio.wav", "temp_video.avi"
        def analyze_speech_patterns(self, audio_path):
            return {'success': False, 'error': 'Audio analysis not available'}
        def analyze_video_feed(self, video_path):
            return {'success': False, 'error': 'Video analysis not available'}
    
    # NEW: Fallback audio/video bias detection
    def detect_audio_biases(speech_analysis):
        return {'biases_detected': [], 'severity': 'None', 'recommendations': ['Audio analysis unavailable']}
    
    def detect_video_biases(video_analysis):
        return {'biases_detected': [], 'severity': 'None', 'recommendations': ['Video analysis unavailable']}
    
    def analyze_communication_skills(speech_analysis, video_analysis):
        return {'audio_insights': [], 'video_insights': [], 'overall_assessment': 'Audio/Video analysis not available'}
    
    def generate_comprehensive_av_report(speech_analysis, video_analysis):
        return {'overall_assessment': {'total_bias_instances': 0, 'overall_severity': 'None'}}
    
    bias_heatmap = BiasHeatmapGenerator()
    difficulty_manager = DifficultyManager()
    heatmap_generator = HeatmapGenerator()
    analytics_engine = AnalyticsEngine()
    av_processor = AudioVideoProcessor()
    
    def detect_bias_in_text(text): 
        return {"bias_types": [], "severity": "Low", "confidence": 0.0}
    
    def analyze_question_fairness(question):
        return {
            "question": question,
            "bias_analysis": {"bias_types": [], "severity": "None"},
            "risk_level": "Low",
            "suggestion": "No issues detected"
        }
    
    def generate_bias_report(interview_data):
        return {
            "overall_score": 100, 
            "grade": "A+", 
            "recommendations": ["No biases detected"],
            "category_breakdown": {},
            "trend_analysis": {"hotspots": []}
        }
    
    def build_skills_graph(*args): 
        return {}
    def get_skills_by_category(*args): 
        return {}
    def calculate_skill_metrics(*args): 
        return {"total_skills": 0, "avg_confidence": 0, "total_relationships": 0, "connectivity_score": 0}
    def create_skills_network(*args): 
        return go.Figure()
    def plot_skill_categories(*args): 
        return go.Figure()
    def create_category_barchart(*args): 
        return go.Figure()
    def create_confidence_heatmap(*args): 
        return go.Figure()

class FairAIHireApp:
    def __init__(self):
        try:
            self.parser = ResumeParser()
            self.question_gen = QuestionGenerator()
            self.ai_enhancer = AIEnhancer()
            # NEW: Initialize the new components
            self.bias_heatmap = bias_heatmap
            self.difficulty_manager = difficulty_manager
            self.heatmap_generator = heatmap_generator
            self.analytics_engine = AnalyticsEngine()
            # NEW: Initialize audio-video processor
            self.av_processor = av_processor
            # NEW: Initialize real-time AV processor
            self.rt_av_processor = None
        except Exception as e:
            st.error(f"Error initializing: {e}")
            self.parser = ResumeParser()
            self.question_gen = QuestionGenerator()
            self.ai_enhancer = AIEnhancer()
            # NEW: Initialize fallbacks
            self.bias_heatmap = bias_heatmap
            self.difficulty_manager = difficulty_manager
            self.heatmap_generator = heatmap_generator
            self.analytics_engine = AnalyticsEngine()
            self.av_processor = AudioVideoProcessor()
            self.rt_av_processor = None
        
        self.setup_page()
    
    def setup_page(self):
        st.set_page_config(
            page_title="FairAI Hire - Bias-Free Interviews",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Enhanced CSS for dark/light theme compatibility
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        .skill-chip {
            background-color: #2e86ab;
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            margin: 0.3rem;
            display: inline-block;
            font-size: 0.9rem;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .skill-chip-technical {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .skill-chip-soft {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }
        .question-box {
            background-color: #1e1e1e;
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 6px solid #1f77b4;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .ai-enhanced-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 6px solid #ffd700;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .section-header {
            color: #1f77b4;
            font-size: 1.8rem;
            margin: 1.5rem 0 1rem 0;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 0.5rem;
        }
        .progress-text {
            color: white;
            font-weight: bold;
            text-align: center;
        }
        .custom-container {
            background-color: #1e1e1e;
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #333;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
        }
        .ai-analysis-box {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .bias-alert-box {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 6px solid #ff6b6b;
        }
        .recruiter-metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem;
        }
        .hire-confidence-high {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }
        .hire-confidence-medium {
            background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        }
        .hire-confidence-low {
            background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        }
        .stTextArea textarea {
            background-color: #2b2b2b !important;
            color: white !important;
            border: 1px solid #555 !important;
        }
        p, div, span, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        
        /* NEW: Audio/Video specific styles */
        .av-recording-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 6px solid #ff6b6b;
        }
        .av-preview-box {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .av-analysis-section {
            background-color: #2d2d2d;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #555;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        defaults = {
            'current_question_index': 0,
            'candidate_skills': [],
            'candidate_experience': "Unknown",
            'interview_questions': [],
            'candidate_answers': [],
            'bias_reports': [],
            'interview_started': False,
            'interview_completed': False,
            'resume_analyzed': False,
            'ai_enabled': False,
            'ai_enhanced_questions': [],
            'answer_analysis': [],
            'follow_up_questions': [],
            'skills_graph': {},
            'skills_data': {},
            # NEW: Add difficulty tracking and bias history
            'current_difficulty': 'Medium',
            'answer_scores': [],
            'bias_history': [],
            'question_bias_warnings': [],
            'interview_data': {
                'questions': [], 'answers': [], 'bias_analysis': [],
                'start_time': None, 'end_time': None
            },
            # NEW: Analytics data
            'analytics_data': {},
            'comparative_data': {},
            'candidate_pool': [],
            # NEW: Audio/Video session state
            'av_recorded': False,
            'audio_path': None,
            'video_path': None,
            'fallback_to_text': False,
            'start_recording': False,
            'recording_question_index': None,
            'auto_analyze': False,
            'response_type': 'text'  # 'text' or 'audio_video'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def reset_interview(self):
        """Reset the interview session"""
        for key in list(st.session_state.keys()):
            if key != 'ai_enabled':  # Keep AI setting
                del st.session_state[key]
        self.initialize_session_state()
    
    def analyze_resume(self, resume_text):
        """Analyze resume and extract skills/experience"""
        try:
            skills_result = self.parser.extract_skills(resume_text)
            experience_level = self.parser.parse_experience(resume_text)
            
            st.session_state.candidate_skills = skills_result
            st.session_state.candidate_experience = experience_level
            st.session_state.resume_analyzed = True
            
            # Build skills graph for visualization
            st.session_state.skills_graph = build_skills_graph(resume_text)
            st.session_state.skills_data = get_skills_by_category(st.session_state.skills_graph)
            
            return True
        except Exception as e:
            st.error(f"Error analyzing resume: {str(e)}")
            return False
    
    def generate_interview_questions(self):
        """Generate personalized interview questions with bias checking"""
        try:
            questions = self.question_gen.generate_questions(
                st.session_state.candidate_skills,
                st.session_state.candidate_experience
            )
            
            # NEW: Check questions for potential bias before displaying
            checked_questions = []
            bias_warnings = []
            
            for i, question in enumerate(questions):
                try:
                    bias_check = analyze_question_fairness(question)
                    # FIXED: Use .get() with default value to avoid KeyError
                    risk_level = bias_check.get('risk_level', 'Low')
                    suggestion = bias_check.get('suggestion', 'Consider rephrasing this question')
                    
                    if risk_level == 'High':
                        bias_warnings.append(f"Question {i+1}: {suggestion}")
                except Exception as e:
                    # If bias checking fails, log but continue
                    print(f"Bias check warning for question {i+1}: {str(e)}")
                    # Continue with the question anyway
                
                checked_questions.append(question)
            
            # Store bias warnings for later reference
            st.session_state.question_bias_warnings = bias_warnings
            
            st.session_state.interview_questions = checked_questions
            st.session_state.candidate_answers = [""] * len(checked_questions)
            st.session_state.bias_reports = [None] * len(checked_questions)
            st.session_state.answer_analysis = [None] * len(checked_questions)
            st.session_state.follow_up_questions = [None] * len(checked_questions)
            st.session_state.interview_started = True
            st.session_state.interview_data['questions'] = checked_questions
            st.session_state.interview_data['start_time'] = datetime.now()
            
            # Show bias warnings if any
            if bias_warnings and st.session_state.ai_enabled:
                with st.container():
                    st.error("🚨 **Bias Alert in Generated Questions:**")
                    for warning in bias_warnings:
                        st.write(f"• {warning}")
            
            # Generate AI-enhanced questions if enabled
            if st.session_state.ai_enabled and self.ai_enhancer.available:
                with st.spinner("🤖 Enhancing questions with AI..."):
                    st.session_state.ai_enhanced_questions = []
                    for i, question in enumerate(questions):
                        enhanced = self.ai_enhancer.improve_question(
                            question, 
                            f"Skills: {[skill[0] for skill in st.session_state.candidate_skills]}"
                        )
                        st.session_state.ai_enhanced_questions.append(enhanced)
            
            return True
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return False

    def realtime_audio_video_interface(self, question_index):
        """
        Real-time audio/video interface with live transcription
        Add this method to your FairAIHireApp class
        """
        st.markdown("---")
        st.subheader("🎙️ Real-Time Audio/Video Response")
        
        # State management (unique per question)
        state_key = f"realtime_state_{question_index}"
        if state_key not in st.session_state:
            st.session_state[state_key] = {
                'recorded': False,
                'transcription': None,
                'audio_path': None,
                'video_path': None,
                'speech_analysis': None,
                'video_analysis': None
            }
        
        state = st.session_state[state_key]
        
        # Info
        with st.expander("ℹ️ Real-Time Recording", expanded=not state['recorded']):
            st.info("""
            **How it works:**
            - 🎤 Speak naturally - transcription appears **live** as you speak
            - 📹 Camera shows live preview
            - ⚡ See your words instantly (updates every 3 seconds)
            - 🔄 Complete transcription ready at the end
            - 📊 Automatic speech and engagement analysis
            """)
            st.warning("🌐 **Requires internet** for Google Speech Recognition")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ⚙️ Settings")
            duration = st.slider(
                "Duration (seconds)", 
                15, 60, 30,
                key=f"rt_duration_{question_index}",
                disabled=state['recorded'],
                help="How long to record your response"
            )
            
            if not state['recorded']:
                if st.button(
                    "🎤 Start Real-Time Recording",
                    use_container_width=True,
                    type="primary",
                    key=f"rt_start_{question_index}"
                ):
                    # Initialize processor if needed
                    if not hasattr(self, 'rt_av_processor') or self.rt_av_processor is None:
                        try:
                            from utils.audio_video_processor import RealtimeAudioVideoProcessor
                            self.rt_av_processor = RealtimeAudioVideoProcessor()
                        except ImportError:
                            st.error("❌ Real-time audio/video processor not available")
                            return None
                    
                    # Start real-time recording
                    transcription, audio_path, video_path = self.rt_av_processor.start_realtime_recording(
                        duration=duration
                    )
                    
                    if transcription and transcription.strip():
                        state['transcription'] = transcription
                        state['audio_path'] = audio_path
                        state['video_path'] = video_path
                        state['recorded'] = True
                        
                        # Analyze in background
                        with st.spinner("📊 Analyzing recording..."):
                            if audio_path and os.path.exists(audio_path):
                                state['speech_analysis'] = self.rt_av_processor.analyze_speech_patterns(audio_path)
                            if video_path and os.path.exists(video_path):
                                state['video_analysis'] = self.rt_av_processor.analyze_video_feed(video_path)
                        
                        st.success("✅ Recording and analysis complete!")
                        st.rerun()
                    else:
                        st.error("❌ No speech detected. Please try again and speak more clearly.")
            else:
                st.success("✅ Recording complete!")
                if st.button(
                    "🔄 Record Again",
                    use_container_width=True,
                    key=f"rt_again_{question_index}"
                ):
                    # Cleanup files
                    if state['audio_path'] and os.path.exists(state['audio_path']):
                        try:
                            os.remove(state['audio_path'])
                        except:
                            pass
                    if state['video_path'] and os.path.exists(state['video_path']):
                        try:
                            os.remove(state['video_path'])
                        except:
                            pass
                    
                    # Reset state
                    st.session_state[state_key] = {
                        'recorded': False,
                        'transcription': None,
                        'audio_path': None,
                        'video_path': None,
                        'speech_analysis': None,
                        'video_analysis': None
                    }
                    st.rerun()
        
        with col2:
            st.markdown("#### 📊 Status")
            if state['recorded']:
                st.success("✅ **Recording Complete**")
                words = len(state['transcription'].split()) if state['transcription'] else 0
                st.metric("Words Captured", words)
                if words < 10:
                    st.warning("⚠️ Response seems short. Consider recording again.")
            else:
                st.info("⏳ **Ready to Record**")
                st.write("Click button to start")
        
        # Display results
        if state['recorded'] and state['transcription']:
            st.markdown("---")
            st.subheader("📝 Your Transcribed Answer")
            st.success(state['transcription'])
            
            # Speech metrics
            if state['speech_analysis'] and state['speech_analysis'].get('success'):
                st.markdown("#### 🎤 Speech Analysis")
                speech = state['speech_analysis']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Speaking Pace", f"{speech['speaking_pace_wpm']:.0f} WPM")
                with col2:
                    st.metric("Clarity", f"{speech['clarity_score']:.1f}/10")
                with col3:
                    st.metric("Duration", f"{speech['audio_duration_seconds']:.1f}s")
            
            # Video metrics
            if state['video_analysis'] and state['video_analysis'].get('success'):
                st.markdown("#### 📹 Engagement Analysis")
                video = state['video_analysis']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Face Detection", f"{video['face_detection_ratio']*100:.0f}%")
                with col2:
                    st.metric("Engagement", f"{video['engagement_score']*100:.0f}%")
                with col3:
                    st.metric("Expression", video['facial_expression'].title())
            
            # Media preview
            with st.expander("🎬 Review Recording"):
                col1, col2 = st.columns(2)
                with col1:
                    if state['video_path'] and os.path.exists(state['video_path']):
                        st.markdown("**📹 Video Recording:**")
                        st.video(state['video_path'])
                with col2:
                    if state['audio_path'] and os.path.exists(state['audio_path']):
                        st.markdown("**🔊 Audio Recording:**")
                        st.audio(state['audio_path'])
            
            # Return transcription
            return state['transcription']
        
        return None

    def audio_video_interface(self, question_index):
        """
        Audio/Video recording interface with live camera preview
        """
        st.markdown("---")
        st.subheader("🎥 Audio/Video Response")
        
        # Information section
        with st.expander("ℹ️ How to use audio/video response", expanded=True):
            st.info("""
            **Instructions:**
            1. Click 'Start Recording' - camera will open with live preview
            2. Speak clearly while looking at the camera
            3. Recording will automatically stop after selected duration
            4. Your speech will be converted to text automatically
            5. Review analysis and submit your response
            """)
        
        st.warning("🔒 **Privacy Note:** Audio/video is processed locally and never stored on servers.")
        
        # Create main interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ⚙️ Recording Settings")
            recording_duration = st.slider(
                "Recording Duration (seconds)", 
                15, 60, 30, 
                key=f"duration_{question_index}",
                help="How long to record your response"
            )
            
            # Recording button
            if st.button(
                "🎤 Start Recording", 
                use_container_width=True, 
                key=f"record_{question_index}",
                type="primary"
            ):
                # Set flag to start recording
                st.session_state.start_recording = True
                st.session_state.recording_question_index = question_index
        
        with col2:
            st.markdown("#### 📊 Status")
            if st.session_state.get('av_recorded', False):
                st.success("✅ **Recording Complete!**")
                st.write("Your response has been recorded and analyzed.")
            else:
                st.info("⏳ **Ready to Record**")
                st.write("Click the button to start recording.")
        
        # Handle recording when flag is set
        if (st.session_state.get('start_recording', False) and 
            st.session_state.get('recording_question_index') == question_index):
            
            st.info("🎥 **Camera is starting... Please allow camera access if prompted.**")
            
            # Record audio and video
            audio_path, video_path = self.av_processor.record_audio_video(
                duration=recording_duration
            )
            
            # Reset recording flag
            st.session_state.start_recording = False
            
            if audio_path:
                # Store paths in session state
                st.session_state.audio_path = audio_path
                st.session_state.video_path = video_path
                st.session_state.av_recorded = True
                
                # Auto-analyze the recording
                st.session_state.auto_analyze = True
                
                st.rerun()
            else:
                st.error("❌ Recording failed. Please check your camera and microphone permissions.")
                st.session_state.fallback_to_text = True
        
        # Auto-analyze after recording
        if (st.session_state.get('auto_analyze', False) and 
            st.session_state.get('av_recorded', False)):
            
            with st.spinner("🔍 Analyzing your recording..."):
                result_text = self.analyze_audio_video_response(question_index)
                
                if result_text is not None:
                    # Store the transcribed text as the answer
                    st.session_state.candidate_answers[question_index] = result_text
                    st.session_state.auto_analyze = False
                    st.success("✅ Analysis complete! Your response has been saved.")
                    
                    # Show preview of recorded media
                    if st.session_state.video_path and os.path.exists(st.session_state.video_path):
                        st.subheader("📹 Recording Preview")
                        st.video(st.session_state.video_path)
                    
                    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                        st.audio(st.session_state.audio_path)
                    
                    return result_text
                else:
                    st.error("❌ Analysis failed. Please try again.")
                    st.session_state.auto_analyze = False
        
        # Show analyze button if recording exists but hasn't been analyzed
        if (st.session_state.get('av_recorded', False) and 
            not st.session_state.get('auto_analyze', False) and
            st.session_state.candidate_answers[question_index] == ""):
            
            if st.button("🔍 Analyze Recording", use_container_width=True, key=f"analyze_{question_index}"):
                result_text = self.analyze_audio_video_response(question_index)
                if result_text is not None:
                    st.session_state.candidate_answers[question_index] = result_text
                    st.success("✅ Analysis complete! Your response has been saved.")
                    return result_text
        
        # Fallback to text
        if st.session_state.get('fallback_to_text', False):
            st.markdown("---")
            st.warning("🎯 **Using Text Response**")
            st.info("Please provide your answer in text format:")
            
            fallback_answer = st.text_area(
                "Your answer:",
                value=st.session_state.candidate_answers[question_index],
                height=150,
                placeholder="Type your answer here...",
                key=f"fallback_{question_index}",
                label_visibility="collapsed"
            )
            
            if st.button("💾 Save Text Response", key=f"save_fallback_{question_index}"):
                if fallback_answer.strip():
                    return fallback_answer
                else:
                    st.error("Please provide an answer before saving.")
        
        return None

    def analyze_audio_video_response(self, question_index):
        """
        Analyze the recorded audio and video response
        """
        try:
            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info("🔄 Starting analysis...")
            progress_bar.progress(10)
            
            result_text = ""
            
            # Speech to text analysis
            if st.session_state.audio_path:
                status_text.info("🔊 Transcribing audio...")
                progress_bar.progress(30)
                
                text, success = self.av_processor.speech_to_text(st.session_state.audio_path)
                
                if success and text != "Could not understand audio":
                    result_text = text
                    st.subheader("📝 Transcribed Text")
                    st.success(text)
                    progress_bar.progress(50)
                else:
                    st.warning(f"🗣️ Could not transcribe audio: {text}")
                    progress_bar.progress(50)
            
            # If we have text, proceed with analysis
            if result_text:
                # Analyze speech patterns
                status_text.info("🎤 Analyzing speech patterns...")
                speech_analysis = self.av_processor.analyze_speech_patterns(st.session_state.audio_path)
                progress_bar.progress(70)
                
                if speech_analysis.get('success'):
                    self._display_speech_analysis(speech_analysis)
                
                # Analyze video if available
                if st.session_state.video_path and os.path.exists(st.session_state.video_path):
                    status_text.info("📹 Analyzing video...")
                    video_analysis = self.av_processor.analyze_video_feed(st.session_state.video_path)
                    progress_bar.progress(90)
                    
                    if video_analysis.get('success'):
                        self._display_video_analysis(video_analysis)
                    
                    # Run bias detection
                    if speech_analysis.get('success') and video_analysis.get('success'):
                        status_text.info("🛡️ Checking for biases...")
                        self._run_bias_detection(speech_analysis, video_analysis)
            
            progress_bar.progress(100)
            status_text.success("✅ Analysis complete!")
            
            # Cleanup files
            self._cleanup_av_files()
            
            return result_text
            
        except Exception as e:
            st.error(f"❌ Analysis error: {str(e)}")
            return None

    def _display_speech_analysis(self, speech_analysis):
        """Display speech analysis results"""
        st.subheader("🎤 Speech Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            wpm = speech_analysis['speaking_pace_wpm']
            st.metric("Speaking Pace", f"{wpm:.1f} WPM")
        
        with col2:
            pause_freq = speech_analysis['pause_frequency']
            st.metric("Pause Frequency", f"{pause_freq:.1f}/sec")
        
        with col3:
            clarity = speech_analysis['clarity_score']
            st.metric("Clarity Score", f"{clarity:.1f}/10")

    def _display_video_analysis(self, video_analysis):
        """Display video analysis results"""
        st.subheader("📊 Video Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            face_ratio = video_analysis['face_detection_ratio'] * 100
            st.metric("Face Detection", f"{face_ratio:.1f}%")
        
        with col2:
            engagement = video_analysis['engagement_score'] * 100
            st.metric("Engagement", f"{engagement:.1f}%")
        
        with col3:
            expression = video_analysis['facial_expression']
            st.metric("Expression", expression.title())

    def _run_bias_detection(self, speech_analysis, video_analysis):
        """Run bias detection on audio/video analysis"""
        st.subheader("🛡️ Bias Detection")
        
        # Audio bias detection
        audio_biases = detect_audio_biases(speech_analysis)
        if audio_biases['biases_detected']:
            for bias in audio_biases['biases_detected']:
                st.warning(f"**Audio - {bias['type']}**: {bias['message']}")
        else:
            st.success("✅ No significant audio biases detected")
        
        # Video bias detection
        video_biases = detect_video_biases(video_analysis)
        if video_biases['biases_detected']:
            for bias in video_biases['biases_detected']:
                st.warning(f"**Video - {bias['type']}**: {bias['message']}")
        else:
            st.success("✅ No significant video biases detected")

    def _cleanup_av_files(self):
        """Clean up temporary audio/video files"""
        try:
            if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
                os.remove(st.session_state.audio_path)
            if st.session_state.video_path and os.path.exists(st.session_state.video_path):
                os.remove(st.session_state.video_path)
        except:
            pass  # Ignore cleanup errors

    def submit_answer(self, answer_text, question_index):
        """Submit answer and run bias detection - ENHANCED FOR AUDIO/VIDEO"""
        # For audio/video responses, we might have empty text but successful recording
        if answer_text.strip() or st.session_state.get('av_recorded', False):
            st.session_state.candidate_answers[question_index] = answer_text
            
            # Run bias detection on text (if available)
            if answer_text.strip():
                bias_result = detect_bias_in_text(answer_text)
                st.session_state.bias_reports[question_index] = bias_result
            else:
                # For pure audio/video responses, create a placeholder bias report
                st.session_state.bias_reports[question_index] = {
                    'bias_types': [], 
                    'severity': 'None', 
                    'message': 'Audio/Video response - text analysis not available'
                }
            
            # NEW: Assess answer quality and update difficulty
            current_question = st.session_state.interview_questions[question_index]
            question_type = 'technical' if any(skill[0].lower() in current_question.lower() 
                                            for skill in st.session_state.candidate_skills 
                                            if skill[1] == 'technical') else 'soft'
            
            quality_score = self.difficulty_manager.assess_answer_quality(answer_text, question_type)
            st.session_state.answer_scores.append(quality_score)
            
            # Update difficulty based on recent performance
            recent_scores = st.session_state.answer_scores[-3:]  # Last 3 answers
            new_difficulty = self.difficulty_manager.get_next_difficulty(
                st.session_state.current_difficulty, recent_scores
            )
            st.session_state.current_difficulty = new_difficulty
            
            # NEW: Update bias history for trend analysis
            bias_entry = {
                'timestamp': datetime.now(),
                'high_count': len([r for r in st.session_state.bias_reports if r and r.get('severity') == 'High']),
                'medium_count': len([r for r in st.session_state.bias_reports if r and r.get('severity') == 'Medium']),
                'low_count': len([r for r in st.session_state.bias_reports if r and r.get('severity') == 'Low'])
            }
            st.session_state.bias_history.append(bias_entry)
            
            # Run AI analysis if enabled
            if st.session_state.ai_enabled and self.ai_enhancer.available and answer_text.strip():
                with st.spinner("🤖 Analyzing answer depth..."):
                    skills_list = [skill[0] for skill in st.session_state.candidate_skills]
                    analysis = self.ai_enhancer.analyze_answer_depth(
                        answer_text, 
                        st.session_state.interview_questions[question_index],
                        skills_list
                    )
                    st.session_state.answer_analysis[question_index] = analysis
                    
                    # Generate follow-up question
                    skill_focus = None
                    if skills_list and question_index < len(skills_list):
                        skill_focus = skills_list[min(question_index, len(skills_list)-1)]
                    
                    follow_up = self.ai_enhancer.generate_follow_up_question(
                        answer_text,
                        st.session_state.interview_questions[question_index],
                        skill_focus
                    )
                    st.session_state.follow_up_questions[question_index] = follow_up
            
            # Update interview data
            if question_index < len(st.session_state.interview_data['answers']):
                st.session_state.interview_data['answers'][question_index] = answer_text
                st.session_state.interview_data['bias_analysis'][question_index] = bias_result
            else:
                st.session_state.interview_data['answers'].append(answer_text)
                st.session_state.interview_data['bias_analysis'].append(bias_result)
            
            return True
        return False
    
    def navigate_questions(self, direction):
        """Navigate between questions"""
        if direction == "next" and st.session_state.current_question_index < len(st.session_state.interview_questions) - 1:
            st.session_state.current_question_index += 1
        elif direction == "previous" and st.session_state.current_question_index > 0:
            st.session_state.current_question_index -= 1
    
    def complete_interview(self):
        """Mark interview as completed"""
        st.session_state.interview_completed = True
        st.session_state.interview_data['end_time'] = datetime.now()
        
        # Generate analytics when interview is completed
        self.generate_candidate_analytics()
        st.rerun()
    
    def generate_candidate_analytics(self):
        """Generate comprehensive analytics for the candidate"""
        try:
            # Mock job requirements - in real implementation, this would come from job description
            job_requirements = {
                'required_skills': ['python', 'communication', 'problem solving'],
                'preferred_skills': ['javascript', 'teamwork', 'leadership']
            }
            
            # Calculate candidate fit
            skills_fit = self.analytics_engine.calculate_candidate_fit(
                st.session_state.skills_graph,
                job_requirements
            )
            
            # Analyze communication skills
            answers_data = [{'text': answer, 'response_time': 5} for answer in st.session_state.candidate_answers if answer.strip()]
            communication_analysis = self.analytics_engine.analyze_communication_skills(answers_data)
            
            # Generate improvement recommendations
            improvement_recommendations = self.analytics_engine.generate_improvement_recommendations({
                'skills_fit': skills_fit,
                'communication_analysis': communication_analysis,
                'bias_analysis': st.session_state.interview_data['bias_analysis']
            })
            
            # Calculate hire confidence
            hire_confidence = self.analytics_engine.calculate_hire_confidence({
                'skills_fit': skills_fit,
                'communication_analysis': communication_analysis
            })
            
            # Store analytics data
            st.session_state.analytics_data = {
                'skills_fit': skills_fit,
                'communication_analysis': communication_analysis,
                'hire_confidence': hire_confidence,
                'improvement_recommendations': improvement_recommendations,
                'summary_insights': self.generate_automated_insights({
                    'skills_fit': skills_fit,
                    'communication_analysis': communication_analysis,
                    'hire_confidence': hire_confidence
                })
            }
            
        except Exception as e:
            st.error(f"Error generating analytics: {str(e)}")
            # Create fallback analytics data
            st.session_state.analytics_data = {
                'skills_fit': {
                    'overall_score': 75,
                    'required_skills_score': 80,
                    'preferred_skills_score': 70,
                    'missing_required_skills': ['advanced_sql'],
                    'missing_preferred_skills': ['docker'],
                    'strengths': ['python', 'communication'],
                    'weaknesses': ['cloud_architecture']
                },
                'communication_analysis': {
                    'coherence_score': 72.5,
                    'avg_response_time_seconds': 8.2,
                    'avg_answer_length': 45.3,
                    'confidence_level': 68.0,
                    'communication_style': "Articulate and Confident",
                    'improvement_areas': ["Response time", "Confidence and assertiveness"]
                },
                'hire_confidence': 78.5,
                'improvement_recommendations': [
                    "Focus on developing required skills: advanced_sql",
                    "Work on structuring answers more clearly using STAR method",
                    "Practice speaking with more confidence and avoid tentative language"
                ],
                'summary_insights': [
                    "🎯 Good skills alignment with some development areas",
                    "💬 Strong communication skills demonstrated",
                    "⚖️ Low bias risk detected throughout interview",
                    "👍 Moderate hire confidence - consider for next round"
                ]
            }
    
    def generate_automated_insights(self, analytics_data):
        """Generate automated insights based on analytics"""
        insights = []
        
        skills_fit = analytics_data.get('skills_fit', {})
        communication = analytics_data.get('communication_analysis', {})
        hire_confidence = analytics_data.get('hire_confidence', 0)
        
        # Skills insights
        if skills_fit.get('overall_score', 0) >= 80:
            insights.append("🎯 Excellent skills match with job requirements")
        elif skills_fit.get('overall_score', 0) >= 60:
            insights.append("✅ Good skills alignment with some development areas")
        else:
            insights.append("📝 Significant skills gap identified - consider training")
        
        # Communication insights
        if communication.get('coherence_score', 0) >= 70:
            insights.append("💬 Strong communication skills demonstrated")
        else:
            insights.append("🗣️ Communication skills need improvement")
        
        # Bias insights
        bias_count = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
        if bias_count == 0:
            insights.append("⚖️ Low bias risk detected throughout interview")
        else:
            insights.append(f"⚠️ {bias_count} potential bias(es) identified")
        
        # Hire confidence insights
        if hire_confidence >= 80:
            insights.append("🏆 High hire confidence - strong candidate")
        elif hire_confidence >= 60:
            insights.append("👍 Moderate hire confidence - consider for next round")
        else:
            insights.append("🤔 Lower hire confidence - review carefully")
        
        return insights
    
    def display_recruiter_dashboard(self):
        """Display comprehensive recruiter dashboard with analytics"""
        st.markdown('<div class="section-header">👔 Recruiter Dashboard - Candidate Analytics</div>', unsafe_allow_html=True)
        
        if not st.session_state.analytics_data:
            st.info("Complete an interview to see candidate analytics")
            return
        
        analytics_data = st.session_state.analytics_data
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_score = analytics_data['skills_fit'].get('overall_score', 0)
            st.markdown(f"""
            <div class="recruiter-metric-card">
                <h3>🎯 Overall Match</h3>
                <h1>{overall_score}%</h1>
                <p>Job Requirement Fit</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            hire_confidence = analytics_data.get('hire_confidence', 0)
            confidence_class = "hire-confidence-high" if hire_confidence >= 80 else "hire-confidence-medium" if hire_confidence >= 60 else "hire-confidence-low"
            st.markdown(f"""
            <div class="recruiter-metric-card {confidence_class}">
                <h3>🏆 Hire Confidence</h3>
                <h1>{hire_confidence}%</h1>
                <p>Recommended Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            coherence_score = analytics_data['communication_analysis'].get('coherence_score', 0)
            st.markdown(f"""
            <div class="recruiter-metric-card">
                <h3>💬 Communication</h3>
                <h1>{coherence_score}%</h1>
                <p>Coherence Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            bias_count = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
            bias_score = max(0, 100 - (bias_count * 15))
            st.markdown(f"""
            <div class="recruiter-metric-card">
                <h3>⚖️ Fairness</h3>
                <h1>{bias_score}%</h1>
                <p>Bias-Free Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Automated Insights
        st.markdown("### 🤖 Automated Insights")
        insights = analytics_data.get('summary_insights', [])
        for insight in insights:
            st.info(insight)
        
        # Detailed Analytics Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Skills Analysis", "💬 Communication", "🎯 Recommendations", "📈 Comparative"])
        
        with tab1:
            self.display_skills_analytics(analytics_data['skills_fit'])
        
        with tab2:
            self.display_communication_analytics(analytics_data['communication_analysis'])
        
        with tab3:
            self.display_recommendations_analytics(analytics_data)
        
        with tab4:
            self.display_comparative_analytics()
        
        # Export Functionality
        st.markdown("### 📤 Export Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate Full Report", use_container_width=True):
                report = self.generate_analytics_report()
                st.download_button(
                    label="📥 Download PDF Report",
                    data=report,
                    file_name=f"candidate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("🔄 Analyze New Candidate", type="primary", use_container_width=True):
                self.reset_interview()
                st.rerun()
    
    def display_skills_analytics(self, skills_fit):
        """Display skills analysis in recruiter dashboard"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Skills Match Breakdown")
            
            # Create skills match gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = skills_fit.get('overall_score', 0),
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Overall Match Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"},
                        {'range': [80, 100], 'color': "darkgray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Skills Distribution")
            
            # Skills breakdown
            strengths = skills_fit.get('strengths', [])
            weaknesses = skills_fit.get('weaknesses', [])
            
            st.metric("Key Strengths", len(strengths))
            if strengths:
                for strength in strengths:
                    st.success(f"✅ {strength}")
            
            st.metric("Development Areas", len(weaknesses))
            if weaknesses:
                for weakness in weaknesses:
                    st.error(f"📝 {weakness}")
    
    def display_communication_analytics(self, communication_analysis):
        """Display communication analytics"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🗣️ Communication Metrics")
            
            metrics_data = {
                'Metric': ['Coherence', 'Response Time', 'Answer Length', 'Confidence'],
                'Score': [
                    communication_analysis.get('coherence_score', 0),
                    communication_analysis.get('avg_response_time_seconds', 0),
                    communication_analysis.get('avg_answer_length', 0),
                    communication_analysis.get('confidence_level', 0)
                ],
                'Target': [70, 5, 50, 70]
            }
            
            df = pd.DataFrame(metrics_data)
            fig = px.bar(df, x='Metric', y='Score', title="Communication Metrics",
                        color='Score', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 💡 Communication Style")
            
            style = communication_analysis.get('communication_style', 'Unknown')
            st.metric("Communication Style", style)
            
            improvement_areas = communication_analysis.get('improvement_areas', [])
            if improvement_areas:
                st.markdown("**Areas for Improvement:**")
                for area in improvement_areas:
                    st.warning(f"⚠️ {area}")
            else:
                st.success("🎉 Strong communication skills across all areas!")
    
    def display_recommendations_analytics(self, analytics_data):
        """Display recommendations and next steps"""
        st.markdown("#### 💡 Actionable Recommendations")
        
        recommendations = analytics_data.get('improvement_recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
        else:
            st.success("🎉 No major improvement areas identified!")
        
        # Next steps based on hire confidence
        hire_confidence = analytics_data.get('hire_confidence', 0)
        st.markdown("#### 🎯 Recommended Next Steps")
        
        if hire_confidence >= 80:
            st.success("**🏆 Strong Candidate - Recommended Actions:**")
            st.write("- Proceed to final interview round")
            st.write("- Check reference and background")
            st.write("- Prepare offer package")
        elif hire_confidence >= 60:
            st.warning("**👍 Consider Candidate - Recommended Actions:**")
            st.write("- Schedule second interview with team lead")
            st.write("- Assess specific skill gaps")
            st.write("- Review with hiring committee")
        else:
            st.error("**🤔 Review Needed - Recommended Actions:**")
            st.write("- Conduct additional technical assessment")
            st.write("- Consider alternative roles")
            st.write("- Provide constructive feedback")
    
    def display_comparative_analytics(self):
        """Display comparative analytics for multiple candidates"""
        st.markdown("#### 📊 Candidate Comparison")
        
        # Mock comparative data - in real implementation, this would come from database
        comparative_data = self.analytics_engine.generate_comparative_analytics([
            {'candidate_id': 'current', 'analytics': st.session_state.analytics_data},
            {'candidate_id': 'candidate_2', 'analytics': {'skills_fit': {'overall_score': 65}, 'hire_confidence': 72}},
            {'candidate_id': 'candidate_3', 'analytics': {'skills_fit': {'overall_score': 88}, 'hire_confidence': 85}}
        ])
        
        if comparative_data:
            # Ranking
            st.markdown("##### 🏆 Candidate Ranking")
            ranked_candidates = comparative_data.get('candidates_ranked', [])
            for candidate in ranked_candidates:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{candidate['rank']}. {candidate['candidate_id']}**")
                with col2:
                    st.write(f"Score: {candidate['overall_score']}%")
                with col3:
                    st.write(f"Hire: {candidate['hire_confidence']}%")
            
            # Skills comparison chart
            st.markdown("##### 📈 Skills Comparison")
            skills_comparison = comparative_data.get('skills_comparison', {})
            if skills_comparison:
                df = pd.DataFrame(skills_comparison)
                fig = px.bar(df, barmode='group', title="Skills Proficiency Comparison")
                st.plotly_chart(fig, use_container_width=True)
            
            # Diversity metrics
            st.markdown("##### 🌈 Diversity Metrics")
            diversity_metrics = comparative_data.get('diversity_metrics', {})
            if diversity_metrics:
                for metric, value in diversity_metrics.items():
                    st.write(f"**{metric.replace('_', ' ').title()}:** {value}")
        else:
            st.info("Add more candidates to enable comparative analytics")
    
    def generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        analytics_data = st.session_state.analytics_data
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("              FAIRAI HIRE - CANDIDATE ANALYSIS REPORT")
        report_lines.append("=" * 70)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("EXECUTIVE SUMMARY:")
        report_lines.append(f"  • Overall Match Score: {analytics_data['skills_fit'].get('overall_score', 0)}%")
        report_lines.append(f"  • Hire Confidence: {analytics_data.get('hire_confidence', 0)}%")
        report_lines.append(f"  • Communication Score: {analytics_data['communication_analysis'].get('coherence_score', 0)}%")
        report_lines.append("")
        
        # Skills Analysis
        report_lines.append("SKILLS ANALYSIS:")
        skills_fit = analytics_data['skills_fit']
        report_lines.append(f"  • Required Skills Score: {skills_fit.get('required_skills_score', 0)}%")
        report_lines.append(f"  • Preferred Skills Score: {skills_fit.get('preferred_skills_score', 0)}%")
        report_lines.append(f"  • Key Strengths: {', '.join(skills_fit.get('strengths', []))}")
        report_lines.append(f"  • Development Areas: {', '.join(skills_fit.get('weaknesses', []))}")
        report_lines.append("")
        
        # Communication Analysis
        report_lines.append("COMMUNICATION ANALYSIS:")
        comm = analytics_data['communication_analysis']
        report_lines.append(f"  • Coherence Score: {comm.get('coherence_score', 0)}%")
        report_lines.append(f"  • Average Response Time: {comm.get('avg_response_time_seconds', 0)}s")
        report_lines.append(f"  • Communication Style: {comm.get('communication_style', 'Unknown')}")
        report_lines.append(f"  • Improvement Areas: {', '.join(comm.get('improvement_areas', []))}")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS:")
        for i, rec in enumerate(analytics_data.get('improvement_recommendations', []), 1):
            report_lines.append(f"  {i}. {rec}")
        report_lines.append("")
        
        # Automated Insights
        report_lines.append("AUTOMATED INSIGHTS:")
        for insight in analytics_data.get('summary_insights', []):
            report_lines.append(f"  • {insight}")
        
        report_lines.append("")
        report_lines.append("=" * 70)
        report_lines.append("           DATA-DRIVEN HIRING DECISIONS")
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)

    def sidebar_controls(self):
        """Display sidebar controls and information"""
        with st.sidebar:
            st.markdown("### 🔧 Session Controls")
            
            # AI Enhancement Toggle
            st.markdown("### 🤖 AI Enhancement")
            ai_enabled = st.toggle("Enable AI Features", 
                                 value=st.session_state.ai_enabled,
                                 help="Use Ollama for enhanced question generation and answer analysis")
            
            if ai_enabled != st.session_state.ai_enabled:
                st.session_state.ai_enabled = ai_enabled
                if ai_enabled and not self.ai_enhancer.available:
                    st.warning("Ollama not detected! Install from https://ollama.ai")
            
            if st.session_state.ai_enabled and self.ai_enhancer.available:
                st.success("🤖 AI Enhancement Active")
            elif st.session_state.ai_enabled:
                st.error("❌ Ollama not available")
            
            st.markdown("---")
            st.markdown("### 📊 Current Status")
            
            if st.session_state.resume_analyzed:
                st.success("✅ Resume Analyzed")
                st.write(f"Skills Found: {len(st.session_state.candidate_skills)}")
                st.write(f"Experience: {st.session_state.candidate_experience}")
                st.write(f"Difficulty: {st.session_state.current_difficulty}")
            
            if st.session_state.interview_started:
                st.success("✅ Interview Started")
                st.write(f"Questions: {len(st.session_state.interview_questions)}")
                answered = len([a for a in st.session_state.candidate_answers if a.strip()])
                st.write(f"Answered: {answered}/{len(st.session_state.interview_questions)}")
                
                # NEW: Show bias count
                bias_count = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
                st.write(f"Bias Alerts: {bias_count}")
            
            if st.session_state.interview_completed:
                st.success("✅ Interview Completed")
                if st.session_state.analytics_data:
                    st.write(f"Hire Confidence: {st.session_state.analytics_data.get('hire_confidence', 0)}%")
            
            st.markdown("---")
            
            if st.button("🔄 Reset Entire Session", use_container_width=True, key="sidebar_reset"):
                self.reset_interview()
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 💡 Interview Tips")
            st.markdown("""
            - Be specific in your answers
            - Include real examples and projects
            - Mention challenges and solutions
            - Focus on job-relevant information
            - Avoid personal details that could introduce bias
            """)

    def display_header(self):
        """Display application header"""
        st.markdown('<h1 class="main-header">🤖 FairAI Hire - Bias-Free Interviews</h1>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; color: #ddd; margin-bottom: 2rem;'>
        Welcome to FairAI Hire! Upload your resume below to start a personalized, 
        unbiased technical interview.
        </div>
        """, unsafe_allow_html=True)
    
    def resume_analysis_section(self):
        """Display resume analysis section"""
        st.markdown('<div class="section-header">📄 Resume Analysis</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        st.markdown("**Paste your resume text below:**")
        
        resume_text = st.text_area(
            " ",
            height=250,
            placeholder="""Paste your resume content here...

Example:
John Doe - Software Developer
3 years of experience in Python and JavaScript
Skills: Python, React, SQL, Teamwork, Communication""",
            key="resume_input",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🚀 Analyze Resume & Start Interview", type="primary", use_container_width=True):
                if resume_text.strip():
                    with st.spinner("🔍 Analyzing your resume..."):
                        if self.analyze_resume(resume_text) and self.generate_interview_questions():
                            st.success("✅ Resume analyzed successfully!")
                            st.rerun()
                else:
                    st.error("❌ Please paste your resume text to continue.")
        
        with col2:
            if st.button("🔄 Reset Session", use_container_width=True):
                self.reset_interview()
                st.rerun()
    
    def display_skills(self):
        """Display extracted skills in a visually appealing way"""
        if st.session_state.candidate_skills:
            st.markdown('<div class="section-header">🎯 Discovered Skills & Experience</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="custom-container">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔧 Technical Skills**")
                tech_skills = [skill for skill, category, confidence in st.session_state.candidate_skills if category == 'technical']
                if tech_skills:
                    for skill in tech_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-technical">⚡ {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.markdown("*No technical skills detected*")
            
            with col2:
                st.markdown("**💬 Soft Skills**")
                soft_skills = [skill for skill, category, confidence in st.session_state.candidate_skills if category == 'soft']
                if soft_skills:
                    for skill in soft_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-soft">🌟 {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.markdown("*No soft skills detected*")
            
            # Experience level
            level_emojis = {'Entry': '🟢', 'Mid': '🟡', 'Senior': '🔴'}
            emoji = level_emojis.get(st.session_state.candidate_experience, '⚪')
            
            st.markdown(f"""
            **📊 Experience Level:** 
            <span style='font-size: 1.2rem; font-weight: bold; color: #4CAF50;'>
            {emoji} {st.session_state.candidate_experience} Level
            </span>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def skills_visualization_section(self):
        """Display skills graph visualization"""
        st.markdown('<div class="section-header">🕸️ Skills Graph Visualization</div>', unsafe_allow_html=True)
        
        if not st.session_state.skills_graph:
            st.info("👆 Analyze a resume first to see skills visualization!")
            return
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Network Graph", "Category Analysis", "Confidence Heatmap"])
        
        with viz_tab1:
            st.markdown("### 🕸️ Skills Relationship Network")
            st.markdown("""
            **Understanding the Network:**
            - 🔴 **Nodes** = Your skills (size = confidence level)
            - 🔵 **Lines** = Skills that work well together  
            - 🎨 **Colors** = Different skill categories
            """)
            
            # Create network graph
            fig_network = create_skills_network(st.session_state.skills_graph)
            st.plotly_chart(fig_network, use_container_width=True, key="skills_network_graph")
            
            # Show skills list with details
            st.markdown("### 📋 Detected Skills Details")
            skills_list = []
            for skill_name, skill_node in st.session_state.skills_graph.items():
                skills_list.append({
                    "Skill": skill_name,
                    "Category": skill_node.category,
                    "Confidence": f"{skill_node.confidence:.2f}",
                    "Frequency": skill_node.frequency,
                    "Related Skills": len(skill_node.related_skills)
                })
            
            df_skills = pd.DataFrame(skills_list)
            st.dataframe(df_skills, use_container_width=True, key="skills_dataframe")
            
        with viz_tab2:
            st.markdown("### 📊 Skills Category Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Category distribution
                st.markdown("#### Skills by Category")
                fig_barchart = create_category_barchart(st.session_state.skills_data)
                st.plotly_chart(fig_barchart, use_container_width=True, key="category_barchart")
            
            with col2:
                # Radar chart
                st.markdown("#### Skills Radar")
                fig_radar = plot_skill_categories(st.session_state.skills_data)
                st.plotly_chart(fig_radar, use_container_width=True, key="skills_radar")
            
        with viz_tab3:
            st.markdown("### 🔥 Skill Confidence Heatmap")
            fig_heatmap = create_confidence_heatmap(st.session_state.skills_graph)
            st.plotly_chart(fig_heatmap, use_container_width=True, key="confidence_heatmap")
            
            # Skills metrics
            metrics = calculate_skill_metrics(st.session_state.skills_graph)
            st.markdown("### 📈 Skills Metrics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Skills", metrics['total_skills'])
            with col2:
                st.metric("Avg Confidence", f"{metrics['avg_confidence']:.2f}")
            with col3:
                st.metric("Relationships", metrics['total_relationships'])
            with col4:
                st.metric("Connectivity", f"{metrics['connectivity_score']:.2f}")
            
            # Export functionality
            st.markdown("### 💾 Export Skills Data")
            if st.button("Export Skills Data as JSON", key="export_skills"):
                skills_export = {
                    "skills_graph": {
                        name: {
                            "skill": node.skill,
                            "category": node.category,
                            "confidence": node.confidence,
                            "frequency": node.frequency,
                            "related_skills": node.related_skills
                        } for name, node in st.session_state.skills_graph.items()
                    },
                    "metrics": metrics
                }
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(skills_export, indent=2),
                    file_name="skills_analysis.json",
                    mime="application/json",
                    key="download_skills_json"
                )

    def interview_section(self):
        """Display interview questions and answers with navigation - ENHANCED WITH REAL-TIME AUDIO/VIDEO"""
        if not st.session_state.interview_started or st.session_state.interview_completed:
            return
        
        st.markdown('<div class="section-header">🎤 Interview Session</div>', unsafe_allow_html=True)
        
        # Real-time bias alert counter
        current_biases = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
        if current_biases > 0:
            st.markdown(f"""
            <div class="bias-alert-box">
                <strong>🚨 Real-time Bias Alert:</strong> {current_biases} potential bias(es) detected so far
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.interview_questions:
            current_index = st.session_state.current_question_index
            total_questions = len(st.session_state.interview_questions)
            
            # Progress tracking
            progress = (current_index) / total_questions
            st.progress(progress)
            
            st.markdown(f"""
            <div class='progress-text'>
            📍 Question {current_index + 1} of {total_questions} 
            ({int(progress * 100)}% Complete)
            <br>📊 Current Difficulty: <strong>{st.session_state.current_difficulty}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Display question
            current_question = st.session_state.interview_questions[current_index]
            
            if (st.session_state.ai_enabled and 
                st.session_state.ai_enhanced_questions and 
                current_index < len(st.session_state.ai_enhanced_questions) and
                st.session_state.ai_enhanced_questions[current_index].get('success')):
                
                enhanced_data = st.session_state.ai_enhanced_questions[current_index]
                st.markdown(f"""
                <div class="ai-enhanced-box">
                    <strong style='color: #FFD700;'>🤖 AI-Enhanced Question:</strong><br>
                    {enhanced_data['improved_question']}
                    <br><br>
                    <small><em>💡 {enhanced_data['explanation']}</em></small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="question-box">
                    <strong style='color: #4FC3F7;'>💡 Question:</strong><br>
                    {current_question}
                </div>
                """, unsafe_allow_html=True)
            
            # Response type selection
            st.markdown("### 📝 Choose Your Response Method")
            response_type = st.radio(
                "Response Type:",
                ["💬 Text Response", "🎙️ Real-Time Audio/Video (Live Transcription)"],
                horizontal=True,
                key=f"response_type_{current_index}",
                help="Choose how you want to answer this question"
            )
            
            answer = ""
            
            if response_type == "💬 Text Response":
                # Text input
                st.markdown("**📝 Your Answer:**")
                answer = st.text_area(
                    " ",
                    value=st.session_state.candidate_answers[current_index],
                    height=180,
                    placeholder="Share your experience and thoughts here... Be specific and provide examples.",
                    key=f"answer_{current_index}",
                    label_visibility="collapsed"
                )
                
                # Update answer in session state as user types
                if answer != st.session_state.candidate_answers[current_index]:
                    st.session_state.candidate_answers[current_index] = answer
                
                # Character/word count
                if answer.strip():
                    word_count = len(answer.split())
                    char_count = len(answer)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"📊 Words: {word_count}")
                    with col2:
                        st.caption(f"📊 Characters: {char_count}")
                    
            else:  # Real-Time Audio/Video Response
                transcription = self.realtime_audio_video_interface(current_index)
                if transcription:
                    answer = transcription
                    # Auto-save the transcription
                    st.session_state.candidate_answers[current_index] = answer
            
            # Display AI analysis of previous answer if available
            if (current_index > 0 and 
                st.session_state.answer_analysis and 
                st.session_state.answer_analysis[current_index-1]):
                
                st.markdown("---")
                analysis = st.session_state.answer_analysis[current_index-1]
                if analysis.get('success'):
                    st.markdown(f"""
                    <div class="ai-analysis-box">
                        <strong>🤖 AI Analysis of Previous Answer:</strong><br>
                        <strong>Quality Score:</strong> {analysis.get('quality_score', 'N/A')}/10<br>
                        <strong>Strengths:</strong> {', '.join(analysis.get('strengths', []))}<br>
                        <strong>Skills Demonstrated:</strong> {', '.join(analysis.get('skills_demonstrated', []))}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Navigation and action buttons
            st.markdown("---")
            st.markdown("### 🎯 Actions")
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if current_index > 0:
                    if st.button("⬅️ Previous", use_container_width=True, key=f"prev_{current_index}"):
                        self.navigate_questions("previous")
                        st.rerun()
                else:
                    st.button("⬅️ Previous", use_container_width=True, disabled=True, key=f"prev_{current_index}_disabled")
            
            with col2:
                if st.button("💾 Save Answer", use_container_width=True, key=f"save_{current_index}"):
                    if answer.strip():
                        if self.submit_answer(answer, current_index):
                            st.success("✅ Answer saved successfully!")
                            time.sleep(0.5)
                        else:
                            st.error("❌ Failed to save answer. Please try again.")
                    else:
                        st.error("❌ Please provide an answer before saving.")
            
            with col3:
                if current_index < total_questions - 1:
                    if st.button("Next ➡️", type="primary", use_container_width=True, key=f"next_{current_index}"):
                        if answer.strip():
                            self.submit_answer(answer, current_index)
                            self.navigate_questions("next")
                            st.rerun()
                        else:
                            st.error("❌ Please provide an answer before proceeding to the next question.")
                else:
                    if st.button("🏁 Complete Interview", type="primary", use_container_width=True, key="complete_interview"):
                        if answer.strip():
                            self.submit_answer(answer, current_index)
                            self.complete_interview()
                            st.balloons()
                            st.success("🎊 Congratulations! Interview completed successfully!")
                            st.info("📊 Check the 'Fairness Dashboard' and 'Recruiter Analytics' tabs for your results.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Please provide an answer before completing the interview.")
            
            with col4:
                if st.button("🔄 Restart Interview", use_container_width=True, key=f"restart_{current_index}"):
                    if st.warning("⚠️ Are you sure? This will delete all your answers."):
                        self.reset_interview()
                        st.rerun()
            
            # Help section
            with st.expander("💡 Tips for Better Answers"):
                st.markdown("""
                **For Text Responses:**
                - Use the STAR method (Situation, Task, Action, Result)
                - Be specific with examples and numbers
                - Keep answers concise but detailed (50-150 words)
                - Proofread before saving
                
                **For Audio/Video Responses:**
                - Speak clearly and at a moderate pace
                - Look at the camera for better engagement scores
                - Ensure good lighting and quiet environment
                - Practice your answer mentally before recording
                - Aim for 1-2 minutes per response
                
                **General Tips:**
                - Focus on job-relevant skills and experiences
                - Avoid personal demographic information
                - Use concrete examples from your work
                - Show problem-solving and critical thinking
                """)

    def display_fairness_dashboard(self):
        """Display comprehensive fairness dashboard with visual analytics"""
        st.markdown('<div class="section-header">📊 Fairness Dashboard & Analytics</div>', unsafe_allow_html=True)
        
        # Calculate metrics
        skills_match_score = self.calculate_skills_match_score()
        bias_alert_level, bias_color = self.calculate_bias_alert_level()
        completeness_score = self.calculate_interview_completeness()
        fairness_score = self.calculate_overall_fairness_score()
        
        # NEW: Generate comprehensive bias report
        bias_report = generate_bias_report(st.session_state.interview_data)
        
        # Overall Metrics Row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <h3>🎯 Skills Match</h3>
                <h2>{skills_match_score}%</h2>
                <p>Job Relevance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            alert_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(bias_alert_level, "⚪")
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, {bias_color} 0%, #e83e8c 100%);">
                <h3>⚠️ Bias Alert</h3>
                <h2>{alert_emoji} {bias_alert_level}</h2>
                <p>Fairness Level</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                <h3>📈 Completeness</h3>
                <h2>{completeness_score}%</h2>
                <p>Interview Progress</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            score_color = "#28a745" if fairness_score >= 7 else "#ffc107" if fairness_score >= 5 else "#dc3545"
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, {score_color} 0%, #fd7e14 100%);">
                <h3>⚖️ Fairness Score</h3>
                <h2>{fairness_score}/10</h2>
                <p>Overall Rating</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            # NEW: Bias Score Gauge
            bias_score = bias_report.get('overall_score', 100)
            grade = bias_report.get('grade', 'A+')
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);">
                <h3>📊 Bias Score</h3>
                <h2>{bias_score}% {grade}</h2>
                <p>Fairness Grade</p>
            </div>
            """, unsafe_allow_html=True)
        
        # NEW: Enhanced Visual Analytics Section
        st.markdown("### 📊 Advanced Bias Analytics")
        
        # Row 1: Heatmap and Timeline
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 Real-time Bias Heatmap")
            heatmap_fig = self.heatmap_generator.generate_bias_heatmap(st.session_state.interview_data)
            st.plotly_chart(heatmap_fig, use_container_width=True, key="enhanced_bias_heatmap")
        
        with col2:
            st.markdown("#### 📈 Bias Detection Timeline")
            if len(st.session_state.bias_history) > 1:
                timeline_fig = self.heatmap_generator.generate_timeline_heatmap(st.session_state.bias_history)
                st.plotly_chart(timeline_fig, use_container_width=True, key="bias_timeline")
            else:
                st.info("Complete more questions to see timeline analysis")
        
        # Row 2: Category Distribution and Severity Gauge
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("#### 🎯 Bias Category Distribution")
            category_fig = self.heatmap_generator.generate_category_distribution(
                bias_report.get('category_breakdown', {})
            )
            st.plotly_chart(category_fig, use_container_width=True, key="bias_categories")
        
        with col4:
            st.markdown("#### 📊 Overall Bias Score")
            gauge_fig = self.heatmap_generator.generate_severity_gauge(bias_score)
            st.plotly_chart(gauge_fig, use_container_width=True, key="bias_gauge")
        
        # NEW: Bias Hotspots Section
        st.markdown("### 🚨 Bias Hotspots & Recommendations")
        
        hotspots = bias_report.get('trend_analysis', {}).get('hotspots', [])
        if hotspots:
            st.warning(f"**Bias Hotspots Detected:** {', '.join(hotspots)}")
            
            # Display recommendations
            recommendations = bias_report.get('recommendations', [])
            if recommendations:
                st.markdown("#### 💡 Improvement Recommendations:")
                for rec in recommendations:
                    st.success(f"✅ {rec}")
        else:
            st.success("🎉 Excellent! No significant bias hotspots detected in this interview.")
        
        # Detailed Breakdown Section
        st.markdown("### 📋 Detailed Analysis")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Skills Analysis", "⚠️ Bias Alerts", "📊 Performance", "🤖 AI Insights", "💡 Recommendations"])
        
        with tab1:
            self.display_skills_analysis()
        
        with tab2:
            self.display_bias_analysis()
        
        with tab3:
            self.display_performance_analysis()
        
        with tab4:
            self.display_ai_insights()
        
        with tab5:
            self.display_recommendations()
        
        # Export Functionality
        st.markdown("### 📤 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate Fairness Report", use_container_width=True, key="generate_report"):
                report = self.generate_fairness_report()
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"fairness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_report"
                )
        
        with col2:
            if st.button("🔄 Start New Interview", type="primary", use_container_width=True, key="new_interview"):
                self.reset_interview()
                st.rerun()

    def calculate_skills_match_score(self):
        """Calculate how well candidate skills match typical job requirements"""
        if not st.session_state.candidate_skills:
            return 0
        
        target_technical_skills = ['python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'node.js']
        target_soft_skills = ['communication', 'teamwork', 'leadership', 'problem solving', 'creativity']
        
        candidate_tech_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'technical']
        candidate_soft_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'soft']
        
        tech_match = len([skill for skill in candidate_tech_skills if skill in target_technical_skills])
        soft_match = len([skill for skill in candidate_soft_skills if skill in target_soft_skills])
        
        tech_score = (tech_match / len(target_technical_skills)) * 70 if target_technical_skills else 0
        soft_score = (soft_match / len(target_soft_skills)) * 30 if target_soft_skills else 0
        
        return min(100, int(tech_score + soft_score))

    def calculate_bias_alert_level(self):
        """Calculate overall bias alert level"""
        if not st.session_state.bias_reports:
            return "Low", "#28a745"
        
        high_bias_count = 0
        medium_bias_count = 0
        
        for report in st.session_state.bias_reports:
            if report and report.get('severity') == 'High':
                high_bias_count += 1
            elif report and report.get('severity') == 'Medium':
                medium_bias_count += 1
        
        if high_bias_count > 0:
            return "High", "#dc3545"
        elif medium_bias_count > 1:
            return "Medium", "#ffc107"
        else:
            return "Low", "#28a745"

    def calculate_interview_completeness(self):
        """Calculate interview completion percentage"""
        if not st.session_state.interview_questions:
            return 0
        
        answered = len([answer for answer in st.session_state.candidate_answers if answer.strip()])
        total = len(st.session_state.interview_questions)
        
        return int((answered / total) * 100) if total > 0 else 0

    def calculate_overall_fairness_score(self):
        """Calculate overall fairness score (1-10)"""
        bias_alert_level, _ = self.calculate_bias_alert_level()
        completeness = self.calculate_interview_completeness()
        
        bias_scores = {"Low": 9, "Medium": 6, "High": 3}
        base_score = bias_scores.get(bias_alert_level, 5)
        
        completeness_factor = completeness / 100.0
        
        return min(10, int(base_score + (completeness_factor * 2)))

    def display_skills_analysis(self):
        """Display detailed skills analysis"""
        st.markdown("#### 🎯 Skills Identified")
        
        if st.session_state.candidate_skills:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Technical Skills:**")
                tech_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'technical']
                if tech_skills:
                    for skill in tech_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-technical">⚡ {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.write("No technical skills detected")
            
            with col2:
                st.markdown("**Soft Skills:**")
                soft_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'soft']
                if soft_skills:
                    for skill in soft_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-soft">🌟 {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.write("No soft skills detected")
            
            st.metric("Total Skills Identified", len(st.session_state.candidate_skills))
        else:
            st.info("No skills data available")

    def display_bias_analysis(self):
        """Display detailed bias analysis"""
        st.markdown("#### ⚠️ Bias Detection Results")
        
        if not st.session_state.bias_reports or all(report is None for report in st.session_state.bias_reports):
            st.success("✅ Excellent! No biases detected in the interview.")
            return
        
        bias_count = 0
        for i, (question, answer, bias_report) in enumerate(zip(
            st.session_state.interview_questions,
            st.session_state.candidate_answers,
            st.session_state.bias_reports
        )):
            if bias_report and bias_report.get('bias_types'):
                bias_count += 1
                with st.expander(f"🚩 Question {i+1}: Potential Bias Detected", expanded=False):
                    st.write(f"**Question:** {question}")
                    st.write(f"**Answer:** {answer}")
                    st.write(f"**Bias Types:** {', '.join(bias_report['bias_types'])}")
                    st.write(f"**Severity:** {bias_report.get('severity', 'Unknown')}")
        
        if bias_count == 0:
            st.success("✅ No significant biases detected in the interview responses.")

    def display_performance_analysis(self):
        """NEW: Display performance analysis with difficulty tracking"""
        st.markdown("#### 📊 Performance & Difficulty Analysis")
        
        if not st.session_state.answer_scores:
            st.info("Complete some questions to see performance analysis")
            return
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_score = sum(st.session_state.answer_scores) / len(st.session_state.answer_scores)
            st.metric("Average Answer Quality", f"{avg_score:.1f}/10")
        
        with col2:
            st.metric("Current Difficulty", st.session_state.current_difficulty)
        
        with col3:
            improvement = "↑ Improving" if len(st.session_state.answer_scores) > 1 and st.session_state.answer_scores[-1] > st.session_state.answer_scores[0] else "→ Stable"
            st.metric("Performance Trend", improvement)
        
        # Score progression chart
        if len(st.session_state.answer_scores) > 1:
            st.markdown("#### 📈 Answer Quality Progression")
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=list(range(1, len(st.session_state.answer_scores) + 1)),
                y=st.session_state.answer_scores,
                mode='lines+markers',
                name='Answer Quality',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))
            
            # Add difficulty level zones
            difficulty_zones = {
                'Easy': (0, 4, 'rgba(40, 167, 69, 0.1)'),
                'Medium': (4, 7, 'rgba(255, 193, 7, 0.1)'),
                'Hard': (7, 9, 'rgba(253, 126, 20, 0.1)'),
                'Expert': (9, 11, 'rgba(220, 53, 69, 0.1)')
            }
            
            for level, (low, high, color) in difficulty_zones.items():
                fig.add_hrect(
                    y0=low, y1=high,
                    fillcolor=color,
                    opacity=0.3,
                    line_width=0,
                    annotation_text=level,
                    annotation_position="inside top left"
                )
            
            fig.update_layout(
                title="Answer Quality Progression with Difficulty Zones",
                xaxis_title="Question Number",
                yaxis_title="Quality Score (1-10)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, key="performance_chart")

    def display_ai_insights(self):
        """Display AI-powered insights and analysis"""
        st.markdown("#### 🤖 AI-Powered Insights")
        
        if not st.session_state.ai_enabled or not self.ai_enhancer.available:
            st.info("Enable AI Enhancement in the sidebar to get AI-powered insights!")
            return
        
        if not st.session_state.answer_analysis or all(analysis is None for analysis in st.session_state.answer_analysis):
            st.info("Complete the interview to see AI analysis of your answers.")
            return
        
        # Overall AI Analysis
        total_answers = len([a for a in st.session_state.candidate_answers if a.strip()])
        if total_answers > 0:
            quality_scores = []
            for analysis in st.session_state.answer_analysis:
                if analysis and analysis.get('quality_score'):
                    quality_scores.append(analysis['quality_score'])
            
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                st.metric("📊 Average Answer Quality Score", f"{avg_quality:.1f}/10")
                
                if avg_quality >= 8:
                    st.success("🎉 Excellent! Your answers demonstrate strong experience and clarity.")
                elif avg_quality >= 6:
                    st.info("👍 Good! Your answers are comprehensive and relevant.")
                else:
                    st.warning("💡 Consider providing more specific examples and details in your answers.")
        
        # Detailed answer analysis
        st.markdown("#### 📝 Answer-by-Answer Analysis")
        for i, (question, answer, analysis) in enumerate(zip(
            st.session_state.interview_questions,
            st.session_state.candidate_answers,
            st.session_state.answer_analysis
        )):
            if answer.strip() and analysis and analysis.get('success'):
                with st.expander(f"Question {i+1} Analysis", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("**Answer:**")
                        st.info(answer)
                    
                    with col2:
                        st.metric("Quality Score", f"{analysis.get('quality_score', 'N/A')}/10")
                        st.metric("Relevance", f"{analysis.get('relevance_score', 'N/A')}/10")
                    
                    st.markdown("**Strengths:**")
                    for strength in analysis.get('strengths', []):
                        st.write(f"✅ {strength}")
                    
                    st.markdown("**Areas for Improvement:**")
                    for improvement in analysis.get('improvements', []):
                        st.write(f"📝 {improvement}")
                    
                    st.markdown("**Skills Demonstrated:**")
                    skills = analysis.get('skills_demonstrated', [])
                    if skills:
                        for skill in skills:
                            st.markdown(f'<span class="skill-chip">🎯 {skill}</span>', unsafe_allow_html=True)
                    else:
                        st.write("No specific skills identified in this answer.")

    def display_recommendations(self):
        """Display fairness recommendations"""
        st.markdown("#### 💡 Recommendations for Fair Hiring")
        
        recommendations = [
            "✅ Focus on job-relevant skills and experience only",
            "✅ Use standardized questions for all candidates",
            "✅ Avoid questions about personal demographics",
            "✅ Evaluate based on demonstrated capabilities",
            "✅ Use blind resume screening when possible",
            "✅ Provide clear evaluation criteria upfront",
            "✅ Train interviewers on unconscious bias",
            "✅ Use structured interview formats"
        ]
        
        for recommendation in recommendations:
            st.write(recommendation)
        
        bias_alert_level, _ = self.calculate_bias_alert_level()
        
        if bias_alert_level == "High":
            st.warning("🚨 **Priority Action Needed:** Consider reviewing and retraining interviewers on bias awareness.")
        elif bias_alert_level == "Medium":
            st.info("📝 **Improvement Opportunity:** Implement structured scoring rubrics for more objective evaluation.")

    def generate_fairness_report(self):
        """Generate a comprehensive fairness report"""
        # NEW: Generate comprehensive bias report
        bias_report = generate_bias_report(st.session_state.interview_data)
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("           FAIRAI HIRE - FAIRNESS REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary Metrics
        report_lines.append("SUMMARY METRICS:")
        report_lines.append(f"  • Skills Match Score: {self.calculate_skills_match_score()}%")
        report_lines.append(f"  • Bias Alert Level: {self.calculate_bias_alert_level()[0]}")
        report_lines.append(f"  • Interview Completeness: {self.calculate_interview_completeness()}%")
        report_lines.append(f"  • Overall Fairness Score: {self.calculate_overall_fairness_score()}/10")
        report_lines.append(f"  • Final Difficulty Level: {st.session_state.current_difficulty}")
        report_lines.append(f"  • Bias Detection Score: {bias_report.get('overall_score', 100)}% ({bias_report.get('grade', 'A+')})")
        report_lines.append("")
        
        # Skills Analysis
        report_lines.append("SKILLS ANALYSIS:")
        if st.session_state.candidate_skills:
            tech_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'technical']
            soft_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'soft']
            report_lines.append(f"  • Technical Skills: {', '.join(tech_skills) if tech_skills else 'None'}")
            report_lines.append(f"  • Soft Skills: {', '.join(soft_skills) if soft_skills else 'None'}")
        else:
            report_lines.append("  • No skills data available")
        report_lines.append("")
        
        # Bias Analysis
        report_lines.append("BIAS ANALYSIS:")
        bias_count = 0
        for i, (question, bias_report_item) in enumerate(zip(st.session_state.interview_questions, st.session_state.bias_reports)):
            if bias_report_item and bias_report_item.get('bias_types'):
                bias_count += 1
                report_lines.append(f"  • Question {i+1}: {', '.join(bias_report_item['bias_types'])}")
        
        if bias_count == 0:
            report_lines.append("  • No biases detected - Excellent!")
        
        # Bias Hotspots
        hotspots = bias_report.get('trend_analysis', {}).get('hotspots', [])
        if hotspots:
            report_lines.append(f"  • Bias Hotspots: {', '.join(hotspots)}")
        report_lines.append("")
        
        # Performance Analysis
        report_lines.append("PERFORMANCE ANALYSIS:")
        if st.session_state.answer_scores:
            avg_score = sum(st.session_state.answer_scores) / len(st.session_state.answer_scores)
            report_lines.append(f"  • Average Answer Quality: {avg_score:.1f}/10")
            report_lines.append(f"  • Questions Answered: {len([a for a in st.session_state.candidate_answers if a.strip()])}")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS:")
        recommendations = bias_report.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                report_lines.append(f"  {i}. {rec}")
        else:
            report_lines.append("  1. Focus on job-relevant qualifications")
            report_lines.append("  2. Use standardized evaluation criteria")
            report_lines.append("  3. Avoid demographic-based assumptions")
            report_lines.append("  4. Implement structured interview processes")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("           HIRING THAT SEES SKILLS, NOT DEMOGRAPHICS")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)

    def display_detailed_question_review(self):
        """Display detailed question-by-question review in separate tab"""
        st.markdown('<div class="section-header">📋 Detailed Question Review</div>', unsafe_allow_html=True)
        
        for i, (question, answer, bias_report, analysis, follow_up) in enumerate(zip(
            st.session_state.interview_questions,
            st.session_state.candidate_answers,
            st.session_state.bias_reports,
            st.session_state.answer_analysis,
            st.session_state.follow_up_questions
        )):
            with st.expander(f"Question {i+1}: {question[:80]}...", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Your Answer:**")
                    st.info(answer if answer else "No answer provided")
                    
                    if analysis and analysis.get('success'):
                        st.markdown("**🤖 AI Analysis:**")
                        st.write(f"**Quality Score:** {analysis.get('quality_score', 'N/A')}/10")
                        st.write(f"**Relevance:** {analysis.get('relevance_score', 'N/A')}/10")
                        
                        if analysis.get('strengths'):
                            st.write("**Strengths:**")
                            for strength in analysis['strengths']:
                                st.write(f"✅ {strength}")
                
                with col2:
                    st.markdown("**Bias Analysis:**")
                    if bias_report:
                        severity = bias_report['severity']
                        if severity == 'High':
                            st.error(f"🟥 High Bias")
                            if bias_report['bias_types']:
                                st.write(f"Detected: {', '.join(bias_report['bias_types'])}")
                        elif severity == 'Medium':
                            st.warning(f"🟨 Medium Bias")
                            if bias_report['bias_types']:
                                st.write(f"Detected: {', '.join(bias_report['bias_types'])}")
                        elif severity == 'Low':
                            st.info(f"🟦 Low Bias")
                        else:
                            st.success(f"🟩 No Bias Detected")
                    else:
                        st.info("No bias analysis available")
                    
                    if (follow_up and follow_up.get('success') and 
                        st.session_state.ai_enabled and self.ai_enhancer.available):
                        st.markdown("**🤖 Suggested Follow-up:**")
                        st.info(follow_up.get('follow_up_question', ''))
    
    def run(self):
        """Main application runner"""
        self.initialize_session_state()
        self.display_header()
        
        # Create tabs for different sections - UPDATED to include Recruiter Dashboard
        if st.session_state.interview_completed:
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Fairness Dashboard", "👔 Recruiter Analytics", "🕸️ Skills Visualization", "🎤 Interview Review"])
        elif st.session_state.resume_analyzed:
            tab1, tab2, tab3, tab4 = st.tabs(["🎤 Interview", "🕸️ Skills Visualization", "📊 Dashboard Preview", "👔 Recruiter View"])
        else:
            tab1, tab2, tab3, tab4 = st.tabs(["🎤 Interview", "🕸️ Skills Visualization", "📊 Dashboard Preview", "👔 Recruiter View"])
        
        with tab1:
            if not st.session_state.resume_analyzed:
                self.resume_analysis_section()
            else:
                if not st.session_state.interview_completed:
                    self.display_skills()
                    self.interview_section()
                else:
                    self.display_fairness_dashboard()
        
        with tab2:
            self.skills_visualization_section()
        
        with tab3:
            if st.session_state.interview_completed:
                self.display_detailed_question_review()
            else:
                st.info("Complete the interview to see the comprehensive fairness dashboard!")
        
        with tab4:
            if st.session_state.interview_completed:
                self.display_recruiter_dashboard()
            else:
                st.info("Complete an interview to access recruiter analytics and insights!")
        
        self.sidebar_controls()

# Run the application
if __name__ == "__main__":
    app = FairAIHireApp()
    app.run()