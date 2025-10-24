import streamlit as st
import os
import sys
from datetime import datetime

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
    
    def interview_summary_section(self):
        """Display comprehensive interview summary"""
        if not st.session_state.interview_completed:
            return
        
        st.markdown('<div class="section-header">📊 Interview Summary</div>', unsafe_allow_html=True)
        
        # Calculate bias metrics
        total_questions = len(st.session_state.interview_questions)
        biased_answers = 0
        good_answers = 0
        
        for bias_report in st.session_state.bias_reports:
            if bias_report and bias_report['severity'] in ['Medium', 'High']:
                biased_answers += 1
            else:
                good_answers += 1
        
        # Summary cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="summary-card">
                <h3>📝 Total Questions</h3>
                <h2>{total_questions}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%);">
                <h3>✅ Good Answers</h3>
                <h2>{good_answers}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            bias_color = "#dc3545" if biased_answers > 0 else "#28a745"
            st.markdown(f"""
            <div class="summary-card" style="background: linear-gradient(135deg, {bias_color} 0%, #e83e8c 100%);">
                <h3>⚠️ Biased Answers</h3>
                <h2>{biased_answers}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed question-by-question review
        st.markdown("### 📋 Detailed Review")
        
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
        
        # Overall bias report
        st.markdown("### 📈 Overall Bias Report")
        overall_report = generate_bias_report(st.session_state.interview_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Overall Fairness Score", f"{overall_report['overall_fairness_score']}/10")
            st.metric("Total Bias Instances", overall_report['total_bias_instances'])
        
        with col2:
            st.metric("Bias Types Detected", len(overall_report['bias_types_detected']))
            st.metric("Fair Questions", overall_report['detailed_metrics']['fair_questions_count'])
        
        # Recommendations
        if overall_report.get('recommendations'):
            st.markdown("### 💡 Recommendations for Fairer Interviews")
            for rec in overall_report['recommendations'][:5]:  # Show top 5
                st.write(f"• {rec}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Start New Interview", type="primary", use_container_width=True):
                self.reset_interview()
                st.rerun()
        with col2:
            if st.button("📊 Export Report", use_container_width=True):
                st.info("Export functionality coming soon!")
    
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
            tab1, tab2 = st.tabs(["📊 Summary", "🎤 Interview"])
        else:
            tab1, tab2 = st.tabs(["🎤 Interview", "📊 Summary"])
        
        with tab1:
            if not st.session_state.resume_analyzed:
                self.resume_analysis_section()
            else:
                if not st.session_state.interview_completed:
                    self.display_skills()
                    self.interview_section()
                else:
                    st.info("Interview completed! Check the Summary tab for results.")
        
        with tab2:
            if st.session_state.interview_completed:
                self.interview_summary_section()
            else:
                st.info("Complete the interview to see the summary report!")
        
        # Always show sidebar controls
        self.sidebar_controls()

# Run the application
if __name__ == "__main__":
    app = FairAIHireApp()
    app.run()