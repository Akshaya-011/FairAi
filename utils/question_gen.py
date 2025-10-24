import random
from .ai_enhancer import AIEnhancer

class QuestionGenerator:
    def __init__(self, use_ai_enhancement: bool = False):
        self.question_templates = {
            'technical': {
                'python': [
                    "Tell me about your experience with {skill}",
                    "Describe a project where you used {skill}",
                    "What are the key features of {skill} that you find most useful?",
                    "How do you handle error handling in {skill}?",
                    "What {skill} libraries or frameworks are you most familiar with?"
                ],
                'java': [
                    "How would you debug a {skill} application?",
                    "What are the strengths of {skill}?",
                    "Describe your experience with object-oriented programming in {skill}",
                    "How do you manage memory in {skill} applications?"
                ],
                'javascript': [
                    "Tell me about a complex feature you implemented using {skill}",
                    "How do you handle asynchronous operations in {skill}?",
                    "What {skill} frameworks have you worked with?"
                ],
                'sql': [
                    "Describe a complex query you've written in {skill}",
                    "How do you optimize {skill} queries for better performance?",
                    "What's your experience with database design using {skill}?"
                ],
                'react': [
                    "Tell me about a React component you're proud of building",
                    "How do you manage state in {skill} applications?",
                    "What React hooks do you use most frequently?"
                ],
                'node.js': [
                    "Describe a backend service you built with {skill}",
                    "How do you handle API development in {skill}?",
                    "What's your experience with building RESTful APIs in {skill}?"
                ]
            },
            'behavioral': {
                'teamwork': [
                    "Describe a team project where you demonstrated {skill}",
                    "How do you handle conflicts in teams?",
                    "Tell me about a time you helped a teammate overcome a challenge"
                ],
                'communication': [
                    "How do you explain technical concepts to non-technical stakeholders?",
                    "Describe a time when your {skill} skills helped resolve a misunderstanding",
                    "How do you ensure clear communication in remote teams?"
                ],
                'leadership': [
                    "Tell me about a time you demonstrated {skill} on a project",
                    "How do you motivate team members during challenging projects?",
                    "Describe your approach to mentoring junior developers"
                ],
                'problem solving': [
                    "Describe a complex technical problem you solved using your {skill} skills",
                    "How do you approach debugging when you're stuck on a difficult issue?",
                    "Tell me about a time you had to think creatively to solve a problem"
                ]
            }
        }
        
        # Default templates for skills not in the dictionary
        self.default_technical = [
            "What's your experience with {skill}?",
            "Describe a project where you used {skill}",
            "How do you stay updated with the latest developments in {skill}?"
        ]
        
        self.default_behavioral = [
            "How have you demonstrated {skill} in your previous role?",
            "Tell me about a situation where your {skill} was tested",
            "Why is {skill} important in a team environment?"
        ]
        
        # AI Enhancement setup
        self.use_ai = use_ai_enhancement
        self.ai_enhancer = None
        
        if self.use_ai:
            try:
                self.ai_enhancer = AIEnhancer()
                print("🤖 AI Enhancement initialized successfully")
            except Exception as e:
                print(f"⚠️ AI Enhancement failed to initialize: {e}")
                self.use_ai = False

    def generate_questions(self, skills_list, experience_level, use_ai_enhancement=None):
        """
        Generate personalized questions based on skills and experience level
        with optional AI enhancement
        """
        # Use instance setting if not explicitly overridden
        if use_ai_enhancement is None:
            use_ai_enhancement = self.use_ai
        
        questions = []
        technical_skills = [skill for skill, category, _ in skills_list if category == 'technical']
        soft_skills = [skill for skill, category, _ in skills_list if category == 'soft']
        
        # Adjust number of questions based on experience level
        if experience_level == 'Entry':
            num_tech = min(2, len(technical_skills))
            num_behavioral = min(2, len(soft_skills))
        elif experience_level == 'Mid':
            num_tech = min(3, len(technical_skills))
            num_behavioral = min(2, len(soft_skills))
        else:  # Senior
            num_tech = min(4, len(technical_skills))
            num_behavioral = min(3, len(soft_skills))
        
        # Select technical skills and generate questions
        selected_tech = random.sample(technical_skills, min(num_tech, len(technical_skills)))
        for skill in selected_tech:
            templates = self.question_templates['technical'].get(skill, self.default_technical)
            question = random.choice(templates).format(skill=skill)
            
            # AI Enhancement for technical questions
            if use_ai_enhancement and self.ai_enhancer:
                try:
                    context = f"Technical skill: {skill}, Experience level: {experience_level}, Role: Software Developer"
                    enhanced_question = self.ai_enhancer.improve_question(question, context)
                    questions.append(enhanced_question)
                    print(f"🤖 Enhanced technical question: {enhanced_question}")
                except Exception as e:
                    print(f"❌ AI enhancement failed for technical question: {e}")
                    questions.append(question)  # Fallback to original
            else:
                questions.append(question)
        
        # Select soft skills and generate questions
        selected_soft = random.sample(soft_skills, min(num_behavioral, len(soft_skills)))
        for skill in selected_soft:
            templates = self.question_templates['behavioral'].get(skill, self.default_behavioral)
            question = random.choice(templates).format(skill=skill)
            
            # AI Enhancement for behavioral questions
            if use_ai_enhancement and self.ai_enhancer:
                try:
                    context = f"Soft skill: {skill}, Experience level: {experience_level}, Role: Team Collaboration"
                    enhanced_question = self.ai_enhancer.improve_question(question, context)
                    questions.append(enhanced_question)
                    print(f"🤖 Enhanced behavioral question: {enhanced_question}")
                except Exception as e:
                    print(f"❌ AI enhancement failed for behavioral question: {e}")
                    questions.append(question)  # Fallback to original
            else:
                questions.append(question)
        
        # Add experience-level specific questions
        experience_questions = {
            'Entry': [
                "What are you most excited to learn in your next role?",
                "How do you approach learning new technologies?",
                "What kind of mentorship are you looking for in your first role?"
            ],
            'Mid': [
                "How do you balance technical debt with new feature development?",
                "Describe your experience mentoring junior developers",
                "How do you handle competing priorities in projects?"
            ],
            'Senior': [
                "How do you approach system architecture decisions?",
                "Describe your experience leading technical initiatives",
                "How do you align technical decisions with business goals?",
                "What's your strategy for technical team development?"
            ]
        }
        
        level_questions = random.sample(
            experience_questions[experience_level], 
            min(2, len(experience_questions[experience_level]))
        )
        
        # AI Enhancement for experience-level questions
        if use_ai_enhancement and self.ai_enhancer:
            enhanced_level_questions = []
            for question in level_questions:
                try:
                    context = f"Experience level: {experience_level}, Career development question"
                    enhanced_question = self.ai_enhancer.improve_question(question, context)
                    enhanced_level_questions.append(enhanced_question)
                except Exception as e:
                    enhanced_level_questions.append(question)  # Fallback
            questions.extend(enhanced_level_questions)
        else:
            questions.extend(level_questions)
        
        return questions[:5]  # Return max 5 questions

    def get_follow_up_question(self, previous_answer, skill, use_ai_enhancement=None):
        """
        Generate follow-up questions based on previous answer and skill
        with optional AI enhancement
        """
        # Use instance setting if not explicitly overridden
        if use_ai_enhancement is None:
            use_ai_enhancement = self.use_ai
        
        # AI-powered follow-up if enabled
        if use_ai_enhancement and self.ai_enhancer:
            try:
                ai_follow_up = self.ai_enhancer.generate_follow_up(previous_answer, skill)
                print(f"🤖 AI-generated follow-up: {ai_follow_up}")
                return ai_follow_up
            except Exception as e:
                print(f"❌ AI follow-up generation failed: {e}")
                # Fall through to rule-based follow-up
        
        # Rule-based follow-up (fallback)
        follow_ups = {
            'technical': [
                "That's interesting. Can you tell me more about the technical challenges you faced?",
                "How would you approach that differently now with your current knowledge?",
                "What was the impact of that solution on the overall project?",
                "How does that experience relate to other technologies you've worked with?",
                "Can you elaborate on the specific tools or methodologies you used?"
            ],
            'behavioral': [
                "How did that situation help you grow professionally?",
                "What would you do differently if faced with a similar situation today?",
                "How did that experience influence your approach to similar challenges?",
                "What feedback did you receive about your handling of that situation?",
                "How would you apply what you learned to our team environment?"
            ]
        }
        
        # Determine if it's a technical or behavioral skill
        category = 'technical' if skill.lower() in [s.lower() for s in self.question_templates['technical'].keys()] else 'behavioral'
        
        return random.choice(follow_ups[category])

    def analyze_answer_quality(self, answer, question, skill):
        """
        Analyze the quality of a candidate's answer using AI
        """
        if self.use_ai and self.ai_enhancer:
            try:
                analysis = self.ai_enhancer.analyze_answer_depth(answer, question)
                return analysis
            except Exception as e:
                print(f"❌ Answer analysis failed: {e}")
                return self._get_basic_analysis_fallback()
        else:
            return self._get_basic_analysis_fallback()
    
    def _get_basic_analysis_fallback(self):
        """Fallback analysis when AI is not available"""
        return {
            "depth_score": 6,
            "relevance_score": 7,
            "key_strengths": ["Answer provided relevant information"],
            "improvement_areas": ["Could benefit from more specific examples"]
        }

