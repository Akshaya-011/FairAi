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
    # NEW: Import language support
    from utils.language_support import language_support
except ImportError as e:
    st.error(f"Some modules not found: {e}")
    
    # Fallback implementations (keeping your existing fallbacks)
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
    
    # Language support fallback
    class LanguageSupport:
        def __init__(self):
            self.supported_languages = ['English', 'Spanish', 'French', 'Telugu', 'Hindi']
        
        def detect_language(self, text):
            return 'English'
        
        def translate_ui_text(self, text_key, target_language):
            return text_key
        
        def adapt_question_for_language(self, question, target_language, original_language='English'):
            return question
    
    bias_heatmap = BiasHeatmapGenerator()
    difficulty_manager = DifficultyManager()
    heatmap_generator = HeatmapGenerator()
    analytics_engine = AnalyticsEngine()
    language_support = LanguageSupport()
    
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
            self.language_support = language_support
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
            self.language_support = language_support
        
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
        .language-selector {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: white;
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
            # NEW: Language support
            'selected_language': 'English',
            'auto_detected_language': None,
            'resume_language_detected': False
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def reset_interview(self):
        """Reset the interview session"""
        for key in list(st.session_state.keys()):
            if key not in ['ai_enabled', 'selected_language']:  # Keep AI and language settings
                del st.session_state[key]
        self.initialize_session_state()
    
    def get_translated_text(self, text_key):
        """Get translated text for current language"""
        return self.language_support.translate_ui_text(text_key, st.session_state.selected_language)
    
    def analyze_resume(self, resume_text):
        """Analyze resume and extract skills/experience"""
        try:
            # Auto-detect language from resume if not already detected
            if not st.session_state.resume_language_detected:
                detected_lang = self.language_support.detect_language(resume_text)
                st.session_state.auto_detected_language = detected_lang
                st.session_state.resume_language_detected = True
                
                # Auto-switch to detected language if different from current
                if detected_lang != st.session_state.selected_language:
                    st.session_state.selected_language = detected_lang
                    st.success(f"🌍 {self.get_translated_text('auto_detect')}: {detected_lang}")
            
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
        """Generate personalized interview questions with bias checking and language adaptation"""
        try:
            questions = self.question_gen.generate_questions(
                st.session_state.candidate_skills,
                st.session_state.candidate_experience
            )
            
            # Adapt questions to selected language
            adapted_questions = []
            for question in questions:
                adapted_question = self.language_support.adapt_question_for_language(
                    question, 
                    st.session_state.selected_language
                )
                adapted_questions.append(adapted_question)
            
            # NEW: Check questions for potential bias before displaying
            checked_questions = []
            bias_warnings = []
            
            for i, question in enumerate(adapted_questions):
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
                    st.error(f"🚨 {self.get_translated_text('bias_alerts')}:")
                    for warning in bias_warnings:
                        st.write(f"• {warning}")
            
            # Generate AI-enhanced questions if enabled
            if st.session_state.ai_enabled and self.ai_enhancer.available:
                with st.spinner(f"🤖 {self.get_translated_text('ai_enhancement')}..."):
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
    
    def submit_answer(self, answer_text, question_index):
        """Submit answer and run bias detection"""
        if answer_text.strip():
            st.session_state.candidate_answers[question_index] = answer_text
            
            # Run bias detection with language-specific patterns
            bias_result = detect_bias_in_text(answer_text)
            st.session_state.bias_reports[question_index] = bias_result
            
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
            if st.session_state.ai_enabled and self.ai_enhancer.available:
                with st.spinner(f"🤖 {self.get_translated_text('ai_analysis_previous_answer')}..."):
                    skills_list = [skill[0] for skill in st.session_state.candidate_skills]
                    analysis = self.ai_enhancer.analyze_answer_depth(
                        answer_text, 
                        st.session_state.interview_questions[question_index],
                        skills_list
                    )
                    st.session_state.answer_analysis[question_index] = analysis
                    
                    # Generate follow-up question - FIXED THE SYNTAX ERROR HERE
                    skill_focus = None
                    if skills_list and question_index < len(skills_list):
                        skill_focus = skills_list[min(question_index, len(skills_list)-1)]  # FIXED: Added missing closing parenthesis
                    
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
        st.markdown(f'<div class="section-header">{self.get_translated_text("recruiter_dashboard")}</div>', unsafe_allow_html=True)
        
        if not st.session_state.analytics_data:
            st.info(self.get_translated_text("complete_interview_to_see"))
            return
        
        analytics_data = st.session_state.analytics_data
        
        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_score = analytics_data['skills_fit'].get('overall_score', 0)
            st.markdown(f"""
            <div class="recruiter-metric-card">
                <h3>🎯 {self.get_translated_text("overall_match")}</h3>
                <h1>{overall_score}%</h1>
                <p>{self.get_translated_text("job_requirement_fit")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            hire_confidence = analytics_data.get('hire_confidence', 0)
            confidence_class = "hire-confidence-high" if hire_confidence >= 80 else "hire-confidence-medium" if hire_confidence >= 60 else "hire-confidence-low"
            st.markdown(f"""
            <div class="recruiter-metric-card {confidence_class}">
                <h3>🏆 {self.get_translated_text("hire_confidence")}</h3>
                <h1>{hire_confidence}%</h1>
                <p>{self.get_translated_text("recommended_score")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            coherence_score = analytics_data['communication_analysis'].get('coherence_score', 0)
            st.markdown(f"""
            <div class="recruiter-metric-card">
                <h3>💬 {self.get_translated_text("communication")}</h3>
                <h1>{coherence_score}%</h1>
                <p>{self.get_translated_text("coherence_score")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            bias_count = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
            bias_score = max(0, 100 - (bias_count * 15))
            st.markdown(f"""
            <div class="recruiter-metric-card">
                <h3>⚖️ {self.get_translated_text("fairness")}</h3>
                <h1>{bias_score}%</h1>
                <p>{self.get_translated_text("bias_free_score")}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Automated Insights
        st.markdown(f"### 🤖 {self.get_translated_text('automated_insights')}")
        insights = analytics_data.get('summary_insights', [])
        for insight in insights:
            st.info(insight)
        
        # Detailed Analytics Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            f"📊 {self.get_translated_text('skills_analysis')}",
            f"💬 {self.get_translated_text('communication')}",
            f"🎯 {self.get_translated_text('recommendations')}",
            f"📈 {self.get_translated_text('candidate_comparison')}"
        ])
        
        with tab1:
            self.display_skills_analytics(analytics_data['skills_fit'])
        
        with tab2:
            self.display_communication_analytics(analytics_data['communication_analysis'])
        
        with tab3:
            self.display_recommendations_analytics(analytics_data)
        
        with tab4:
            self.display_comparative_analytics()
        
        # Export Functionality
        st.markdown(f"### 📤 {self.get_translated_text('export_analysis')}")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"📄 {self.get_translated_text('generate_full_report')}", use_container_width=True):
                report = self.generate_analytics_report()
                st.download_button(
                    label=f"📥 {self.get_translated_text('download_report')}",
                    data=report,
                    file_name=f"candidate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button(f"🔄 {self.get_translated_text('analyze_new_candidate')}", type="primary", use_container_width=True):
                self.reset_interview()
                st.rerun()
    
    def display_skills_analytics(self, skills_fit):
        """Display skills analysis in recruiter dashboard"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🎯 {self.get_translated_text('skills_match_breakdown')}")
            
            # Create skills match gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = skills_fit.get('overall_score', 0),
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': self.get_translated_text("overall_match")},
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
            st.markdown(f"#### 📈 {self.get_translated_text('skills_distribution')}")
            
            # Skills breakdown
            strengths = skills_fit.get('strengths', [])
            weaknesses = skills_fit.get('weaknesses', [])
            
            st.metric(self.get_translated_text("strengths_label"), len(strengths))
            if strengths:
                for strength in strengths:
                    st.success(f"✅ {strength}")
            
            st.metric(self.get_translated_text("weaknesses"), len(weaknesses))
            if weaknesses:
                for weakness in weaknesses:
                    st.error(f"📝 {weakness}")
    
    def display_communication_analytics(self, communication_analysis):
        """Display communication analytics"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🗣️ {self.get_translated_text('communication_metrics')}")
            
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
            fig = px.bar(df, x='Metric', y='Score', title=self.get_translated_text("communication_metrics"),
                        color='Score', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"#### 💡 {self.get_translated_text('communication_style')}")
            
            style = communication_analysis.get('communication_style', 'Unknown')
            st.metric(self.get_translated_text("communication_style"), style)
            
            improvement_areas = communication_analysis.get('improvement_areas', [])
            if improvement_areas:
                st.markdown(f"**{self.get_translated_text('improvement_areas')}:**")
                for area in improvement_areas:
                    st.warning(f"⚠️ {area}")
            else:
                st.success("🎉 Strong communication skills across all areas!")
    
    def display_recommendations_analytics(self, analytics_data):
        """Display recommendations and next steps"""
        st.markdown(f"#### 💡 {self.get_translated_text('actionable_recommendations')}")
        
        recommendations = analytics_data.get('improvement_recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
        else:
            st.success("🎉 No major improvement areas identified!")
        
        # Next steps based on hire confidence
        hire_confidence = analytics_data.get('hire_confidence', 0)
        st.markdown(f"#### 🎯 {self.get_translated_text('recommended_next_steps')}")
        
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
        st.markdown(f"#### 📊 {self.get_translated_text('candidate_comparison')}")
        
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
                fig = px.bar(df, barmode='group', title=self.get_translated_text("skills_comparison"))
                st.plotly_chart(fig, use_container_width=True)
            
            # Diversity metrics
            st.markdown("##### 🌈 Diversity Metrics")
            diversity_metrics = comparative_data.get('diversity_metrics', {})
            if diversity_metrics:
                for metric, value in diversity_metrics.items():
                    st.write(f"**{metric.replace('_', ' ').title()}:** {value}")
        else:
            st.info(self.get_translated_text("add_more_candidates"))
    
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
            st.markdown(f"### 🔧 {self.get_translated_text('session_controls')}")
            
            # Language Selector
            st.markdown(f"### 🌍 {self.get_translated_text('interview_language')}")
            selected_language = st.selectbox(
                self.get_translated_text('select_language'),
                options=self.language_support.supported_languages,
                index=self.language_support.supported_languages.index(st.session_state.selected_language)
            )
            
            if selected_language != st.session_state.selected_language:
                st.session_state.selected_language = selected_language
                st.rerun()
            
            # Show auto-detected language if available
            if st.session_state.auto_detected_language:
                st.info(f"🌐 {self.get_translated_text('auto_detect')}: {st.session_state.auto_detected_language}")
            
            st.markdown("---")
            
            # AI Enhancement Toggle
            st.markdown(f"### 🤖 {self.get_translated_text('ai_enhancement')}")
            ai_enabled = st.toggle(self.get_translated_text("enable_ai_features"), 
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
            st.markdown(f"### 📊 {self.get_translated_text('current_status')}")
            
            if st.session_state.resume_analyzed:
                st.success(f"✅ {self.get_translated_text('resume_analyzed')}")
                st.write(f"{self.get_translated_text('skills_found')}: {len(st.session_state.candidate_skills)}")
                st.write(f"{self.get_translated_text('experience_level')}: {st.session_state.candidate_experience}")
                st.write(f"{self.get_translated_text('current_difficulty')}: {st.session_state.current_difficulty}")
                st.write(f"{self.get_translated_text('interview_language')}: {st.session_state.selected_language}")
            
            if st.session_state.interview_started:
                st.success(f"✅ {self.get_translated_text('interview_started')}")
                st.write(f"{self.get_translated_text('questions_generated')}: {len(st.session_state.interview_questions)}")
                answered = len([a for a in st.session_state.candidate_answers if a.strip()])
                st.write(f"{self.get_translated_text('answered_questions')}: {answered}/{len(st.session_state.interview_questions)}")
                
                # NEW: Show bias count
                bias_count = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
                st.write(f"{self.get_translated_text('bias_alerts')}: {bias_count}")
            
            if st.session_state.interview_completed:
                st.success(f"✅ {self.get_translated_text('interview_completed')}")
                if st.session_state.analytics_data:
                    st.write(f"{self.get_translated_text('hire_confidence')}: {st.session_state.analytics_data.get('hire_confidence', 0)}%")
            
            st.markdown("---")
            
            if st.button(f"🔄 {self.get_translated_text('reset_entire_session')}", use_container_width=True, key="sidebar_reset"):
                self.reset_interview()
                st.rerun()
            
            st.markdown("---")
            st.markdown(f"### 💡 {self.get_translated_text('interview_tips')}")
            st.markdown("""
            - Be specific in your answers
            - Include real examples and projects
            - Mention challenges and solutions
            - Focus on job-relevant information
            - Avoid personal details that could introduce bias
            - You can answer in any supported language
            """)
            
            # Accessibility Note
            st.markdown("---")
            st.markdown(f"### 🌐 {self.get_translated_text('accessibility')}")
            st.info(self.get_translated_text('accessibility_note'))

    def display_header(self):
        """Display application header"""
        st.markdown(f'<h1 class="main-header">🤖 {self.get_translated_text("welcome")}</h1>', 
                   unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style='text-align: center; color: #ddd; margin-bottom: 2rem;'>
        Upload your resume below to start a personalized, 
        unbiased technical interview.
        </div>
        """, unsafe_allow_html=True)
    
    def resume_analysis_section(self):
        """Display resume analysis section"""
        st.markdown(f'<div class="section-header">📄 {self.get_translated_text("resume_analysis")}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        st.markdown(f"**{self.get_translated_text('paste_resume')}**")
        
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
            if st.button(f"🚀 {self.get_translated_text('analyze_resume')}", type="primary", use_container_width=True):
                if resume_text.strip():
                    with st.spinner("🔍 Analyzing your resume..."):
                        if self.analyze_resume(resume_text) and self.generate_interview_questions():
                            st.success("✅ Resume analyzed successfully!")
                            st.rerun()
                else:
                    st.error("❌ Please paste your resume text to continue.")
        
        with col2:
            if st.button(f"🔄 {self.get_translated_text('reset_session')}", use_container_width=True):
                self.reset_interview()
                st.rerun()
    
    def display_skills(self):
        """Display extracted skills in a visually appealing way"""
        if st.session_state.candidate_skills:
            st.markdown(f'<div class="section-header">🎯 {self.get_translated_text("discovered_skills")}</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="custom-container">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**🔧 {self.get_translated_text('technical_skills')}**")
                tech_skills = [skill for skill, category, confidence in st.session_state.candidate_skills if category == 'technical']
                if tech_skills:
                    for skill in tech_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-technical">⚡ {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.markdown(f"*{self.get_translated_text('no_technical_skills')}*")
            
            with col2:
                st.markdown(f"**💬 {self.get_translated_text('soft_skills')}**")
                soft_skills = [skill for skill, category, confidence in st.session_state.candidate_skills if category == 'soft']
                if soft_skills:
                    for skill in soft_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-soft">🌟 {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.markdown(f"*{self.get_translated_text('no_soft_skills')}*")
            
            # Experience level
            level_emojis = {'Entry': '🟢', 'Mid': '🟡', 'Senior': '🔴'}
            emoji = level_emojis.get(st.session_state.candidate_experience, '⚪')
            
            st.markdown(f"""
            **📊 {self.get_translated_text('experience_level')}:** 
            <span style='font-size: 1.2rem; font-weight: bold; color: #4CAF50;'>
            {emoji} {st.session_state.candidate_experience} Level
            </span>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def skills_visualization_section(self):
        """Display skills graph visualization"""
        st.markdown(f'<div class="section-header">🕸️ {self.get_translated_text("skills_visualization")}</div>', unsafe_allow_html=True)
        
        if not st.session_state.skills_graph:
            st.info(f"👆 {self.get_translated_text('analyze_resume_first')}")
            return
        
        # Create tabs for different visualizations
        viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Network Graph", "Category Analysis", "Confidence Heatmap"])
        
        with viz_tab1:
            st.markdown(f"### 🕸️ {self.get_translated_text('skills_relationship_network')}")
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
            st.markdown(f"### 📊 {self.get_translated_text('skills_category_analysis')}")
            
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
            st.markdown(f"### 🔥 {self.get_translated_text('skill_confidence_heatmap')}")
            fig_heatmap = create_confidence_heatmap(st.session_state.skills_graph)
            st.plotly_chart(fig_heatmap, use_container_width=True, key="confidence_heatmap")
            
            # Skills metrics
            metrics = calculate_skill_metrics(st.session_state.skills_graph)
            st.markdown(f"### 📈 {self.get_translated_text('skills_metrics')}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(self.get_translated_text("total_skills"), metrics['total_skills'])
            with col2:
                st.metric(self.get_translated_text("avg_confidence"), f"{metrics['avg_confidence']:.2f}")
            with col3:
                st.metric(self.get_translated_text("relationships"), metrics['total_relationships'])
            with col4:
                st.metric(self.get_translated_text("connectivity"), f"{metrics['connectivity_score']:.2f}")
            
            # Export functionality
            st.markdown(f"### 💾 {self.get_translated_text('export_skills_data')}")
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
        """Display interview questions and answers with navigation"""
        if not st.session_state.interview_started or st.session_state.interview_completed:
            return
        
        st.markdown(f'<div class="section-header">🎤 {self.get_translated_text("interview_session")}</div>', unsafe_allow_html=True)
        
        # Language indicator
        st.markdown(f"""
        <div class="language-selector">
            🌍 <strong>{self.get_translated_text('interview_language')}:</strong> {st.session_state.selected_language} 
            | 💬 <strong>You can answer in any language</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # NEW: Real-time bias alert counter
        current_biases = len([r for r in st.session_state.bias_reports if r and r.get('bias_types')])
        if current_biases > 0:
            st.markdown(f"""
            <div class="bias-alert-box">
                <strong>🚨 {self.get_translated_text('bias_alerts')}:</strong> {current_biases} potential bias(es) detected so far
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
            <br>📊 {self.get_translated_text('current_difficulty')}: <strong>{st.session_state.current_difficulty}</strong>
            <br>🌐 {self.get_translated_text('interview_language')}: <strong>{st.session_state.selected_language}</strong>
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
                    <strong style='color: #FFD700;'>🤖 {self.get_translated_text('ai_enhanced_question')}:</strong><br>
                    {enhanced_data['improved_question']}
                    <br><br>
                    <small><em>💡 {enhanced_data['explanation']}</em></small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="question-box">
                    <strong style='color: #4FC3F7;'>💡 {self.get_translated_text('questions_generated')}:</strong><br>
                    {current_question}
                </div>
                """, unsafe_allow_html=True)
            
            # Answer input area
            st.markdown(f"**{self.get_translated_text('your_answer')}**")
            answer = st.text_area(
                " ",
                value=st.session_state.candidate_answers[current_index],
                height=180,
                placeholder="Share your experience and thoughts here... You can answer in any language.",
                key=f"answer_{current_index}",
                label_visibility="collapsed"
            )
            
            # Update answer in session state as user types
            if answer != st.session_state.candidate_answers[current_index]:
                st.session_state.candidate_answers[current_index] = answer
            
            # Display AI analysis of previous answer if available
            if (current_index > 0 and 
                st.session_state.answer_analysis and 
                st.session_state.answer_analysis[current_index-1]):
                
                analysis = st.session_state.answer_analysis[current_index-1]
                if analysis.get('success'):
                    st.markdown(f"""
                    <div class="ai-analysis-box">
                        <strong>🤖 {self.get_translated_text('ai_analysis_previous_answer')}:</strong><br>
                        <strong>{self.get_translated_text('quality_score_label')}:</strong> {analysis.get('quality_score', 'N/A')}/10<br>
                        <strong>{self.get_translated_text('strengths_label')}:</strong> {', '.join(analysis.get('strengths', []))}<br>
                        <strong>{self.get_translated_text('skills_demonstrated')}:</strong> {', '.join(analysis.get('skills_demonstrated', []))}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Navigation and action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if current_index > 0:
                    if st.button(f"⬅️ {self.get_translated_text('previous_question')}", use_container_width=True, key=f"prev_{current_index}"):
                        self.navigate_questions("previous")
                        st.rerun()
            
            with col2:
                if st.button(f"💾 {self.get_translated_text('save_answer')}", use_container_width=True, key=f"save_{current_index}"):
                    if self.submit_answer(answer, current_index):
                        st.success("✅ Answer saved!")
                    else:
                        st.error("Please provide an answer before saving.")
            
            with col3:
                if current_index < total_questions - 1:
                    if st.button(f"{self.get_translated_text('next_question')} ➡️", type="primary", use_container_width=True, key=f"next_{current_index}"):
                        self.submit_answer(answer, current_index)
                        self.navigate_questions("next")
                        st.rerun()
                else:
                    if st.button(f"🏁 {self.get_translated_text('complete_interview')}", type="primary", use_container_width=True, key="complete_interview"):
                        if self.submit_answer(answer, current_index):
                            self.complete_interview()
                            st.balloons()
                            st.success("🎊 Interview completed! Check the summary tab.")
                            st.rerun()
            
            with col4:
                if st.button("🔄 Restart", use_container_width=True, key=f"restart_{current_index}"):
                    self.reset_interview()
                    st.rerun()

    def display_fairness_dashboard(self):
        """Display comprehensive fairness dashboard with visual analytics"""
        st.markdown(f'<div class="section-header">📊 {self.get_translated_text("fairness_dashboard")}</div>', unsafe_allow_html=True)
        
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
                <h3>🎯 {self.get_translated_text('overall_match')}</h3>
                <h2>{skills_match_score}%</h2>
                <p>{self.get_translated_text('job_requirement_fit')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            alert_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}.get(bias_alert_level, "⚪")
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, {bias_color} 0%, #e83e8c 100%);">
                <h3>⚠️ {self.get_translated_text('bias_alerts')}</h3>
                <h2>{alert_emoji} {bias_alert_level}</h2>
                <p>{self.get_translated_text('fairness')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                <h3>📈 {self.get_translated_text('completeness')}</h3>
                <h2>{completeness_score}%</h2>
                <p>{self.get_translated_text('interview_progress')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            score_color = "#28a745" if fairness_score >= 7 else "#ffc107" if fairness_score >= 5 else "#dc3545"
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, {score_color} 0%, #fd7e14 100%);">
                <h3>⚖️ {self.get_translated_text('fairness_score')}</h3>
                <h2>{fairness_score}/10</h2>
                <p>{self.get_translated_text('overall_rating')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            # NEW: Bias Score Gauge
            bias_score = bias_report.get('overall_score', 100)
            grade = bias_report.get('grade', 'A+')
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);">
                <h3>📊 {self.get_translated_text('bias_score')}</h3>
                <h2>{bias_score}% {grade}</h2>
                <p>{self.get_translated_text('fairness_grade')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # NEW: Enhanced Visual Analytics Section
        st.markdown(f"### 📊 {self.get_translated_text('advanced_bias_analytics')}")
        
        # Row 1: Heatmap and Timeline
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 🔥 {self.get_translated_text('real_time_bias_heatmap')}")
            heatmap_fig = self.heatmap_generator.generate_bias_heatmap(st.session_state.interview_data)
            st.plotly_chart(heatmap_fig, use_container_width=True, key="enhanced_bias_heatmap")
        
        with col2:
            st.markdown(f"#### 📈 {self.get_translated_text('bias_detection_timeline')}")
            if len(st.session_state.bias_history) > 1:
                timeline_fig = self.heatmap_generator.generate_timeline_heatmap(st.session_state.bias_history)
                st.plotly_chart(timeline_fig, use_container_width=True, key="bias_timeline")
            else:
                st.info(self.get_translated_text("complete_more_questions"))
        
        # Row 2: Category Distribution and Severity Gauge
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown(f"#### 🎯 {self.get_translated_text('bias_category_distribution')}")
            category_fig = self.heatmap_generator.generate_category_distribution(
                bias_report.get('category_breakdown', {})
            )
            st.plotly_chart(category_fig, use_container_width=True, key="bias_categories")
        
        with col4:
            st.markdown(f"#### 📊 {self.get_translated_text('overall_bias_score')}")
            gauge_fig = self.heatmap_generator.generate_severity_gauge(bias_score)
            st.plotly_chart(gauge_fig, use_container_width=True, key="bias_gauge")
        
        # NEW: Bias Hotspots Section
        st.markdown(f"### 🚨 {self.get_translated_text('bias_hotspots_recommendations')}")
        
        hotspots = bias_report.get('trend_analysis', {}).get('hotspots', [])
        if hotspots:
            st.warning(f"**Bias Hotspots Detected:** {', '.join(hotspots)}")
            
            # Display recommendations
            recommendations = bias_report.get('recommendations', [])
            if recommendations:
                st.markdown(f"#### 💡 {self.get_translated_text('improvement_recommendations')}:")
                for rec in recommendations:
                    st.success(f"✅ {rec}")
        else:
            st.success("🎉 Excellent! No significant bias hotspots detected in this interview.")
        
        # Detailed Breakdown Section
        st.markdown(f"### 📋 {self.get_translated_text('detailed_analysis')}")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            f"🔍 {self.get_translated_text('skills_analysis')}",
            f"⚠️ {self.get_translated_text('bias_analysis')}",
            f"📊 {self.get_translated_text('performance_analysis')}",
            f"🤖 {self.get_translated_text('ai_insights')}",
            f"💡 {self.get_translated_text('recommendations')}"
        ])
        
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
        st.markdown(f"### 📤 {self.get_translated_text('export_analysis')}")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"📄 {self.get_translated_text('generate_full_report')}", use_container_width=True, key="generate_report"):
                report = self.generate_fairness_report()
                st.download_button(
                    label=f"📥 {self.get_translated_text('download_report')}",
                    data=report,
                    file_name=f"fairness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_report"
                )
        
        with col2:
            if st.button(f"🔄 {self.get_translated_text('start_interview')}", type="primary", use_container_width=True, key="new_interview"):
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
        st.markdown(f"#### 🎯 {self.get_translated_text('skills_identified')}")
        
        if st.session_state.candidate_skills:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{self.get_translated_text('technical_skills')}:**")
                tech_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'technical']
                if tech_skills:
                    for skill in tech_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-technical">⚡ {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.write(self.get_translated_text("no_technical_skills"))
            
            with col2:
                st.markdown(f"**{self.get_translated_text('soft_skills')}:**")
                soft_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'soft']
                if soft_skills:
                    for skill in soft_skills:
                        st.markdown(f'<span class="skill-chip skill-chip-soft">🌟 {skill.title()}</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.write(self.get_translated_text("no_soft_skills"))
            
            st.metric(self.get_translated_text("total_skills"), len(st.session_state.candidate_skills))
        else:
            st.info(self.get_translated_text("no_skills_detected"))

    def display_bias_analysis(self):
        """Display detailed bias analysis"""
        st.markdown(f"#### ⚠️ {self.get_translated_text('bias_detection_results')}")
        
        if not st.session_state.bias_reports or all(report is None for report in st.session_state.bias_reports):
            st.success(f"✅ {self.get_translated_text('excellent_no_biases')}")
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
            st.success(f"✅ {self.get_translated_text('no_significant_biases')}")

    def display_performance_analysis(self):
        """NEW: Display performance analysis with difficulty tracking"""
        st.markdown(f"#### 📊 {self.get_translated_text('performance_analysis')}")
        
        if not st.session_state.answer_scores:
            st.info(self.get_translated_text("complete_more_questions"))
            return
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_score = sum(st.session_state.answer_scores) / len(st.session_state.answer_scores)
            st.metric(self.get_translated_text("quality_score"), f"{avg_score:.1f}/10")
        
        with col2:
            st.metric(self.get_translated_text("current_difficulty"), st.session_state.current_difficulty)
        
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
        st.markdown(f"#### 🤖 {self.get_translated_text('ai_powered_insights')}")
        
        if not st.session_state.ai_enabled or not self.ai_enhancer.available:
            st.info(self.get_translated_text("enable_ai_for_insights"))
            return
        
        if not st.session_state.answer_analysis or all(analysis is None for analysis in st.session_state.answer_analysis):
            st.info(self.get_translated_text("complete_for_ai_analysis"))
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
                st.metric(f"📊 {self.get_translated_text('answer_quality_score')}", f"{avg_quality:.1f}/10")
                
                if avg_quality >= 8:
                    st.success("🎉 Excellent! Your answers demonstrate strong experience and clarity.")
                elif avg_quality >= 6:
                    st.info("👍 Good! Your answers are comprehensive and relevant.")
                else:
                    st.warning("💡 Consider providing more specific examples and details in your answers.")
        
        # Detailed answer analysis
        st.markdown(f"#### 📝 {self.get_translated_text('answer_by_answer_analysis')}")
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
                        st.metric(self.get_translated_text("quality_score_label"), f"{analysis.get('quality_score', 'N/A')}/10")
                        st.metric(self.get_translated_text("relevance"), f"{analysis.get('relevance_score', 'N/A')}/10")
                    
                    st.markdown(f"**{self.get_translated_text('strengths_label')}:**")
                    for strength in analysis.get('strengths', []):
                        st.write(f"✅ {strength}")
                    
                    st.markdown("**Areas for Improvement:**")
                    for improvement in analysis.get('improvements', []):
                        st.write(f"📝 {improvement}")
                    
                    st.markdown(f"**{self.get_translated_text('skills_demonstrated')}:**")
                    skills = analysis.get('skills_demonstrated', [])
                    if skills:
                        for skill in skills:
                            st.markdown(f'<span class="skill-chip">🎯 {skill}</span>', unsafe_allow_html=True)
                    else:
                        st.write("No specific skills identified in this answer.")

    def display_recommendations(self):
        """Display fairness recommendations"""
        st.markdown(f"#### 💡 {self.get_translated_text('recommendations_for_fair_hiring')}")
        
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
        st.markdown(f'<div class="section-header">📋 {self.get_translated_text("detailed_question_review")}</div>', unsafe_allow_html=True)
        
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
            tab1, tab2, tab3, tab4 = st.tabs([
                f"📊 {self.get_translated_text('fairness_dashboard')}",
                f"👔 {self.get_translated_text('recruiter_dashboard')}",
                f"🕸️ {self.get_translated_text('skills_visualization')}",
                f"🎤 {self.get_translated_text('interview_review')}"
            ])
        elif st.session_state.resume_analyzed:
            tab1, tab2, tab3, tab4 = st.tabs([
                f"🎤 {self.get_translated_text('interview')}",
                f"🕸️ {self.get_translated_text('skills_visualization')}",
                f"📊 {self.get_translated_text('dashboard_preview')}",
                f"👔 {self.get_translated_text('recruiter_view')}"
            ])
        else:
            tab1, tab2, tab3, tab4 = st.tabs([
                f"🎤 {self.get_translated_text('interview')}",
                f"🕸️ {self.get_translated_text('skills_visualization')}",
                f"📊 {self.get_translated_text('dashboard_preview')}",
                f"👔 {self.get_translated_text('recruiter_view')}"
            ])
        
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