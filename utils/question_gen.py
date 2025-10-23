# utils/question_gen.py
import random

class QuestionGenerator:
    def __init__(self):
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

    def generate_questions(self, skills_list, experience_level):
        """
        Generate personalized questions based on skills and experience level
        """
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
            questions.append(question)
        
        # Select soft skills and generate questions
        selected_soft = random.sample(soft_skills, min(num_behavioral, len(soft_skills)))
        for skill in selected_soft:
            templates = self.question_templates['behavioral'].get(skill, self.default_behavioral)
            question = random.choice(templates).format(skill=skill)
            questions.append(question)
        
        # Add experience-level specific questions
        experience_questions = {
            'Entry': [
                "What are you most excited to learn in your next role?",
                "How do you approach learning new technologies?"
            ],
            'Mid': [
                "How do you balance technical debt with new feature development?",
                "Describe your experience mentoring junior developers"
            ],
            'Senior': [
                "How do you approach system architecture decisions?",
                "Describe your experience leading technical initiatives",
                "How do you align technical decisions with business goals?"
            ]
        }
        
        questions.extend(random.sample(experience_questions[experience_level], 
                                     min(2, len(experience_questions[experience_level]))))
        
        return questions[:5]  # Return max 5 questions

    def get_follow_up_question(self, previous_answer, skill):
        """
        Generate follow-up questions based on previous answer and skill
        """
        follow_ups = {
            'technical': [
                "That's interesting. Can you tell me more about the technical challenges you faced?",
                "How would you approach that differently now?",
                "What was the impact of that solution?",
                "How does that experience relate to other technologies you've worked with?"
            ],
            'behavioral': [
                "How did that situation help you grow professionally?",
                "What would you do differently if faced with a similar situation?",
                "How did that experience influence your approach to similar challenges?"
            ]
        }
        
        # Determine if it's a technical or behavioral skill
        category = 'technical' if skill in [s for s in self.question_templates['technical'].keys()] else 'behavioral'
        
        return random.choice(follow_ups[category])

# Test function
def test_question_gen():
    generator = QuestionGenerator()
    
    # Sample skills and experience
    sample_skills = [('python', 'technical', 1.0), ('teamwork', 'soft', 1.0)]
    experience_level = 'Mid'
    
    questions = generator.generate_questions(sample_skills, experience_level)
    print("Generated Questions:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    # Test follow-up question
    follow_up = generator.get_follow_up_question("I built a web application using Python", "python")
    print(f"\nFollow-up: {follow_up}")

if __name__ == "__main__":
    test_question_gen()