import re
import spacy
from typing import Dict, List, Tuple
import json

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please install spaCy model: python -m spacy download en_core_web_sm")
    nlp = None

class SkillNode:
    def __init__(self, skill: str, category: str, confidence: float = 1.0):
        self.skill = skill
        self.category = category
        self.confidence = confidence
        self.related_skills = {}  # skill -> strength
        self.frequency = 1
    
    def add_relationship(self, skill: str, strength: float = 0.8):
        self.related_skills[skill] = strength

class ResumeParser:
    def __init__(self):
        self.skill_categories = {
            "technical": ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'sql', 'html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js', 'express', 'tensorflow', 'pytorch'],
            "soft": ['communication', 'teamwork', 'leadership', 'problem solving', 'creativity', 'adaptability', 'time management', 'collaboration']
        }
    
    def extract_skills(self, resume_text: str) -> List[Tuple[str, str, float]]:
        """Extract skills from resume text"""
        skills_found = []
        resume_lower = resume_text.lower()
        
        # Check for technical skills
        for skill in self.skill_categories["technical"]:
            if skill in resume_lower:
                # Calculate basic confidence
                confidence = 0.8
                # Increase confidence if skill appears multiple times
                frequency = resume_lower.count(skill)
                confidence = min(1.0, confidence + (frequency * 0.1))
                
                skills_found.append((skill, "technical", round(confidence, 2)))
        
        # Check for soft skills
        for skill in self.skill_categories["soft"]:
            if skill in resume_lower:
                confidence = 0.7
                frequency = resume_lower.count(skill)
                confidence = min(1.0, confidence + (frequency * 0.1))
                
                skills_found.append((skill, "soft", round(confidence, 2)))
        
        return skills_found
    
    def parse_experience(self, resume_text: str) -> str:
        """Parse experience level from resume text"""
        text_lower = resume_text.lower()
        
        # Look for experience indicators
        experience_indicators = {
            'senior': ['senior', 'lead', 'principal', 'architect', '10+', '10 years', 'fifteen', 'fifteen years'],
            'mid': ['mid-level', 'mid level', '3+', '5+', '5 years', 'three years', 'four years', 'experience'],
            'entry': ['junior', 'entry', 'graduate', 'recent grad', '0-2', '1-2', 'first role', 'beginner']
        }
        
        for level, indicators in experience_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    if level == 'senior':
                        return "Senior"
                    elif level == 'mid':
                        return "Mid"
                    elif level == 'entry':
                        return "Entry"
        
        # Default to Mid if no clear indicators
        return "Mid"

# Visualization functions (keep these for the graph features)
def build_skills_graph(resume_text: str) -> Dict[str, SkillNode]:
    """Build a comprehensive skills graph from resume text"""
    
    # Define skill categories and their keywords
    skill_categories = {
        "Programming": ["python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "sql", "html", "css"],
        "Frameworks": ["react", "angular", "vue", "django", "flask", "spring", "node.js", "express", "tensorflow", "pytorch"],
        "Tools": ["git", "docker", "kubernetes", "jenkins", "aws", "azure", "gcp", "linux", "unix"],
        "Data": ["sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "bigquery", "tableau"],
        "Soft Skills": ["communication", "teamwork", "leadership", "problem solving", "creativity", "adaptability", "time management"],
        "Methodologies": ["agile", "scrum", "kanban", "devops", "ci/cd", "tdd", "api design"]
    }
    
    # Skill relationships (which skills often go together)
    skill_relationships = {
        "python": ["django", "flask", "pandas", "numpy", "machine learning"],
        "javascript": ["react", "node.js", "vue", "angular", "html", "css"],
        "java": ["spring", "hibernate", "microservices"],
        "react": ["javascript", "redux", "html", "css"],
        "docker": ["kubernetes", "aws", "jenkins", "ci/cd"],
        "sql": ["mysql", "postgresql", "database design"],
        "aws": ["docker", "kubernetes", "linux", "devops"]
    }
    
    found_skills = {}
    resume_lower = resume_text.lower()
    
    # Extract skills by category
    for category, skills in skill_categories.items():
        for skill in skills:
            if skill in resume_lower:
                # Calculate confidence based on context
                confidence = 1.0
                context_words = resume_lower.split()
                skill_index = context_words.index(skill) if skill in context_words else -1
                
                if skill_index > 0:
                    # Check for proficiency indicators
                    proficiency_indicators = ["expert", "advanced", "proficient", "experienced", "skilled"]
                    context_window = context_words[max(0, skill_index-3):skill_index+1]
                    for indicator in proficiency_indicators:
                        if indicator in context_window:
                            confidence = min(1.0, confidence + 0.2)
                
                # Create skill node
                skill_node = SkillNode(skill, category, confidence)
                found_skills[skill] = skill_node
                
                # Add relationships
                if skill in skill_relationships:
                    for related_skill in skill_relationships[skill]:
                        if related_skill in found_skills:
                            skill_node.add_relationship(related_skill, 0.8)
    
    # Calculate frequencies and adjust confidence
    words = resume_lower.split()
    for skill_node in found_skills.values():
        frequency = words.count(skill_node.skill)
        skill_node.frequency = frequency
        skill_node.confidence = min(1.0, skill_node.confidence + (frequency * 0.1))
    
    return found_skills

def get_skills_by_category(skills_graph: Dict[str, SkillNode]) -> Dict[str, List[dict]]:
    """Organize skills by category for visualization"""
    categories = {}
    for skill_node in skills_graph.values():
        if skill_node.category not in categories:
            categories[skill_node.category] = []
        
        categories[skill_node.category].append({
            "skill": skill_node.skill,
            "confidence": skill_node.confidence,
            "frequency": skill_node.frequency,
            "related_count": len(skill_node.related_skills)
        })
    
    return categories

def calculate_skill_metrics(skills_graph: Dict[str, SkillNode]) -> dict:
    """Calculate overall skill metrics"""
    total_skills = len(skills_graph)
    avg_confidence = sum(node.confidence for node in skills_graph.values()) / total_skills if total_skills > 0 else 0
    total_relationships = sum(len(node.related_skills) for node in skills_graph.values())
    
    return {
        "total_skills": total_skills,
        "avg_confidence": round(avg_confidence, 2),
        "total_relationships": total_relationships,
        "connectivity_score": round(total_relationships / total_skills, 2) if total_skills > 0 else 0
    }