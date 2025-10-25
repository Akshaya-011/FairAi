class DifficultyManager:
    def __init__(self):
        self.difficulty_levels = {
            'Easy': {'score_range': (0, 4), 'next_level': 'Medium'},
            'Medium': {'score_range': (4, 7), 'next_level': 'Hard'}, 
            'Hard': {'score_range': (7, 9), 'next_level': 'Expert'},
            'Expert': {'score_range': (9, 11), 'next_level': 'Expert'}
        }
        
        self.question_banks = {
            'Easy': {
                'technical': [
                    "What is {skill} used for?",
                    "Have you worked with {skill} before?",
                    "Can you explain what {skill} does?",
                    "When would you choose {skill} for a project?",
                    "What are the basic features of {skill}?"
                ],
                'soft': [
                    "Tell me about a time you worked in a team",
                    "How do you handle deadlines?",
                    "What does good communication mean to you?",
                    "Describe your ideal work environment",
                    "How do you approach learning new things?"
                ]
            },
            'Medium': {
                'technical': [
                    "Describe a project where you used {skill}",
                    "What are the main features of {skill}?",
                    "How would you troubleshoot a basic {skill} issue?",
                    "What are the advantages of using {skill}?",
                    "How does {skill} compare to similar technologies?"
                ],
                'soft': [
                    "Describe a challenging team situation and how you resolved it",
                    "How do you prioritize multiple projects?",
                    "Tell me about a time you had to explain technical concepts to non-technical people",
                    "How do you handle feedback on your work?",
                    "Describe a time you had to adapt to changing requirements"
                ]
            },
            'Hard': {
                'technical': [
                    "Compare {skill} with alternative technologies in detail",
                    "What are the performance considerations when using {skill}?",
                    "Describe a complex problem you solved with {skill}",
                    "How would you optimize a {skill} application?",
                    "What are the limitations of {skill} and how do you work around them?"
                ],
                'soft': [
                    "How do you handle conflicts between team members?",
                    "Describe your approach to mentoring junior developers",
                    "Tell me about a time you had to make a difficult technical decision",
                    "How do you drive technical excellence in a team?",
                    "Describe your experience with cross-functional leadership"
                ]
            },
            'Expert': {
                'technical': [
                    "What architectural patterns work best with {skill} and why?",
                    "How would you scale a {skill} application for millions of users?",
                    "What are the security implications of using {skill} in enterprise environments?",
                    "How would you design a fault-tolerant system using {skill}?",
                    "What future developments do you foresee for {skill} technology?"
                ],
                'soft': [
                    "Describe your experience leading technical strategy for an organization",
                    "How do you balance technical debt with business requirements?",
                    "What's your approach to driving technical innovation in a team?",
                    "How do you build and maintain engineering culture?",
                    "Describe your experience with organizational change management"
                ]
            }
        }
    
    def assess_answer_quality(self, answer, question_type):
        """Assess answer quality on a scale of 1-10"""
        if not answer or len(answer.strip()) < 10:
            return 2  # Very poor
        
        score = 5  # Base score
        
        # Length analysis
        word_count = len(answer.split())
        if word_count > 100:
            score += 1
        elif word_count > 200:
            score += 2
        
        # Specificity indicators
        specificity_indicators = ['because', 'for example', 'specifically', 'in my experience', 'for instance']
        if any(indicator in answer.lower() for indicator in specificity_indicators):
            score += 1
        
        # Technical depth (for technical questions)
        if question_type == 'technical':
            technical_indicators = ['architecture', 'performance', 'scalability', 'debug', 'optimize', 'algorithm', 'database', 'api']
            if any(indicator in answer.lower() for indicator in technical_indicators):
                score += 2
        
        # Example indicators
        if 'example' in answer.lower() or 'project' in answer.lower() or 'experience' in answer.lower():
            score += 1
        
        # Problem-solving indicators
        problem_indicators = ['challenge', 'problem', 'issue', 'debug', 'solve', 'fix']
        if any(indicator in answer.lower() for indicator in problem_indicators):
            score += 1
        
        return min(10, max(1, score))
    
    def get_next_difficulty(self, current_difficulty, recent_scores):
        """Determine next difficulty level based on performance"""
        if not recent_scores:
            return current_difficulty
        
        avg_score = sum(recent_scores) / len(recent_scores)
        current_level = self.difficulty_levels[current_difficulty]
        
        if avg_score >= current_level['score_range'][1]:
            return current_level['next_level']
        elif avg_score <= current_level['score_range'][0]:
            # Move down one level if possible
            for level, data in self.difficulty_levels.items():
                if data.get('next_level') == current_difficulty:
                    return level
        
        return current_difficulty
    
    def get_question_for_difficulty(self, difficulty, skill, question_type='technical'):
        """Get a question appropriate for the difficulty level"""
        bank = self.question_banks.get(difficulty, self.question_banks['Medium'])
        questions = bank.get(question_type, [])
        
        if questions:
            import random
            template = random.choice(questions)
            return template.format(skill=skill)
        
        # Fallback question
        return f"Tell me about your experience with {skill}"

# Global instance
difficulty_manager = DifficultyManager()