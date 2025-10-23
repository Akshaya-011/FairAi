# utils/resume_parser.py
import re
import spacy

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_skills(self, text):
        """
        Extract skills from resume text using keyword matching
        Returns: List of tuples (skill, category, confidence)
        """
        technical_skills = ['python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'node.js', 
                           'c++', 'c#', 'typescript', 'angular', 'vue', 'django', 'flask', 'spring',
                           'mongodb', 'mysql', 'postgresql', 'aws', 'docker', 'kubernetes', 'git']
        
        soft_skills = ['communication', 'teamwork', 'leadership', 'problem solving', 'creativity',
                      'adaptability', 'time management', 'critical thinking', 'collaboration',
                      'presentation', 'negotiation', 'decision making']
        
        found_skills = []
        text_lower = text.lower()
        
        # Check technical skills
        for skill in technical_skills:
            if f" {skill} " in f" {text_lower} ":
                found_skills.append((skill, 'technical', 1.0))
            elif skill in text_lower:
                found_skills.append((skill, 'technical', 0.5))
        
        # Check soft skills
        for skill in soft_skills:
            if f" {skill} " in f" {text_lower} ":
                found_skills.append((skill, 'soft', 1.0))
            elif skill in text_lower:
                # Check for partial matches (e.g., "communicate" for "communication")
                if any(word.startswith(skill.split()[0]) for word in text_lower.split()):
                    found_skills.append((skill, 'soft', 0.5))
        
        return found_skills
    
    def parse_experience(self, text):
        """
        Parse experience level from resume text
        Returns: 'Entry', 'Mid', or 'Senior'
        """
        text_lower = text.lower()
        
        # Experience patterns
        senior_patterns = [
            r'(\d+)\+?\s*years?',
            r'senior\s+',
            r'lead\s+',
            r'principal\s+',
            r'manager',
            r'director',
            r'head\s+of'
        ]
        
        mid_patterns = [
            r'(\d+)\s*years?',
            r'mid[-\\s]level',
            r'experienced',
            r'professional'
        ]
        
        entry_patterns = [
            r'junior',
            r'entry[-\\s]level',
            r'fresh',
            r'graduate',
            r'intern'
        ]
        
        # Check for years of experience
        years_match = re.search(r'(\d+)\+?\s*years?', text_lower)
        if years_match:
            years = int(years_match.group(1))
            if years >= 5:
                return 'Senior'
            elif years >= 2:
                return 'Mid'
            else:
                return 'Entry'
        
        # Check for senior patterns
        for pattern in senior_patterns:
            if re.search(pattern, text_lower):
                return 'Senior'
        
        # Check for mid patterns
        for pattern in mid_patterns:
            if re.search(pattern, text_lower):
                return 'Mid'
        
        # Check for entry patterns
        for pattern in entry_patterns:
            if re.search(pattern, text_lower):
                return 'Entry'
        
        # Default to Entry level if no clear indicators
        return 'Entry'

# Test function
def test_parser():
    parser = ResumeParser()
    
    # Sample resume text for testing
    sample_resume = """
    John Doe
    Software Developer with 3 years of experience in Python and JavaScript.
    Skilled in React, Node.js, and SQL. Strong communication and teamwork abilities.
    Led a team of 3 developers on a major project.
    """
    
    skills = parser.extract_skills(sample_resume)
    experience = parser.parse_experience(sample_resume)
    
    print("Extracted Skills:", skills)
    print("Experience Level:", experience)

if __name__ == "__main__":
    test_parser()