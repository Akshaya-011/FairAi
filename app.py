# app.py
import streamlit as st
import sys
import os
import importlib.util

def load_module_from_file(file_path, module_name):
    """Dynamically load a module from a file path"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules
current_dir = os.path.dirname(os.path.abspath(__file__))
resume_parser_path = os.path.join(current_dir, "utils", "resume_parser.py")
question_gen_path = os.path.join(current_dir, "utils", "question_gen.py")

try:
    resume_parser_module = load_module_from_file(resume_parser_path, "resume_parser")
    question_gen_module = load_module_from_file(question_gen_path, "question_gen")
    ResumeParser = resume_parser_module.ResumeParser
    QuestionGenerator = question_gen_module.QuestionGenerator
except Exception as e:
    st.error(f"Error loading modules: {e}")
    st.stop()

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
        """Initialize session state variables"""
        if 'resume_analyzed' not in st.session_state:
            st.session_state.resume_analyzed = False
        if 'skills' not in st.session_state:
            st.session_state.skills = []
        if 'experience_level' not in st.session_state:
            st.session_state.experience_level = 'Entry'
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'answers' not in st.session_state:
            st.session_state.answers = {}
        if 'interview_started' not in st.session_state:
            st.session_state.interview_started = False
    
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
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚀 Analyze Resume & Start Interview", type="primary", use_container_width=True):
            if resume_text.strip():
                with st.spinner("🔍 Analyzing your resume and generating personalized questions..."):
                    # Analyze resume
                    st.session_state.skills = self.parser.extract_skills(resume_text)
                    st.session_state.experience_level = self.parser.parse_experience(resume_text)
                    st.session_state.questions = self.question_gen.generate_questions(
                        st.session_state.skills, st.session_state.experience_level
                    )
                    st.session_state.resume_analyzed = True
                    st.session_state.interview_started = True
                    st.session_state.current_question_index = 0
                
                st.success("✅ Resume analyzed successfully! Starting your personalized interview...")
                st.rerun()
            else:
                st.error("❌ Please paste your resume text to continue.")
    
    def display_skills(self):
        """Display extracted skills in a visually appealing way"""
        if st.session_state.skills:
            st.markdown('<div class="section-header">🎯 Discovered Skills & Experience</div>', unsafe_allow_html=True)
            
            # Custom container for skills
            st.markdown('<div class="custom-container">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔧 Technical Skills**")
                tech_skills = [(skill, confidence) for skill, category, confidence in st.session_state.skills if category == 'technical']
                if tech_skills:
                    for skill, confidence in tech_skills:
                        confidence_text = "Strong" if confidence >= 0.8 else "Moderate"
                        st.markdown(f'<span class="skill-chip skill-chip-technical">⚡ {skill.title()} ({confidence_text})</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.markdown("*No technical skills detected*")
            
            with col2:
                st.markdown("**💬 Soft Skills**")
                soft_skills = [(skill, confidence) for skill, category, confidence in st.session_state.skills if category == 'soft']
                if soft_skills:
                    for skill, confidence in soft_skills:
                        confidence_text = "Strong" if confidence >= 0.8 else "Moderate"
                        st.markdown(f'<span class="skill-chip skill-chip-soft">🌟 {skill.title()} ({confidence_text})</span>', 
                                   unsafe_allow_html=True)
                else:
                    st.markdown("*No soft skills detected*")
            
            # Experience level with emoji
            level_emojis = {'Entry': '🟢', 'Mid': '🟡', 'Senior': '🔴'}
            emoji = level_emojis.get(st.session_state.experience_level, '⚪')
            
            st.markdown(f"""
            **📊 Experience Level:** 
            <span style='font-size: 1.2rem; font-weight: bold; color: #4CAF50;'>
            {emoji} {st.session_state.experience_level} Level
            </span>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def interview_section(self):
        """Display interview questions and answers"""
        if not st.session_state.interview_started:
            return
        
        st.markdown('<div class="section-header">🎤 Interview Session</div>', unsafe_allow_html=True)
        
        if st.session_state.questions:
            current_index = st.session_state.current_question_index
            total_questions = len(st.session_state.questions)
            
            # Progress tracking
            progress = current_index / total_questions
            st.progress(progress)
            
            st.markdown(f"""
            <div class='progress-text'>
            📍 Question {current_index + 1} of {total_questions} 
            ({int(progress * 100)}% Complete)
            </div>
            """, unsafe_allow_html=True)
            
            # Current question in styled box
            current_question = st.session_state.questions[current_index]
            st.markdown(f"""
            <div class="question-box">
                <strong style='color: #4FC3F7;'>💡 Question:</strong><br>
                {current_question}
            </div>
            """, unsafe_allow_html=True)
            
            # Answer input area
            st.markdown("**📝 Your Answer:**")
            answer_key = f"answer_{current_index}"
            answer = st.text_area(
                " ",
                key=answer_key,
                height=180,
                placeholder="Share your experience and thoughts here...\n\nTip: Be specific about your projects, challenges, and solutions.",
                label_visibility="collapsed"
            )
            
            # Button container
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                    if answer.strip():
                        st.session_state.answers[current_index] = answer
                        st.success("🎉 Answer submitted successfully!")
                        
                        # Move to next question or end interview
                        if current_index + 1 < total_questions:
                            st.session_state.current_question_index += 1
                            st.rerun()
                        else:
                            st.balloons()
                            st.success("""
                            🎊 **Interview Completed!** 
                            
                            Thank you for your participation. Your responses have been recorded.
                            """)
                            st.session_state.interview_started = False
                    else:
                        st.error("Please provide an answer before submitting.")
            
            with col2:
                if st.button("⏭️ Skip Question", use_container_width=True) and current_index + 1 < total_questions:
                    st.session_state.current_question_index += 1
                    st.rerun()
            
            with col3:
                if st.button("🔄 Restart Interview", use_container_width=True):
                    st.session_state.interview_started = False
                    st.session_state.current_question_index = 0
                    st.session_state.answers = {}
                    st.rerun()
    
    def run(self):
        """Main application runner"""
        self.initialize_session_state()
        self.display_header()
        
        if not st.session_state.resume_analyzed:
            self.resume_analysis_section()
        else:
            self.display_skills()
            self.interview_section()
            
            # Sidebar controls
            with st.sidebar:
                st.markdown("### 🔧 Controls")
                if st.button("📄 Analyze New Resume", use_container_width=True):
                    st.session_state.resume_analyzed = False
                    st.session_state.interview_started = False
                    st.session_state.current_question_index = 0
                    st.session_state.answers = {}
                    st.rerun()
                
                # Show current progress
                if st.session_state.interview_started:
                    st.markdown("---")
                    total_questions = len(st.session_state.questions)
                    current_index = st.session_state.current_question_index
                    st.markdown(f"**Progress:** {current_index}/{total_questions} questions")
                
                # Quick tips
                st.markdown("---")
                st.markdown("### 💡 Tips")
                st.markdown("""
                - Be specific in your answers
                - Include real examples and projects
                - Mention challenges and solutions
                - Highlight your learning process
                """)

# Run the application
if __name__ == "__main__":
    app = FairAIHireApp()
    app.run()