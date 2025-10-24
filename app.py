import streamlit as st
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Add the utils directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import from your utils package structure
from utils import ResumeParser, QuestionGenerator
from utils.bias_detector import detect_bias_in_text, analyze_question_fairness, generate_bias_report

class FairAIHireApp:
    def __init__(self):
        self.parser = ResumeParser()
        self.question_gen = QuestionGenerator()
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
        /* Main container styling */
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        
        /* Skill chips with better visibility */
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
        
        /* Question box styling */
        .question-box {
            background-color: #1e1e1e;
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 6px solid #1f77b4;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Section headers */
        .section-header {
            color: #1f77b4;
            font-size: 1.8rem;
            margin: 1.5rem 0 1rem 0;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 0.5rem;
        }
        
        /* Progress bar styling */
        .progress-text {
            color: white;
            font-weight: bold;
            text-align: center;
        }
        
        /* Button container */
        .button-container {
            display: flex;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        /* Answer input area */
        .answer-input {
            background-color: #2b2b2b;
            color: white;
            border: 1px solid #444;
        }
        
        /* Success and error messages */
        .stSuccess {
            color: white;
            background-color: #28a745;
        }
        
        .stError {
            color: white;
            background-color: #dc3545;
        }
        
        /* Bias indicators */
        .bias-low { color: #28a745; font-weight: bold; }
        .bias-medium { color: #ffc107; font-weight: bold; }
        .bias-high { color: #dc3545; font-weight: bold; }
        
        /* Summary cards */
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            margin: 0.5rem 0;
        }
        
        /* Make text areas more visible */
        .stTextArea textarea {
            background-color: #2b2b2b !important;
            color: white !important;
            border: 1px solid #555 !important;
        }
        
        /* Ensure all text is visible */
        .stMarkdown, .stText, .stSubheader, .stHeader {
            color: white !important;
        }
        
        /* Fix for streamlit default text colors */
        p, div, span, h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }
        
        /* Custom container for better contrast */
        .custom-container {
            background-color: #1e1e1e;
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #333;
        }
        
        /* Dashboard specific styles */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
        }
        
        .heatmap-low { background-color: #28a745; color: white; padding: 0.5rem; border-radius: 5px; }
        .heatmap-medium { background-color: #ffc107; color: black; padding: 0.5rem; border-radius: 5px; }
        .heatmap-high { background-color: #dc3545; color: white; padding: 0.5rem; border-radius: 5px; }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        # Session state variables for interview management
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'candidate_skills' not in st.session_state:
            st.session_state.candidate_skills = []
        if 'candidate_experience' not in st.session_state:
            st.session_state.candidate_experience = "Unknown"
        if 'interview_questions' not in st.session_state:
            st.session_state.interview_questions = []
        if 'candidate_answers' not in st.session_state:
            st.session_state.candidate_answers = []
        if 'bias_reports' not in st.session_state:
            st.session_state.bias_reports = []
        if 'interview_started' not in st.session_state:
            st.session_state.interview_started = False
        if 'interview_completed' not in st.session_state:
            st.session_state.interview_completed = False
        if 'resume_analyzed' not in st.session_state:
            st.session_state.resume_analyzed = False
        if 'interview_data' not in st.session_state:
            st.session_state.interview_data = {
                'questions': [],
                'answers': [],
                'bias_analysis': [],
                'start_time': None,
                'end_time': None
            }
    
    def reset_interview(self):
        """Reset the interview session"""
        st.session_state.current_question_index = 0
        st.session_state.candidate_skills = []
        st.session_state.candidate_experience = "Unknown"
        st.session_state.interview_questions = []
        st.session_state.candidate_answers = []
        st.session_state.bias_reports = []
        st.session_state.interview_started = False
        st.session_state.interview_completed = False
        st.session_state.resume_analyzed = False
        st.session_state.interview_data = {
            'questions': [],
            'answers': [],
            'bias_analysis': [],
            'start_time': None,
            'end_time': None
        }
    
    def analyze_resume(self, resume_text):
        """Analyze resume and extract skills/experience"""
        try:
            # Extract skills and experience using the parser class
            skills_result = self.parser.extract_skills(resume_text)
            experience_level = self.parser.parse_experience(resume_text)
            
            # Store in session state
            st.session_state.candidate_skills = skills_result
            st.session_state.candidate_experience = experience_level
            st.session_state.resume_analyzed = True
            
            return True
        except Exception as e:
            st.error(f"Error analyzing resume: {str(e)}")
            return False
    
    def generate_interview_questions(self):
        """Generate personalized interview questions"""
        try:
            questions = self.question_gen.generate_questions(
                st.session_state.candidate_skills,
                st.session_state.candidate_experience
            )
            st.session_state.interview_questions = questions
            st.session_state.candidate_answers = [""] * len(questions)
            st.session_state.bias_reports = [None] * len(questions)
            st.session_state.interview_started = True
            st.session_state.interview_data['questions'] = questions
            st.session_state.interview_data['start_time'] = datetime.now()
            return True
        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return False
    
    def submit_answer(self, answer_text, question_index):
        """Submit answer and run bias detection"""
        if answer_text.strip():
            st.session_state.candidate_answers[question_index] = answer_text
            
            # Run bias detection on the answer
            bias_result = detect_bias_in_text(answer_text)
            st.session_state.bias_reports[question_index] = bias_result
            
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
    
    def display_header(self):
        """Display application header"""
        st.markdown('<h1 class="main-header">🤖 FairAI Hire - Bias-Free Interviews</h1>', 
                   unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; color: #ddd; margin-bottom: 2rem;'>
        Welcome to FairAI Hire! Upload your resume below to start a personalized, 
        unbiased technical interview. Our AI will analyze your skills and generate 
        relevant questions based on your experience level.
        </div>
        """, unsafe_allow_html=True)
    
    def resume_analysis_section(self):
        """Display resume analysis section"""
        st.markdown('<div class="section-header">📄 Resume Analysis</div>', unsafe_allow_html=True)
        
        # Custom container for better visibility
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        
        st.markdown("**Paste your resume text below:**")
        
        resume_text = st.text_area(
            " ",
            height=250,
            placeholder="""Paste your resume content here...

Example:
John Doe
Software Developer with 3 years of experience in Python and JavaScript.

SKILLS:
• Python, JavaScript, React, Node.js, SQL
• Teamwork, Communication, Problem Solving

EXPERIENCE:
• Developed web applications using Python and React
• Led a team of 3 developers
• Strong communication and collaboration skills""",
            key="resume_input",
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🚀 Analyze Resume & Start Interview", type="primary", use_container_width=True):
                if resume_text.strip():
                    with st.spinner("🔍 Analyzing your resume and generating personalized questions..."):
                        if self.analyze_resume(resume_text) and self.generate_interview_questions():
                            st.success("✅ Resume analyzed successfully! Starting your personalized interview...")
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
            
            # Custom container for skills
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
            
            # Experience level with emoji
            level_emojis = {'Entry': '🟢', 'Mid': '🟡', 'Senior': '🔴'}
            emoji = level_emojis.get(st.session_state.candidate_experience, '⚪')
            
            st.markdown(f"""
            **📊 Experience Level:** 
            <span style='font-size: 1.2rem; font-weight: bold; color: #4CAF50;'>
            {emoji} {st.session_state.candidate_experience} Level
            </span>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def interview_section(self):
        """Display interview questions and answers with navigation"""
        if not st.session_state.interview_started or st.session_state.interview_completed:
            return
        
        st.markdown('<div class="section-header">🎤 Interview Session</div>', unsafe_allow_html=True)
        
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
            </div>
            """, unsafe_allow_html=True)
            
            # Current question in styled box
            current_question = st.session_state.interview_questions[current_index]
            st.markdown(f"""
            <div class="question-box">
                <strong style='color: #4FC3F7;'>💡 Question:</strong><br>
                {current_question}
            </div>
            """, unsafe_allow_html=True)
            
            # Answer input area
            st.markdown("**📝 Your Answer:**")
            answer = st.text_area(
                " ",
                value=st.session_state.candidate_answers[current_index],
                height=180,
                placeholder="Share your experience and thoughts here...\n\nTip: Be specific about your projects, challenges, and solutions.",
                key=f"answer_{current_index}",
                label_visibility="collapsed"
            )
            
            # Update answer in session state as user types
            if answer != st.session_state.candidate_answers[current_index]:
                st.session_state.candidate_answers[current_index] = answer
            
            # Navigation and action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                if current_index > 0:
                    if st.button("⬅️ Previous", use_container_width=True):
                        self.navigate_questions("previous")
                        st.rerun()
            
            with col2:
                if st.button("💾 Save Answer", use_container_width=True):
                    if self.submit_answer(answer, current_index):
                        st.success("✅ Answer saved!")
                    else:
                        st.error("Please provide an answer before saving.")
            
            with col3:
                if current_index < total_questions - 1:
                    if st.button("Next ➡️", type="primary", use_container_width=True):
                        self.submit_answer(answer, current_index)
                        self.navigate_questions("next")
                        st.rerun()
                else:
                    if st.button("🏁 Complete Interview", type="primary", use_container_width=True):
                        if self.submit_answer(answer, current_index):
                            self.complete_interview()
                            st.balloons()
                            st.success("🎊 Interview completed! Check the summary tab.")
                            st.rerun()
            
            with col4:
                if st.button("🔄 Restart", use_container_width=True):
                    self.reset_interview()
                    st.rerun()

    def display_fairness_dashboard(self):
        """Display comprehensive fairness dashboard with visual analytics"""
        st.markdown('<div class="section-header">📊 Fairness Dashboard & Analytics</div>', unsafe_allow_html=True)
        
        # Calculate metrics
        skills_match_score = self.calculate_skills_match_score()
        bias_alert_level, bias_color = self.calculate_bias_alert_level()
        completeness_score = self.calculate_interview_completeness()
        fairness_score = self.calculate_overall_fairness_score()
        
        # Overall Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
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
        
        # Visualizations Section
        st.markdown("### 📊 Visual Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Skills Match Visualization
            st.markdown("**🎯 Skills Distribution**")
            self.display_skills_chart()
        
        with col2:
            # Bias Heat Map
            st.markdown("**🔥 Bias Detection Heat Map**")
            self.display_bias_heatmap()
        
        # Detailed Breakdown Section
        st.markdown("### 📋 Detailed Analysis")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Skills Analysis", "⚠️ Bias Alerts", "💡 Recommendations"])
        
        with tab1:
            self.display_skills_analysis()
        
        with tab2:
            self.display_bias_analysis()
        
        with tab3:
            self.display_recommendations()
        
        # Export Functionality
        st.markdown("### 📤 Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Generate Fairness Report", use_container_width=True):
                report = self.generate_fairness_report()
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"fairness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("🔄 Start New Interview", type="primary", use_container_width=True):
                self.reset_interview()
                st.rerun()

    def calculate_skills_match_score(self):
        """Calculate how well candidate skills match typical job requirements"""
        if not st.session_state.candidate_skills:
            return 0
        
        # Define target skills for a software developer role
        target_technical_skills = ['python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'node.js']
        target_soft_skills = ['communication', 'teamwork', 'leadership', 'problem solving', 'creativity']
        
        candidate_tech_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'technical']
        candidate_soft_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'soft']
        
        # Calculate match percentages
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
        
        # Base score based on bias level
        bias_scores = {"Low": 9, "Medium": 6, "High": 3}
        base_score = bias_scores.get(bias_alert_level, 5)
        
        # Adjust based on completeness
        completeness_factor = completeness / 100.0
        
        return min(10, int(base_score + (completeness_factor * 2)))

    def display_skills_chart(self):
        """Display skills distribution chart"""
        if not st.session_state.candidate_skills:
            st.info("No skills data available")
            return
        
        tech_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'technical']
        soft_skills = [skill for skill, category, _ in st.session_state.candidate_skills if category == 'soft']
        
        fig, ax = plt.subplots(figsize=(8, 4))
        
        categories = ['Technical Skills', 'Soft Skills']
        counts = [len(tech_skills), len(soft_skills)]
        colors = ['#667eea', '#f093fb']
        
        bars = ax.bar(categories, counts, color=colors, alpha=0.8)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Number of Skills')
        ax.set_title('Skills Distribution')
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)

    def display_bias_heatmap(self):
        """Display bias detection heatmap"""
        if not st.session_state.bias_reports:
            st.info("No bias data available")
            return
        
        # Count bias types
        bias_types = {}
        for report in st.session_state.bias_reports:
            if report and report.get('bias_types'):
                for bias_type in report['bias_types']:
                    bias_types[bias_type] = bias_types.get(bias_type, 0) + 1
        
        if not bias_types:
            st.success("✅ No biases detected!")
            return
        
        fig, ax = plt.subplots(figsize=(8, 4))
        
        types = list(bias_types.keys())
        counts = list(bias_types.values())
        
        # Create heatmap-like bars
        colors = ['#dc3545' if count > 1 else '#ffc107' for count in counts]
        bars = ax.bar(types, counts, color=colors, alpha=0.8)
        
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{count}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Occurrences')
        ax.set_title('Bias Detection Heatmap')
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)

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
        
        # Specific recommendations based on analysis
        bias_alert_level, _ = self.calculate_bias_alert_level()
        
        if bias_alert_level == "High":
            st.warning("🚨 **Priority Action Needed:** Consider reviewing and retraining interviewers on bias awareness.")
        elif bias_alert_level == "Medium":
            st.info("📝 **Improvement Opportunity:** Implement structured scoring rubrics for more objective evaluation.")

    def generate_fairness_report(self):
        """Generate a comprehensive fairness report"""
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
        for i, (question, bias_report) in enumerate(zip(st.session_state.interview_questions, st.session_state.bias_reports)):
            if bias_report and bias_report.get('bias_types'):
                bias_count += 1
                report_lines.append(f"  • Question {i+1}: {', '.join(bias_report['bias_types'])}")
        
        if bias_count == 0:
            report_lines.append("  • No biases detected - Excellent!")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("RECOMMENDATIONS:")
        report_lines.append("  1. Focus on job-relevant qualifications")
        report_lines.append("  2. Use standardized evaluation criteria")
        report_lines.append("  3. Avoid demographic-based assumptions")
        report_lines.append("  4. Implement structured interview processes")
        
        report_lines.append("")
        report_lines.append("=" * 60)
        report_lines.append("           HIRING THAT SEES SKILLS, NOT DEMOGRAPHICS")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def interview_summary_section(self):
        """Display comprehensive interview summary - NOW USING FAIRNESS DASHBOARD"""
        if not st.session_state.interview_completed:
            return
        
        # Use the new fairness dashboard instead of old summary
        self.display_fairness_dashboard()
    
    def sidebar_controls(self):
        """Display sidebar controls and information"""
        with st.sidebar:
            st.markdown("### 🔧 Session Controls")
            
            if st.session_state.interview_started and not st.session_state.interview_completed:
                st.info("🎤 Interview in Progress")
                current_index = st.session_state.current_question_index
                total_questions = len(st.session_state.interview_questions)
                st.progress(current_index / total_questions)
                st.write(f"Progress: {current_index + 1}/{total_questions}")
            
            if st.button("🔄 Reset Entire Session", use_container_width=True):
                self.reset_interview()
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 📊 Current Status")
            
            if st.session_state.resume_analyzed:
                st.success("✅ Resume Analyzed")
                st.write(f"Skills Found: {len(st.session_state.candidate_skills)}")
                st.write(f"Experience: {st.session_state.candidate_experience}")
            
            if st.session_state.interview_started:
                st.success("✅ Interview Started")
                st.write(f"Questions: {len(st.session_state.interview_questions)}")
                answered = len([a for a in st.session_state.candidate_answers if a.strip()])
                st.write(f"Answered: {answered}/{len(st.session_state.interview_questions)}")
            
            if st.session_state.interview_completed:
                st.success("✅ Interview Completed")
            
            st.markdown("---")
            st.markdown("### 💡 Interview Tips")
            st.markdown("""
            - Be specific in your answers
            - Include real examples and projects
            - Mention challenges and solutions
            - Focus on job-relevant information
            - Avoid personal details that could introduce bias
            """)
    
    def run(self):
        """Main application runner"""
        self.initialize_session_state()
        self.display_header()
        
        # Create tabs for different sections
        if st.session_state.interview_completed:
            tab1, tab2 = st.tabs(["📊 Fairness Dashboard", "🎤 Interview Review"])
        else:
            tab1, tab2 = st.tabs(["🎤 Interview", "📊 Dashboard Preview"])
        
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
            if st.session_state.interview_completed:
                # Show detailed question review in second tab
                self.display_detailed_question_review()
            else:
                st.info("Complete the interview to see the comprehensive fairness dashboard!")
        
        # Always show sidebar controls
        self.sidebar_controls()

    def display_detailed_question_review(self):
        """Display detailed question-by-question review in separate tab"""
        st.markdown('<div class="section-header">📋 Detailed Question Review</div>', unsafe_allow_html=True)
        
        for i, (question, answer, bias_report) in enumerate(zip(
            st.session_state.interview_questions,
            st.session_state.candidate_answers,
            st.session_state.bias_reports
        )):
            with st.expander(f"Question {i+1}: {question[:80]}...", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Your Answer:**")
                    st.info(answer if answer else "No answer provided")
                
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

# Run the application
if __name__ == "__main__":
    app = FairAIHireApp()
    app.run()