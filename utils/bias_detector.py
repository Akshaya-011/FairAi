import re
from typing import List, Dict, Tuple, Any

class BiasDetector:
    def __init__(self):
        self.biased_keywords = {
            'gender': {
                'keywords': [
                    # Gender-specific terms
                    'pregnant', 'maternity', 'paternity', 'husband', 'wife', 
                    'boyfriend', 'girlfriend', 'boy', 'girl', 'he should', 
                    'she should', 'he must', 'she must', 'male', 'female',
                    'mother', 'father', 'mom', 'dad', 'grandmother', 'grandfather',
                    'brother', 'sister', 'son', 'daughter'
                ],
                'pronouns': ['he', 'she', 'him', 'her', 'his', 'hers'],
                'descriptions': ['beautiful', 'handsome', 'pretty', 'strong man', 'gentle woman']
            },
            'age': {
                'keywords': [
                    'young', 'old', 'fresh', 'senior citizen', 'recent grad',
                    'retired', 'millennial', 'gen z', 'baby boomer', 'elderly',
                    'youthful', 'aged', 'junior', 'senior', 'seasoned',
                    'new graduate', 'recent college', 'digital native'
                ],
                'phrases': ['too young', 'too old', 'years young', 'years old']
            },
            'ethnicity': {
                'keywords': [
                    'ethnicity', 'nationality', 'immigrant', 'native', 'foreign',
                    'race', 'racial', 'black', 'white', 'asian', 'hispanic',
                    'latino', 'latina', 'african', 'european', 'american',
                    'christian', 'muslim', 'jewish', 'hindu', 'buddhist',
                    'religious', 'religion'
                ],
                'phrases': ['english only', 'native speaker', 'foreign accent']
            },
            'disability': {
                'keywords': [
                    'disabled', 'handicapped', 'crippled', 'mental health',
                    'depression', 'anxiety', 'therapy', 'medication', 'wheelchair',
                    'blind', 'deaf', 'autism', 'adhd', 'learning disability'
                ]
            },
            'appearance': {
                'keywords': [
                    'attractive', 'unattractive', 'beautiful', 'handsome',
                    'ugly', 'fat', 'overweight', 'skinny', 'thin', 'tall',
                    'short', 'height', 'weight'
                ]
            }
        }
        
        self.job_relevant_terms = [
            'experience', 'skills', 'qualifications', 'education', 'training',
            'certifications', 'projects', 'achievements', 'responsibilities',
            'duties', 'technical', 'professional', 'work', 'job', 'career'
        ]

    def detect_bias_in_text(self, text: str) -> Dict[str, Any]:
        """
        Scan input text for biased keywords and phrases
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict containing bias types, offending phrases, and severity score
        """
        text_lower = text.lower()
        detected_bias = {
            'bias_types': [],
            'offending_phrases': [],
            'severity': 'Low',
            'details': {}
        }
        
        bias_count = 0
        
        for bias_type, bias_data in self.biased_keywords.items():
            found_phrases = []
            
            # Check keywords
            for keyword in bias_data.get('keywords', []):
                if self._exact_match(keyword, text_lower):
                    found_phrases.append(keyword)
                    bias_count += 1
            
            # Check pronouns (for gender bias)
            if bias_type == 'gender':
                pronoun_count = 0
                for pronoun in bias_data.get('pronouns', []):
                    pronoun_count += len(re.findall(r'\b' + pronoun + r'\b', text_lower))
                
                # If only one gender pronoun is used repeatedly, flag it
                if pronoun_count >= 2:
                    found_phrases.append(f"Repeated gender-specific pronouns ({pronoun_count} occurrences)")
                    bias_count += 1
            
            # Check phrases
            for phrase in bias_data.get('phrases', []):
                if phrase in text_lower:
                    found_phrases.append(phrase)
                    bias_count += 1
            
            if found_phrases:
                detected_bias['bias_types'].append(bias_type)
                detected_bias['details'][bias_type] = found_phrases
                detected_bias['offending_phrases'].extend(found_phrases)
        
        # Calculate severity
        if bias_count == 0:
            detected_bias['severity'] = 'None'
        elif bias_count <= 2:
            detected_bias['severity'] = 'Low'
        elif bias_count <= 5:
            detected_bias['severity'] = 'Medium'
        else:
            detected_bias['severity'] = 'High'
        
        detected_bias['bias_count'] = bias_count
        
        return detected_bias

    def analyze_question_fairness(self, question: str) -> Dict[str, Any]:
        """
        Analyze if a question is fair and job-relevant
        
        Args:
            question (str): Interview question to analyze
            
        Returns:
            Dict containing fairness score and analysis
        """
        bias_result = self.detect_bias_in_text(question)
        
        # Calculate job relevance
        job_relevance_score = self._calculate_job_relevance(question)
        
        # Calculate fairness score (0-10)
        base_score = 10
        
        # Penalize for bias
        if bias_result['severity'] == 'High':
            base_score -= 4
        elif bias_result['severity'] == 'Medium':
            base_score -= 2
        elif bias_result['severity'] == 'Low':
            base_score -= 1
        
        # Reward for job relevance
        if job_relevance_score >= 0.7:
            base_score = min(10, base_score + 1)
        elif job_relevance_score <= 0.3:
            base_score = max(0, base_score - 2)
        
        # Ensure score is within bounds
        fairness_score = max(0, min(10, base_score))
        
        return {
            'fairness_score': fairness_score,
            'bias_analysis': bias_result,
            'job_relevance': job_relevance_score,
            'recommendation': self._get_fairness_recommendation(fairness_score, bias_result)
        }

    def generate_bias_report(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive bias report for entire interview
        
        Args:
            interview_data (Dict): Interview data including questions, answers, etc.
            
        Returns:
            Dict containing bias metrics and recommendations
        """
        total_questions = len(interview_data.get('questions', []))
        total_bias_count = 0
        bias_types_found = set()
        fairness_scores = []
        
        # Analyze each question
        for question in interview_data.get('questions', []):
            fairness_analysis = self.analyze_question_fairness(question)
            fairness_scores.append(fairness_analysis['fairness_score'])
            
            bias_analysis = fairness_analysis['bias_analysis']
            total_bias_count += bias_analysis['bias_count']
            bias_types_found.update(bias_analysis['bias_types'])
        
        # Calculate averages
        avg_fairness = sum(fairness_scores) / len(fairness_scores) if fairness_scores else 10
        
        # Generate overall assessment
        overall_assessment = self._get_overall_assessment(avg_fairness, total_bias_count)
        
        return {
            'overall_fairness_score': round(avg_fairness, 2),
            'total_bias_instances': total_bias_count,
            'bias_types_detected': list(bias_types_found),
            'total_questions_analyzed': total_questions,
            'overall_assessment': overall_assessment,
            'recommendations': self._get_comprehensive_recommendations(bias_types_found, total_bias_count),
            'detailed_metrics': {
                'average_fairness_per_question': round(avg_fairness, 2),
                'bias_density': round(total_bias_count / max(total_questions, 1), 2),
                'fair_questions_count': len([score for score in fairness_scores if score >= 7]),
                'biased_questions_count': len([score for score in fairness_scores if score < 5])
            }
        }

    def _exact_match(self, keyword: str, text: str) -> bool:
        """Check for exact word match using regex"""
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))

    def _calculate_job_relevance(self, text: str) -> float:
        """Calculate how job-relevant the text is"""
        text_lower = text.lower()
        relevant_terms_found = 0
        
        for term in self.job_relevant_terms:
            if self._exact_match(term, text_lower):
                relevant_terms_found += 1
        
        return relevant_terms_found / len(self.job_relevant_terms)

    def _get_fairness_recommendation(self, score: float, bias_analysis: Dict) -> str:
        """Get recommendation based on fairness score"""
        if score >= 9:
            return "Excellent - Question is fair and job-relevant"
        elif score >= 7:
            return "Good - Minor improvements possible"
        elif score >= 5:
            return "Fair - Consider rephrasing for better fairness"
        else:
            bias_types = ", ".join(bias_analysis['bias_types'])
            return f"Poor - Significant bias detected ({bias_types}). Rewrite the question."

    def _get_overall_assessment(self, avg_fairness: float, total_bias: int) -> str:
        """Get overall assessment of the interview"""
        if avg_fairness >= 8.5 and total_bias == 0:
            return "EXCELLENT - Highly fair and unbiased interview"
        elif avg_fairness >= 7 and total_bias <= 2:
            return "GOOD - Mostly fair with minor bias concerns"
        elif avg_fairness >= 5 and total_bias <= 5:
            return "FAIR - Some bias detected, needs improvement"
        else:
            return "POOR - Significant bias concerns, major improvements needed"

    def _get_comprehensive_recommendations(self, bias_types: set, total_bias: int) -> List[str]:
        """Generate comprehensive recommendations for fairer interviewing"""
        recommendations = []
        
        if not bias_types and total_bias == 0:
            return ["Excellent! No bias detected. Continue with current practices."]
        
        if 'gender' in bias_types:
            recommendations.extend([
                "Use gender-neutral language (they/them instead of he/she)",
                "Avoid assumptions about family status or personal relationships",
                "Focus on skills and qualifications rather than personal characteristics"
            ])
        
        if 'age' in bias_types:
            recommendations.extend([
                "Remove age-related terms from questions",
                "Focus on experience and skills rather than years",
                "Avoid terms that imply age preferences"
            ])
        
        if 'ethnicity' in bias_types:
            recommendations.extend([
                "Eliminate nationality and ethnicity references",
                "Focus on job-relevant language requirements only",
                "Avoid cultural assumptions in questions"
            ])
        
        if 'disability' in bias_types:
            recommendations.extend([
                "Remove all health and disability references",
                "Focus on ability to perform job functions with reasonable accommodations",
                "Ask about specific job requirements rather than general health"
            ])
        
        if 'appearance' in bias_types:
            recommendations.extend([
                "Eliminate all physical appearance references",
                "Focus entirely on professional qualifications",
                "Ensure questions are relevant to job performance"
            ])
        
        # General recommendations
        recommendations.extend([
            "Use structured interview questions for all candidates",
            "Focus on job-relevant skills and experiences",
            "Train interviewers on unconscious bias awareness",
            "Use rubrics for consistent evaluation across candidates"
        ])
        
        return recommendations

# Utility function for easy use
def detect_bias_in_text(text: str) -> Dict[str, Any]:
    """Convenience function to detect bias in text"""
    detector = BiasDetector()
    return detector.detect_bias_in_text(text)

def analyze_question_fairness(question: str) -> Dict[str, Any]:
    """Convenience function to analyze question fairness"""
    detector = BiasDetector()
    return detector.analyze_question_fairness(question)

def generate_bias_report(interview_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to generate bias report"""
    detector = BiasDetector()
    return detector.generate_bias_report(interview_data)