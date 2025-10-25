import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Any
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import json

class AnalyticsEngine:
    def __init__(self):
        self.metrics_history = []
    
    def calculate_candidate_fit(self, skills_graph: Dict, job_requirements: Dict) -> Dict:
        """
        Calculate how well candidate matches job requirements
        """
        required_skills = job_requirements.get('required_skills', [])
        preferred_skills = job_requirements.get('preferred_skills', [])
        candidate_skills = skills_graph.get('demonstrated_skills', {})
        
        # Calculate required skills match
        required_match = 0
        required_total = len(required_skills)
        
        for skill in required_skills:
            if skill in candidate_skills:
                proficiency = candidate_skills[skill].get('proficiency', 0)
                required_match += min(proficiency / 100, 1.0)
        
        required_score = (required_match / required_total * 100) if required_total > 0 else 0
        
        # Calculate preferred skills match
        preferred_match = 0
        preferred_total = len(preferred_skills)
        
        for skill in preferred_skills:
            if skill in candidate_skills:
                proficiency = candidate_skills[skill].get('proficiency', 0)
                preferred_match += min(proficiency / 100, 0.5)  # Lower weight for preferred skills
        
        preferred_score = (preferred_match / preferred_total * 100) if preferred_total > 0 else 0
        
        # Overall match score
        overall_score = (required_score * 0.7) + (preferred_score * 0.3)
        
        # Skill gap analysis
        missing_required = [skill for skill in required_skills if skill not in candidate_skills]
        missing_preferred = [skill for skill in preferred_skills if skill not in candidate_skills]
        
        return {
            'overall_score': round(overall_score, 1),
            'required_skills_score': round(required_score, 1),
            'preferred_skills_score': round(preferred_score, 1),
            'missing_required_skills': missing_required,
            'missing_preferred_skills': missing_preferred,
            'strengths': self._identify_strengths(candidate_skills, required_skills + preferred_skills),
            'weaknesses': self._identify_weaknesses(candidate_skills, required_skills + preferred_skills)
        }
    
    def analyze_communication_skills(self, answers_data: List[Dict]) -> Dict:
        """
        Analyze communication skills from answer data
        """
        if not answers_data:
            return {}
        
        coherence_scores = []
        response_times = []
        answer_lengths = []
        confidence_indicators = []
        
        for answer in answers_data:
            # Answer coherence (based on length, structure, completeness)
            coherence = self._calculate_coherence(answer.get('text', ''))
            coherence_scores.append(coherence)
            
            # Response time analysis
            response_time = answer.get('response_time', 0)
            response_times.append(response_time)
            
            # Answer length analysis
            answer_length = len(answer.get('text', '').split())
            answer_lengths.append(answer_length)
            
            # Confidence indicators (based on language patterns)
            confidence = self._assess_confidence(answer.get('text', ''))
            confidence_indicators.append(confidence)
        
        # Calculate metrics
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0
        avg_response_time = np.mean(response_times) if response_times else 0
        avg_answer_length = np.mean(answer_lengths) if answer_lengths else 0
        avg_confidence = np.mean(confidence_indicators) if confidence_indicators else 0
        
        # Communication style classification
        communication_style = self._classify_communication_style(
            avg_coherence, avg_response_time, avg_answer_length, avg_confidence
        )
        
        return {
            'coherence_score': round(avg_coherence, 1),
            'avg_response_time_seconds': round(avg_response_time, 1),
            'avg_answer_length': round(avg_answer_length, 1),
            'confidence_level': round(avg_confidence, 1),
            'communication_style': communication_style,
            'improvement_areas': self._identify_communication_issues(
                coherence_scores, response_times, confidence_indicators
            )
        }
    
    def generate_improvement_recommendations(self, interview_data: Dict) -> List[str]:
        """
        Generate actionable improvement recommendations
        """
        recommendations = []
        
        # Analyze skills fit
        skills_fit = interview_data.get('skills_fit', {})
        if skills_fit.get('overall_score', 0) < 70:
            recommendations.append(
                f"Focus on developing required skills: {', '.join(skills_fit.get('missing_required_skills', []))}"
            )
        
        # Analyze communication
        communication = interview_data.get('communication_analysis', {})
        if communication.get('coherence_score', 0) < 60:
            recommendations.append("Work on structuring answers more clearly using STAR method (Situation, Task, Action, Result)")
        
        if communication.get('confidence_level', 0) < 50:
            recommendations.append("Practice speaking with more confidence and avoid tentative language")
        
        if communication.get('avg_response_time_seconds', 0) > 10:
            recommendations.append("Improve response time by practicing common interview questions")
        
        # Analyze bias patterns
        bias_data = interview_data.get('bias_analysis', {})
        if bias_data.get('total_biases', 0) > 0:
            recommendations.append("Review interview questions to reduce potential biases")
        
        # Add general recommendations
        recommendations.extend([
            "Prepare specific examples of past achievements and projects",
            "Research the company and role thoroughly before interviews",
            "Practice explaining technical concepts to non-technical audiences"
        ])
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def calculate_hire_confidence(self, analytics_data: Dict) -> float:
        """
        Calculate hire/no-hire confidence score
        """
        skills_score = analytics_data.get('skills_fit', {}).get('overall_score', 0)
        communication_score = analytics_data.get('communication_analysis', {}).get('coherence_score', 0)
        confidence_level = analytics_data.get('communication_analysis', {}).get('confidence_level', 0)
        
        # Weighted average with emphasis on skills
        hire_score = (skills_score * 0.5) + (communication_score * 0.3) + (confidence_level * 0.2)
        
        return round(hire_score, 1)
    
    def generate_comparative_analytics(self, candidates_data: List[Dict]) -> Dict:
        """
        Generate comparative analytics for multiple candidates
        """
        if len(candidates_data) < 2:
            return {}
        
        comparison = {
            'candidates_ranked': [],
            'skills_comparison': {},
            'performance_metrics': {},
            'diversity_metrics': self._calculate_diversity_metrics(candidates_data)
        }
        
        # Rank candidates by overall score
        ranked_candidates = sorted(
            candidates_data,
            key=lambda x: x.get('analytics', {}).get('skills_fit', {}).get('overall_score', 0),
            reverse=True
        )
        
        for i, candidate in enumerate(ranked_candidates):
            comparison['candidates_ranked'].append({
                'candidate_id': candidate.get('candidate_id', f'candidate_{i}'),
                'rank': i + 1,
                'overall_score': candidate.get('analytics', {}).get('skills_fit', {}).get('overall_score', 0),
                'hire_confidence': candidate.get('analytics', {}).get('hire_confidence', 0)
            })
        
        # Skills comparison
        all_skills = set()
        for candidate in candidates_data:
            skills = candidate.get('skills_graph', {}).get('demonstrated_skills', {})
            all_skills.update(skills.keys())
        
        for skill in all_skills:
            comparison['skills_comparison'][skill] = []
            for candidate in candidates_data:
                skills_data = candidate.get('skills_graph', {}).get('demonstrated_skills', {})
                proficiency = skills_data.get(skill, {}).get('proficiency', 0)
                comparison['skills_comparison'][skill].append(proficiency)
        
        return comparison
    
    def _calculate_coherence(self, text: str) -> float:
        """Calculate answer coherence score"""
        if not text:
            return 0
        
        words = text.split()
        sentences = text.split('.')
        
        # Simple coherence metrics
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        unique_word_ratio = len(set(words)) / len(words) if words else 0
        
        # Score based on structure (simplified)
        score = min(avg_sentence_length / 20 * 40, 40)  # Sentence length factor
        score += min(unique_word_ratio * 30, 30)  # Vocabulary diversity
        score += 30 if len(sentences) >= 2 else 0  # Multi-sentence bonus
        
        return min(score, 100)
    
    def _assess_confidence(self, text: str) -> float:
        """Assess confidence level from text"""
        confident_indicators = ['achieved', 'successfully', 'led', 'managed', 'implemented', 'created']
        tentative_indicators = ['maybe', 'perhaps', 'I think', 'not sure', 'kind of', 'sort of']
        
        text_lower = text.lower()
        confident_count = sum(1 for word in confident_indicators if word in text_lower)
        tentative_count = sum(1 for word in tentative_indicators if word in text_lower)
        
        total_indicators = confident_count + tentative_count
        if total_indicators == 0:
            return 50  # Neutral
        
        confidence_ratio = confident_count / total_indicators
        return confidence_ratio * 100
    
    def _classify_communication_style(self, coherence: float, response_time: float, 
                                    answer_length: float, confidence: float) -> str:
        """Classify communication style"""
        if coherence > 70 and confidence > 70:
            return "Articulate and Confident"
        elif coherence > 70 and confidence <= 70:
            return "Clear but Hesitant"
        elif coherence <= 70 and confidence > 70:
            return "Confident but Unstructured"
        else:
            return "Needs Development"
    
    def _identify_strengths(self, candidate_skills: Dict, required_skills: List) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        for skill in required_skills:
            if skill in candidate_skills:
                proficiency = candidate_skills[skill].get('proficiency', 0)
                if proficiency >= 70:
                    strengths.append(skill)
        return strengths[:3]  # Top 3 strengths
    
    def _identify_weaknesses(self, candidate_skills: Dict, required_skills: List) -> List[str]:
        """Identify candidate weaknesses"""
        weaknesses = []
        for skill in required_skills:
            if skill in candidate_skills:
                proficiency = candidate_skills[skill].get('proficiency', 0)
                if proficiency < 50:
                    weaknesses.append(skill)
            else:
                weaknesses.append(skill)
        return weaknesses[:3]  # Top 3 weaknesses
    
    def _identify_communication_issues(self, coherence_scores: List[float], 
                                     response_times: List[float], 
                                     confidence_scores: List[float]) -> List[str]:
        """Identify communication improvement areas"""
        issues = []
        
        avg_coherence = np.mean(coherence_scores) if coherence_scores else 0
        avg_response_time = np.mean(response_times) if response_times else 0
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
        
        if avg_coherence < 60:
            issues.append("Answer structure and clarity")
        if avg_response_time > 8:
            issues.append("Response time")
        if avg_confidence < 60:
            issues.append("Confidence and assertiveness")
        
        return issues
    
    def _calculate_diversity_metrics(self, candidates_data: List[Dict]) -> Dict:
        """Calculate diversity metrics across candidate pool"""
        # This would integrate with your bias detection system
        # Simplified version for demonstration
        total_candidates = len(candidates_data)
        
        # Mock diversity metrics - in real implementation, this would come from candidate profiles
        return {
            'total_candidates': total_candidates,
            'gender_diversity': 'Medium',  # Would be calculated from actual data
            'experience_variance': 'High',
            'background_diversity': 'Medium'
        }