import re
from typing import List, Tuple, Dict, Any

class ResumeParser:
    def __init__(self):
        # Define skill keywords
        self.technical_skills = [
            'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 
            'node.js', 'typescript', 'angular', 'vue', 'django', 'flask',
            'spring', 'mongodb', 'mysql', 'postgresql', 'redis', 'docker',
            'kubernetes', 'aws', 'azure', 'gcp', 'linux', 'git', 'jenkins',
            'ci/cd', 'rest api', 'graphql', 'microservices', 'machine learning',
            'ai', 'data analysis', 'pandas', 'numpy', 'tensorflow', 'pytorch'
        ]
        
        self.soft_skills = [
            'communication', 'teamwork', 'leadership', 'problem solving',
            'creativity', 'adaptability', 'time management', 'critical thinking',
            'collaboration', 'presentation', 'negotiation', 'conflict resolution',
            'emotional intelligence', 'mentoring', 'project management'
        ]
    
    def extract_skills(self, text: str) -> List[Tuple[str, str, float]]:
        """Extract skills from resume text using keyword matching"""
        text_lower = text.lower()
        found_skills = []
        
        # Check technical skills
        for skill in self.technical_skills:
            if self._exact_match(skill, text_lower):
                confidence = self._calculate_confidence(skill, text)
                found_skills.append((skill, 'technical', confidence))
        
        # Check soft skills
        for skill in self.soft_skills:
            if self._exact_match(skill, text_lower):
                confidence = self._calculate_confidence(skill, text)
                found_skills.append((skill, 'soft', confidence))
        
        return found_skills
    
    def parse_experience(self, text: str) -> str:
        """Parse experience level from resume text"""
        text_lower = text.lower()
        
        # Experience patterns
        senior_patterns = [
            r'(\d+)\+?\s*years', r'(\d+)\+?\s*yr', r'senior', r'lead', r'principal',
            r'architect', r'experienced', r'expert', r'advanced'
        ]
        
        mid_patterns = [
            r'(\d+)\s*years', r'mid[- ]level', r'intermediate', r'professional'
        ]
        
        junior_patterns = [
            r'junior', r'entry[- ]level', r'fresh', r'graduate', r'student',
            r'intern', r'trainee', r'(\d)\s*year'
        ]
        
        # Check for senior level indicators
        for pattern in senior_patterns:
            if re.search(pattern, text_lower):
                if 'year' in pattern:
                    years = re.findall(r'(\d+)\+?\s*years?', text_lower)
                    if years and any(int(year) >= 5 for year in years):
                        return "Senior"
                else:
                    return "Senior"
        
        # Check for mid level indicators
        for pattern in mid_patterns:
            if re.search(pattern, text_lower):
                return "Mid"
        
        # Check for junior level indicators
        for pattern in junior_patterns:
            if re.search(pattern, text_lower):
                return "Entry"
        
        # Default based on content length and complexity
        word_count = len(text.split())
        if word_count > 500:
            return "Mid"
        else:
            return "Entry"
    
    def _exact_match(self, keyword: str, text: str) -> bool:
        """Check for exact word match using regex"""
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))
    
    def _calculate_confidence(self, skill: str, text: str) -> float:
        """Calculate confidence score for skill detection"""
        text_lower = text.lower()
        
        # Count occurrences
        pattern = r'\b' + re.escape(skill) + r'\b'
        occurrences = len(re.findall(pattern, text_lower))
        
        # Check context (nearby words that indicate proficiency)
        proficiency_indicators = ['proficient', 'skilled', 'experienced', 'expert', 'strong']
        context_boost = any(indicator in text_lower for indicator in proficiency_indicators)
        
        # Base confidence on frequency and context
        base_confidence = min(1.0, occurrences * 0.3)
        if context_boost:
            base_confidence = min(1.0, base_confidence + 0.2)
        
        return round(base_confidence, 2)

# Utility functions for skills graph (simplified)
def build_skills_graph(resume_text: str) -> Dict[str, Any]:
    """Build a simple skills graph from resume text"""
    parser = ResumeParser()
    skills = parser.extract_skills(resume_text)
    
    graph = {}
    for skill, category, confidence in skills:
        graph[skill] = {
            'skill': skill,
            'category': category,
            'confidence': confidence,
            'frequency': 1,
            'related_skills': []
        }
    
    return graph

def get_skills_by_category(skills_graph: Dict[str, Any]) -> Dict[str, List]:
    """Get skills organized by category"""
    categories = {
        'technical': [],
        'soft': []
    }
    
    for skill_data in skills_graph.values():
        category = skill_data['category']
        if category in categories:
            categories[category].append({
                'skill': skill_data['skill'],
                'confidence': skill_data['confidence']
            })
    
    return categories

def calculate_skill_metrics(skills_graph: Dict[str, Any]) -> Dict[str, float]:
    """Calculate skill metrics"""
    if not skills_graph:
        return {
            'total_skills': 0,
            'avg_confidence': 0,
            'total_relationships': 0,
            'connectivity_score': 0
        }
    
    total_skills = len(skills_graph)
    total_confidence = sum(skill['confidence'] for skill in skills_graph.values())
    avg_confidence = total_confidence / total_skills
    
    return {
        'total_skills': total_skills,
        'avg_confidence': round(avg_confidence, 2),
        'total_relationships': 0,  # Simplified version
        'connectivity_score': 0    # Simplified version
    }