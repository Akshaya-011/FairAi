import re
from typing import List, Dict, Tuple, Any, Set
from collections import defaultdict

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
                    'brother', 'sister', 'son', 'daughter', 'masculine', 'feminine'
                ],
                'pronouns': ['he', 'she', 'him', 'her', 'his', 'hers'],
                'descriptions': ['beautiful', 'handsome', 'pretty', 'strong man', 'gentle woman'],
                'phrases': ['family man', 'working mother', 'female intuition']
            },
            'age': {
                'keywords': [
                    'young', 'old', 'fresh', 'senior citizen', 'recent grad',
                    'retired', 'millennial', 'gen z', 'baby boomer', 'elderly',
                    'youthful', 'aged', 'junior', 'senior', 'seasoned',
                    'new graduate', 'recent college', 'digital native', 'over the hill'
                ],
                'phrases': ['too young', 'too old', 'years young', 'years old', 'set in their ways']
            },
            'ethnicity': {
                'keywords': [
                    'ethnicity', 'nationality', 'immigrant', 'native', 'foreign',
                    'race', 'racial', 'black', 'white', 'asian', 'hispanic',
                    'latino', 'latina', 'african', 'european', 'american',
                    'christian', 'muslim', 'jewish', 'hindu', 'buddhist',
                    'religious', 'religion', 'cultural background'
                ],
                'phrases': ['english only', 'native speaker', 'foreign accent', 'culturally fit']
            },
            'disability': {
                'keywords': [
                    'disabled', 'handicapped', 'crippled', 'mental health',
                    'depression', 'anxiety', 'therapy', 'medication', 'wheelchair',
                    'blind', 'deaf', 'autism', 'adhd', 'learning disability',
                    'special needs', 'handicap', 'mental illness'
                ],
                'phrases': ['suffers from', 'afflicted with', 'struggles with']
            },
            'appearance': {
                'keywords': [
                    'attractive', 'unattractive', 'beautiful', 'handsome',
                    'ugly', 'fat', 'overweight', 'skinny', 'thin', 'tall',
                    'short', 'height', 'weight', 'good-looking', 'physique'
                ]
            },
            'socioeconomic': {
                'keywords': [
                    'poor', 'rich', 'wealthy', 'privileged', 'disadvantaged',
                    'inner city', 'ghetto', 'ivy league', 'prestigious school',
                    'elite university', 'working class', 'upper class'
                ]
            }
        }
        
        self.job_relevant_terms = [
            'experience', 'skills', 'qualifications', 'education', 'training',
            'certifications', 'projects', 'achievements', 'responsibilities',
            'duties', 'technical', 'professional', 'work', 'job', 'career',
            'performance', 'results', 'accomplishments', 'expertise', 'knowledge',
            'abilities', 'competencies', 'proficiencies', 'capabilities'
        ]

        self.context_exceptions = {
            'required_skills': ['he', 'she', 'his', 'her'],  # Pronouns in required skills context
            'job_titles': ['senior', 'junior']  # Legitimate use in job titles
        }

    def detect_bias_in_text(self, text: str) -> Dict[str, Any]:
        """
        Enhanced bias detection with context awareness
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict containing bias types, offending phrases, and severity score
        """
        text_lower = text.lower()
        detected_bias = {
            'bias_types': [],
            'offending_phrases': [],
            'severity': 'None',
            'details': {},
            'bias_count': 0,
            'context_aware_analysis': {}
        }
        
        bias_count = 0
        bias_details = defaultdict(list)
        
        for bias_type, bias_data in self.biased_keywords.items():
            found_phrases = []
            
            # Check keywords with context awareness
            for keyword in bias_data.get('keywords', []):
                matches = self._find_keyword_with_context(keyword, text_lower)
                if matches:
                    found_phrases.extend(matches)
                    bias_count += len(matches)
            
            # Enhanced pronoun analysis for gender bias
            if bias_type == 'gender':
                pronoun_analysis = self._analyze_gender_pronouns(text_lower)
                if pronoun_analysis['bias_detected']:
                    found_phrases.append(pronoun_analysis['message'])
                    bias_count += pronoun_analysis['severity_level']
            
            # Check phrases
            for phrase in bias_data.get('phrases', []):
                if phrase in text_lower:
                    found_phrases.append(phrase)
                    bias_count += 1
            
            if found_phrases:
                detected_bias['bias_types'].append(bias_type)
                detected_bias['details'][bias_type] = found_phrases
                detected_bias['offending_phrases'].extend(found_phrases)
        
        # Calculate enhanced severity with density consideration
        detected_bias['bias_count'] = bias_count
        detected_bias['severity'] = self._calculate_enhanced_severity(bias_count, text)
        
        # Add context-aware analysis
        detected_bias['context_aware_analysis'] = self._analyze_context(text_lower)
        
        return detected_bias

    def analyze_question_fairness(self, question: str) -> Dict[str, Any]:
        """
        Enhanced question fairness analysis
        
        Args:
            question (str): Interview question to analyze
            
        Returns:
            Dict containing fairness score and analysis
        """
        bias_result = self.detect_bias_in_text(question)
        
        # Calculate job relevance with improved scoring
        job_relevance_score = self._calculate_enhanced_job_relevance(question)
        
        # Calculate fairness score (0-10) with more nuanced penalties
        base_score = 10.0
        
        # Increased Severity-based penalties
        severity_penalties = {
            'High': 6.0,  # Increased from 4.0
            'Medium': 3.0,  # Increased from 2.0
            'Low': 2.0,  # Increased from 1.0
            'None': 0.0
        }
        
        base_score -= severity_penalties[bias_result['severity']]
        
        # Additional penalty for multiple bias types
        if len(bias_result['bias_types']) > 1:
            base_score -= 2.0  # Increased from 1.0
        
        # Job relevance adjustments
        if job_relevance_score >= 0.8:
            base_score = min(10, base_score + 1.0)  # Reduced boost
        elif job_relevance_score >= 0.6:
            base_score = min(10, base_score + 0.3)  # Reduced boost
        elif job_relevance_score <= 0.3:
            base_score = max(0, base_score - 3.0)  # Increased penalty
        elif job_relevance_score <= 0.5:
            base_score = max(0, base_score - 2.0)  # Increased penalty
        
        # Ensure score is within bounds
        fairness_score = max(0.0, min(10.0, base_score))
        
        return {
            'fairness_score': round(fairness_score, 2),
            'bias_analysis': bias_result,
            'job_relevance': round(job_relevance_score, 2),
            'recommendation': self._get_enhanced_fairness_recommendation(fairness_score, bias_result, job_relevance_score),
            'improvement_suggestions': self._get_improvement_suggestions(bias_result, job_relevance_score)
        }

    def generate_bias_report(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive bias report for entire interview
        
        Args:
            interview_data (Dict): Interview data including questions, answers, etc.
            
        Returns:
            Dict containing bias metrics and recommendations
        """
        questions = interview_data.get('questions', [])
        total_questions = len(questions)
        
        if total_questions == 0:
            return {
                'error': 'No questions provided for analysis',
                'overall_fairness_score': 0,
                'total_questions_analyzed': 0
            }
        
        total_bias_count = 0
        bias_types_found = set()
        fairness_scores = []
        question_analyses = []
        
        # Analyze each question
        for i, question in enumerate(questions):
            question_analysis = self.analyze_question_fairness(question)
            fairness_scores.append(question_analysis['fairness_score'])
            question_analyses.append({
                'question_number': i + 1,
                'question': question,
                'analysis': question_analysis
            })
            
            bias_analysis = question_analysis['bias_analysis']
            total_bias_count += bias_analysis['bias_count']
            bias_types_found.update(bias_analysis['bias_types'])
        
        # Calculate comprehensive metrics
        avg_fairness = sum(fairness_scores) / len(fairness_scores)
        
        # Generate enhanced overall assessment
        overall_assessment = self._get_enhanced_overall_assessment(avg_fairness, total_bias_count, total_questions)
        
        return {
            'overall_fairness_score': round(avg_fairness, 2),
            'total_bias_instances': total_bias_count,
            'bias_types_detected': list(bias_types_found),
            'total_questions_analyzed': total_questions,
            'overall_assessment': overall_assessment,
            'recommendations': self._get_comprehensive_recommendations(bias_types_found, total_bias_count, avg_fairness),
            'detailed_metrics': {
                'average_fairness_per_question': round(avg_fairness, 2),
                'bias_density': round(total_bias_count / total_questions, 2),
                'fair_questions_count': len([score for score in fairness_scores if score >= 7]),
                'moderate_questions_count': len([score for score in fairness_scores if 5 <= score < 7]),
                'biased_questions_count': len([score for score in fairness_scores if score < 5]),
                'excellent_questions_count': len([score for score in fairness_scores if score >= 9])
            },
            'question_by_question_analysis': question_analyses
        }

    def _find_keyword_with_context(self, keyword: str, text: str) -> List[str]:
        """Find keywords with context awareness"""
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, text)
        
        # Filter out context exceptions
        filtered_matches = []
        for match in matches:
            if not self._is_context_exception(match, text):
                filtered_matches.append(match)
        
        return filtered_matches

    def _is_context_exception(self, keyword: str, text: str) -> bool:
        """Check if keyword usage is contextually appropriate"""
        # Check for legitimate use in required skills
        if keyword in self.context_exceptions['required_skills']:
            # If it's in a skills context, it might be acceptable
            skills_context = any(term in text for term in ['must', 'should', 'required', 'needs to'])
            return skills_context
        
        # Check for legitimate job title usage
        if keyword in self.context_exceptions['job_titles']:
            job_title_context = any(term in text for term in ['developer', 'engineer', 'analyst', 'manager'])
            return job_title_context
        
        return False

    def _analyze_gender_pronouns(self, text: str) -> Dict[str, Any]:
        """Enhanced gender pronoun analysis - MORE SENSITIVE"""
        male_pronouns = len(re.findall(r'\b(he|him|his)\b', text))
        female_pronouns = len(re.findall(r'\b(she|her|hers)\b', text))
        neutral_pronouns = len(re.findall(r'\b(they|them|their)\b', text))
        
        total_gender_pronouns = male_pronouns + female_pronouns
        
        if total_gender_pronouns == 0:
            return {'bias_detected': False, 'message': '', 'severity_level': 0}
        
        # MORE SENSITIVE: Detect any gender-specific pronoun usage
        if total_gender_pronouns > 0:
            dominant_gender = 'male' if male_pronouns > female_pronouns else 'female'
            imbalance_ratio = abs(male_pronouns - female_pronouns) / max(total_gender_pronouns, 1)
            
            # Flag if any gender-specific pronouns used without balance
            if imbalance_ratio > 0.7 or total_gender_pronouns >= 2:  # More sensitive thresholds
                return {
                    'bias_detected': True,
                    'message': f'Gender-specific pronouns detected: {male_pronouns} male, {female_pronouns} female, {neutral_pronouns} neutral',
                    'severity_level': min(3, total_gender_pronouns)  # Increased severity
                }
        
        # Detect repeated use without neutral alternatives
        if total_gender_pronouns >= 2 and neutral_pronouns == 0:  # Lowered threshold from 3 to 2
            return {
                'bias_detected': True,
                'message': f'Gender-specific pronouns used without neutral alternatives ({total_gender_pronouns} occurrences)',
                'severity_level': 2  # Increased from 1
            }
        
        return {'bias_detected': False, 'message': '', 'severity_level': 0}

    def _calculate_enhanced_severity(self, bias_count: int, text: str) -> str:
        """Calculate severity with text length consideration - LOWERED THRESHOLDS"""
        if bias_count == 0:
            return 'None'
        
        # Normalize by text length (words)
        word_count = len(text.split())
        normalized_bias = bias_count / max(word_count / 50, 1)  # Normalize to 50 words
        
        # LOWERED THRESHOLDS for more sensitive detection
        if normalized_bias <= 0.3:  # Lowered from 1.0
            return 'Low'
        elif normalized_bias <= 1.0:  # Lowered from 3.0
            return 'Medium'
        else:
            return 'High'

    def _calculate_enhanced_job_relevance(self, text: str) -> float:
        """Calculate enhanced job relevance score"""
        text_lower = text.lower()
        relevant_terms_found = 0
        total_terms_checked = len(self.job_relevant_terms)
        
        for term in self.job_relevant_terms:
            if self._exact_match(term, text_lower):
                relevant_terms_found += 1
        
        base_score = relevant_terms_found / total_terms_checked
        
        # Boost score for question markers
        question_indicators = ['describe', 'explain', 'how would', 'what would', 'tell me about']
        if any(indicator in text_lower for indicator in question_indicators):
            base_score = min(1.0, base_score + 0.1)
        
        return base_score

    def _analyze_context(self, text: str) -> Dict[str, Any]:
        """Analyze context for better bias understanding"""
        return {
            'is_question': any(marker in text for marker in ['?', 'how', 'what', 'why', 'describe', 'explain']),
            'contains_requirements': any(marker in text for marker in ['must', 'should', 'required', 'need to']),
            'text_complexity': 'high' if len(text.split()) > 25 else 'medium' if len(text.split()) > 10 else 'low'
        }

    def _get_enhanced_fairness_recommendation(self, score: float, bias_analysis: Dict, job_relevance: float) -> str:
        """Get enhanced recommendation based on multiple factors - STRICTER"""
        if score >= 9.5 and job_relevance >= 0.8:  # Stricter criteria
            return "Excellent - Question is highly fair and job-relevant"
        elif score >= 8.0:  # Stricter criteria
            return "Good - Minor improvements could enhance fairness"
        elif score >= 6.0:  # Stricter criteria
            return "Fair - Some bias concerns; consider rephrasing"
        else:
            bias_types = ", ".join(bias_analysis['bias_types'])
            return f"Poor - Significant bias detected ({bias_types}). Rewrite recommended."

    def _get_improvement_suggestions(self, bias_analysis: Dict, job_relevance: float) -> List[str]:
        """Get specific improvement suggestions"""
        suggestions = []
        
        if job_relevance < 0.5:  # Stricter threshold
            suggestions.append("Increase job relevance by focusing on specific skills and experiences")
        
        if bias_analysis['severity'] != 'None':
            suggestions.append("Use gender-neutral language and avoid demographic references")
            
            if 'gender' in bias_analysis['bias_types']:
                suggestions.append("Replace gender-specific pronouns with 'they/them' or restructure sentences")
            
            if 'age' in bias_analysis['bias_types']:
                suggestions.append("Focus on experience levels rather than age-related terms")
        
        if not suggestions:
            suggestions.append("Question is well-structured. Maintain current approach.")
        
        return suggestions

    def _get_enhanced_overall_assessment(self, avg_fairness: float, total_bias: int, total_questions: int) -> str:
        """Get enhanced overall assessment - STRICTER"""
        bias_density = total_bias / total_questions if total_questions > 0 else 0
        
        # STRICTER CRITERIA
        if avg_fairness >= 9.5 and bias_density == 0:  # Stricter
            return "EXCELLENT - Highly fair and professional interview process"
        elif avg_fairness >= 8.5 and bias_density <= 0.3:  # Stricter
            return "VERY GOOD - Strong fairness standards with minimal bias"
        elif avg_fairness >= 7.5 and bias_density <= 0.7:  # Stricter
            return "GOOD - Generally fair with minor areas for improvement"
        elif avg_fairness >= 6.5:  # Stricter
            return "FAIR - Some bias concerns; review and improve questions"
        elif avg_fairness >= 5.0:
            return "NEEDS IMPROVEMENT - Significant bias detected"
        else:
            return "POOR - Major fairness issues; complete review needed"

    def _exact_match(self, keyword: str, text: str) -> bool:
        """Check for exact word match using regex"""
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))

    def _get_comprehensive_recommendations(self, bias_types: set, total_bias: int, avg_fairness: float) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []
        
        if not bias_types and total_bias == 0 and avg_fairness >= 9.0:  # Stricter
            return ["Excellent! Interview process shows high fairness standards. Continue current practices."]
        
        # Specific bias type recommendations
        bias_recommendations = {
            'gender': [
                "Use gender-neutral language throughout all questions",
                "Avoid assumptions about family status or personal relationships",
                "Ensure balanced examples in scenario-based questions"
            ],
            'age': [
                "Remove all age-related terms and references",
                "Focus on experience levels and competencies rather than years",
                "Avoid terms that imply age preferences or stereotypes"
            ],
            'ethnicity': [
                "Eliminate all nationality, ethnicity, and religious references",
                "Focus on job-relevant language requirements only when essential",
                "Avoid cultural assumptions in all questions"
            ],
            'disability': [
                "Remove all health, disability, and medical references",
                "Focus on ability to perform essential job functions",
                "Ask about specific job requirements rather than general capabilities"
            ],
            'appearance': [
                "Eliminate all physical appearance and personal characteristic references",
                "Focus entirely on professional qualifications and competencies"
            ],
            'socioeconomic': [
                "Remove all socioeconomic and educational background references",
                "Focus on skills and experience rather than educational pedigree"
            ]
        }
        
        for bias_type in bias_types:
            if bias_type in bias_recommendations:
                recommendations.extend(bias_recommendations[bias_type])
        
        # General recommendations based on fairness score
        if avg_fairness < 7.5:  # Stricter threshold
            recommendations.extend([
                "Implement structured interview protocols for all positions",
                "Provide unconscious bias training for all interviewers",
                "Use scoring rubrics for consistent candidate evaluation",
                "Conduct regular audits of interview questions and processes"
            ])
        
        if total_bias > 3:  # Lowered threshold from 5
            recommendations.append("Consider using our question rewriting service to eliminate bias")
        
        return recommendations

# Enhanced utility functions
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

def get_bias_detection_metrics() -> Dict[str, Any]:
    """Get information about the bias detection capabilities"""
    detector = BiasDetector()
    return {
        'bias_categories_detected': list(detector.biased_keywords.keys()),
        'total_keywords_monitored': sum(len(data.get('keywords', [])) for data in detector.biased_keywords.values()),
        'job_relevance_terms': detector.job_relevant_terms,
        'version': '2.1.0',  # Updated version
        'features': [
            'Enhanced sensitive bias detection',
            'Lowered detection thresholds', 
            'Stricter fairness assessment',
            'Context-aware analysis',
            'Comprehensive reporting',
            'Improvement suggestions'
        ]
    }