# Test function with AI enhancement
def test_question_gen():
    print("Testing Question Generator with AI Enhancement...")
    
    # Test with AI enabled
    generator_ai = QuestionGenerator(use_ai_enhancement=True)
    
    # Sample skills and experience
    sample_skills = [('python', 'technical', 1.0), ('teamwork', 'soft', 1.0), ('react', 'technical', 0.8)]
    experience_level = 'Mid'
    
    print("\n" + "="*50)
    print("AI-ENHANCED QUESTIONS:")
    print("="*50)
    
    questions = generator_ai.generate_questions(sample_skills, experience_level, use_ai_enhancement=True)
    print("Generated Questions:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    # Test AI follow-up question
    print("\n" + "="*50)
    print("AI FOLLOW-UP TEST:")
    print("="*50)
    test_answer = "I built a full-stack web application using Python and React that helped automate customer onboarding processes. I implemented real-time data validation and integrated with third-party APIs for document verification."
    follow_up = generator_ai.get_follow_up_question(test_answer, "python", use_ai_enhancement=True)
    print(f"Original Answer: {test_answer}")
    print(f"AI Follow-up: {follow_up}")
    
    # Test answer analysis
    print("\n" + "="*50)
    print("ANSWER ANALYSIS TEST:")
    print("="*50)
    analysis = generator_ai.analyze_answer_quality(test_answer, "Tell me about a Python project", "python")
    print(f"Depth Score: {analysis.get('depth_score', 'N/A')}/10")
    print(f"Relevance Score: {analysis.get('relevance_score', 'N/A')}/10")
    print(f"Strengths: {', '.join(analysis.get('key_strengths', []))}")
    print(f"Areas for Improvement: {', '.join(analysis.get('improvement_areas', []))}")
    
    # Test without AI for comparison
    print("\n" + "="*50)
    print("BASIC QUESTIONS (No AI):")
    print("="*50)
    generator_basic = QuestionGenerator(use_ai_enhancement=False)
    basic_questions = generator_basic.generate_questions(sample_skills, experience_level, use_ai_enhancement=False)
    for i, q in enumerate(basic_questions, 1):
        print(f"{i}. {q}")

if __name__ == "__main__":
    test_question_gen()