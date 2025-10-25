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

        # Add audio/video specific bias patterns
        self.audio_bias_patterns = {
            'speaking_pace': {
                'too_slow': {'threshold': 100, 'message': 'Slow speaking pace may disadvantage fast-speaking candidates'},
                'too_fast': {'threshold': 200, 'message': 'Fast speaking pace may disadvantage deliberate speakers'}
            },
            'clarity': {
                'low_clarity': {'threshold': 4, 'message': 'Low audio clarity may affect comprehension'}
            },
            'energy': {
                'low_energy': {'threshold': 3, 'message': 'Low voice energy may be misinterpreted as low confidence'}
            }
        }
        
        self.video_bias_patterns = {
            'facial_expressions': {
                'negative_emotions': ['angry', 'sad', 'fear', 'disgust'],
                'message': 'Negative facial expressions may trigger unconscious bias'
            },
            'engagement': {
                'low_engagement': {'threshold': 0.3, 'message': 'Low engagement may be due to technical issues or cultural differences'}
            },
            'visibility': {
                'low_visibility': {'threshold': 0.5, 'message': 'Poor visibility may disadvantage candidates with suboptimal setup'}
            }
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

    # NEW AUDIO/VIDEO BIAS DETECTION METHODS

    def detect_audio_biases(self, speech_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect tone-related biases in audio analysis
        
        Args:
            speech_analysis: Output from audio_video_processor.analyze_speech_patterns()
            
        Returns:
            Dict containing audio bias analysis
        """
        if not speech_analysis.get('success', False):
            return {
                'biases_detected': [],
                'severity': 'None',
                'recommendations': ['Audio analysis unavailable - ensure good recording quality'],
                'bias_count': 0,
                'metrics_summary': {}
            }
        
        biases = []
        bias_count = 0
        
        # Speaking pace bias
        wpm = speech_analysis['speaking_pace_wpm']
        if wpm > 0:  # Only if we have valid WPM data
            if wpm < self.audio_bias_patterns['speaking_pace']['too_slow']['threshold']:
                biases.append({
                    'type': 'Speaking Pace',
                    'severity': 'Low',
                    'message': self.audio_bias_patterns['speaking_pace']['too_slow']['message'],
                    'metric': f"{wpm:.1f} WPM",
                    'category': 'Audio',
                    'suggestion': 'Focus on content quality rather than speaking speed'
                })
                bias_count += 1
            elif wpm > self.audio_bias_patterns['speaking_pace']['too_fast']['threshold']:
                biases.append({
                    'type': 'Speaking Pace', 
                    'severity': 'Low',
                    'message': self.audio_bias_patterns['speaking_pace']['too_fast']['message'],
                    'metric': f"{wpm:.1f} WPM",
                    'category': 'Audio',
                    'suggestion': 'Ensure comprehension of rapid speech'
                })
                bias_count += 1
        
        # Clarity bias
        clarity = speech_analysis['clarity_score']
        if clarity < self.audio_bias_patterns['clarity']['low_clarity']['threshold']:
            biases.append({
                'type': 'Voice Clarity',
                'severity': 'Medium',
                'message': self.audio_bias_patterns['clarity']['low_clarity']['message'],
                'metric': f"{clarity:.1f}/10",
                'category': 'Audio',
                'suggestion': 'Provide transcript or allow text follow-up for clarity'
            })
            bias_count += 1
        
        # Energy bias (confidence proxy)
        energy = speech_analysis.get('energy_score', 5)
        if energy < self.audio_bias_patterns['energy']['low_energy']['threshold']:
            biases.append({
                'type': 'Voice Energy',
                'severity': 'Low',
                'message': self.audio_bias_patterns['energy']['low_energy']['message'],
                'metric': f"{energy:.1f}/10",
                'category': 'Audio',
                'suggestion': 'Avoid equating voice energy with confidence or competence'
            })
            bias_count += 1
        
        # Calculate overall severity
        severity = self._calculate_audio_video_severity(bias_count)
        
        return {
            'biases_detected': biases,
            'bias_count': bias_count,
            'severity': severity,
            'recommendations': self._get_audio_bias_recommendations(biases),
            'metrics_summary': {
                'speaking_pace_wpm': wpm,
                'clarity_score': clarity,
                'energy_score': energy
            }
        }

    def detect_video_biases(self, video_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect visual biases in video analysis
        
        Args:
            video_analysis: Output from audio_video_processor.analyze_video_feed()
            
        Returns:
            Dict containing video bias analysis
        """
        if not video_analysis.get('success', False):
            return {
                'biases_detected': [],
                'severity': 'None',
                'recommendations': ['Video analysis unavailable - ensure good camera setup'],
                'bias_count': 0,
                'metrics_summary': {}
            }
        
        biases = []
        bias_count = 0
        
        # Facial expression bias
        emotion = video_analysis['facial_expression']
        if emotion in self.video_bias_patterns['facial_expressions']['negative_emotions']:
            biases.append({
                'type': 'Facial Expression',
                'severity': 'Medium',
                'message': self.video_bias_patterns['facial_expressions']['message'],
                'metric': emotion.title(),
                'category': 'Video',
                'suggestion': 'Evaluate content objectively regardless of facial expressions'
            })
            bias_count += 1
        
        # Engagement bias
        engagement = video_analysis['engagement_score']
        if engagement < self.video_bias_patterns['engagement']['low_engagement']['threshold']:
            biases.append({
                'type': 'Engagement Level',
                'severity': 'Low', 
                'message': self.video_bias_patterns['engagement']['low_engagement']['message'],
                'metric': f"{engagement:.1f}/1.0",
                'category': 'Video',
                'suggestion': 'Consider technical or cultural factors affecting engagement'
            })
            bias_count += 1
        
        # Visibility bias
        face_ratio = video_analysis['face_detection_ratio']
        if face_ratio < self.video_bias_patterns['visibility']['low_visibility']['threshold']:
            biases.append({
                'type': 'Visibility',
                'severity': 'Low',
                'message': self.video_bias_patterns['visibility']['low_visibility']['message'],
                'metric': f"{face_ratio*100:.1f}%",
                'category': 'Video',
                'suggestion': 'Provide clear technical requirements for video setup'
            })
            bias_count += 1
        
        # Calculate overall severity
        severity = self._calculate_audio_video_severity(bias_count)
        
        return {
            'biases_detected': biases,
            'bias_count': bias_count,
            'severity': severity,
            'recommendations': self._get_video_bias_recommendations(biases),
            'metrics_summary': {
                'facial_expression': emotion,
                'engagement_score': engagement,
                'face_detection_ratio': face_ratio
            }
        }

    def analyze_communication_skills(self, speech_analysis: Dict[str, Any], video_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive communication skills analysis
        
        Args:
            speech_analysis: Audio analysis results
            video_analysis: Video analysis results
            
        Returns:
            Dict containing communication skills assessment
        """
        analysis = {
            'audio_insights': [],
            'video_insights': [],
            'overall_assessment': '',
            'improvement_areas': [],
            'strengths': []
        }
        
        # Audio analysis insights
        if speech_analysis.get('success', False):
            wpm = speech_analysis['speaking_pace_wpm']
            if wpm > 0:
                if 120 <= wpm <= 180:
                    analysis['audio_insights'].append(f"🎯 **Speaking Pace**: Optimal ({wpm:.0f} WPM)")
                    analysis['strengths'].append('Excellent speaking pace')
                elif wpm < 120:
                    analysis['audio_insights'].append(f"⚡ **Speaking Pace**: Slow ({wpm:.0f} WPM) - consider practicing pace")
                    analysis['improvement_areas'].append('Speaking pace could be more dynamic')
                else:
                    analysis['audio_insights'].append(f"🐢 **Speaking Pace**: Fast ({wpm:.0f} WPM) - good for engagement")
                    analysis['strengths'].append('Engaging speaking pace')
            
            pause_freq = speech_analysis['pause_frequency']
            if pause_freq < 0.5:
                analysis['audio_insights'].append("💬 **Pause Frequency**: Low - shows confidence and fluency")
                analysis['strengths'].append('Confident speech flow')
            elif pause_freq < 2:
                analysis['audio_insights'].append("💬 **Pause Frequency**: Moderate - good for emphasis")
            else:
                analysis['audio_insights'].append("💬 **Pause Frequency**: High - consider reducing filler pauses")
                analysis['improvement_areas'].append('Reduce frequent pausing')
            
            clarity = speech_analysis['clarity_score']
            if clarity >= 8:
                analysis['audio_insights'].append(f"🎙️ **Clarity Score**: {clarity:.1f}/10 - Excellent articulation")
                analysis['strengths'].append('Clear and articulate speech')
            elif clarity >= 6:
                analysis['audio_insights'].append(f"🎙️ **Clarity Score**: {clarity:.1f}/10 - Good clarity")
            else:
                analysis['audio_insights'].append(f"🎙️ **Clarity Score**: {clarity:.1f}/10 - Needs improvement")
                analysis['improvement_areas'].append('Improve speech clarity')
        
        # Video analysis insights
        if video_analysis.get('success', False):
            engagement = video_analysis['engagement_score'] * 100
            if engagement >= 70:
                analysis['video_insights'].append(f"👀 **Engagement**: {engagement:.0f}% - Excellent presence")
                analysis['strengths'].append('Strong camera presence')
            elif engagement >= 50:
                analysis['video_insights'].append(f"👀 **Engagement**: {engagement:.0f}% - Good engagement") 
            else:
                analysis['video_insights'].append(f"👀 **Engagement**: {engagement:.0f}% - Could improve camera presence")
                analysis['improvement_areas'].append('Enhance video engagement')
            
            emotion = video_analysis['facial_expression']
            positive_emotions = ['happy', 'neutral']
            if emotion in positive_emotions:
                analysis['video_insights'].append(f"😊 **Facial Expressions**: {emotion.title()} - professional demeanor")
                analysis['strengths'].append('Professional presentation')
            else:
                analysis['video_insights'].append(f"😐 **Facial Expressions**: {emotion.title()} - maintain neutral expression")
                analysis['improvement_areas'].append('Maintain neutral professional expression')
            
            face_ratio = video_analysis['face_detection_ratio'] * 100
            if face_ratio >= 80:
                analysis['video_insights'].append("📷 **Visibility**: Excellent - clearly visible throughout")
            elif face_ratio >= 60:
                analysis['video_insights'].append("📷 **Visibility**: Good - generally visible")
            else:
                analysis['video_insights'].append("📷 **Visibility**: Low - ensure good lighting and camera position")
                analysis['improvement_areas'].append('Improve video setup for better visibility')
        
        # Generate overall assessment
        if analysis['strengths'] and not analysis['improvement_areas']:
            analysis['overall_assessment'] = "Excellent communication skills across all dimensions"
        elif analysis['strengths'] and analysis['improvement_areas']:
            analysis['overall_assessment'] = "Good communication skills with specific areas for enhancement"
        else:
            analysis['overall_assessment'] = "Communication skills need development across multiple areas"
        
        return analysis

    def generate_comprehensive_av_report(self, speech_analysis: Dict[str, Any], video_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive audio/video analysis report
        
        Args:
            speech_analysis: Audio analysis results
            video_analysis: Video analysis results
            
        Returns:
            Dict containing complete AV analysis
        """
        audio_biases = self.detect_audio_biases(speech_analysis)
        video_biases = self.detect_video_biases(video_analysis)
        communication_skills = self.analyze_communication_skills(speech_analysis, video_analysis)
        
        # Calculate overall fairness score
        total_bias_count = audio_biases['bias_count'] + video_biases['bias_count']
        overall_severity = self._calculate_audio_video_severity(total_bias_count)
        
        return {
            'overall_assessment': {
                'total_bias_instances': total_bias_count,
                'overall_severity': overall_severity,
                'communication_skills_level': 'Excellent' if len(communication_skills['strengths']) >= 3 else 
                                            'Good' if len(communication_skills['strengths']) >= 1 else 
                                            'Needs Improvement'
            },
            'audio_analysis': {
                'bias_detection': audio_biases,
                'technical_metrics': speech_analysis if speech_analysis.get('success') else {}
            },
            'video_analysis': {
                'bias_detection': video_biases,
                'technical_metrics': video_analysis if video_analysis.get('success') else {}
            },
            'communication_skills': communication_skills,
            'recommendations': self._get_comprehensive_av_recommendations(audio_biases, video_biases, communication_skills)
        }

    # HELPER METHODS FOR AUDIO/VIDEO

    def _calculate_audio_video_severity(self, bias_count: int) -> str:
        """Calculate severity for audio/video biases"""
        if bias_count == 0:
            return 'None'
        elif bias_count == 1:
            return 'Low'
        elif bias_count <= 3:
            return 'Medium'
        else:
            return 'High'

    def _get_audio_bias_recommendations(self, biases: List[Dict]) -> List[str]:
        """Get recommendations for audio biases"""
        recommendations = []
        
        for bias in biases:
            if bias['type'] == 'Speaking Pace':
                recommendations.append("Evaluate candidates based on content quality, not speaking speed")
            elif bias['type'] == 'Voice Clarity':
                recommendations.append("Provide transcripts for audio responses to ensure fair evaluation")
            elif bias['type'] == 'Voice Energy':
                recommendations.append("Avoid associating voice energy levels with confidence or competence")
        
        if not recommendations:
            recommendations.append("Audio presentation shows no significant bias concerns")
        
        return recommendations

    def _get_video_bias_recommendations(self, biases: List[Dict]) -> List[str]:
        """Get recommendations for video biases"""
        recommendations = []
        
        for bias in biases:
            if bias['type'] == 'Facial Expression':
                recommendations.append("Focus on verbal content rather than facial expressions during evaluation")
            elif bias['type'] == 'Engagement Level':
                recommendations.append("Consider cultural differences in eye contact and engagement styles")
            elif bias['type'] == 'Visibility':
                recommendations.append("Provide clear technical requirements for video interviews")
        
        if not recommendations:
            recommendations.append("Video presentation shows no significant bias concerns")
        
        return recommendations

    def _get_comprehensive_av_recommendations(self, audio_biases: Dict, video_biases: Dict, communication_skills: Dict) -> List[str]:
        """Get comprehensive recommendations for audio/video analysis"""
        recommendations = []
        
        # Add audio recommendations
        recommendations.extend(audio_biases['recommendations'])
        
        # Add video recommendations
        recommendations.extend(video_biases['recommendations'])
        
        # Add communication skills recommendations
        if communication_skills['improvement_areas']:
            for area in communication_skills['improvement_areas']:
                recommendations.append(f"Focus on improving: {area}")
        
        # Remove duplicates
        return list(set(recommendations))

    # EXISTING HELPER METHODS (keep these as they are)

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

def detect_audio_biases(speech_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to detect audio biases"""
    detector = BiasDetector()
    return detector.detect_audio_biases(speech_analysis)

def detect_video_biases(video_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to detect video biases"""
    detector = BiasDetector()
    return detector.detect_video_biases(video_analysis)

def analyze_communication_skills(speech_analysis: Dict[str, Any], video_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to analyze communication skills"""
    detector = BiasDetector()
    return detector.analyze_communication_skills(speech_analysis, video_analysis)

def generate_comprehensive_av_report(speech_analysis: Dict[str, Any], video_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to generate comprehensive AV report"""
    detector = BiasDetector()
    return detector.generate_comprehensive_av_report(speech_analysis, video_analysis)

def get_bias_detection_metrics() -> Dict[str, Any]:
    """Get information about the bias detection capabilities"""
    detector = BiasDetector()
    return {
        'bias_categories_detected': list(detector.biased_keywords.keys()),
        'total_keywords_monitored': sum(len(data.get('keywords', [])) for data in detector.biased_keywords.values()),
        'job_relevance_terms': detector.job_relevant_terms,
        'audio_bias_patterns': list(detector.audio_bias_patterns.keys()),
        'video_bias_patterns': list(detector.video_bias_patterns.keys()),
        'version': '3.0.0',  # Updated version with AV support
        'features': [
            'Enhanced sensitive bias detection',
            'Lowered detection thresholds', 
            'Stricter fairness assessment',
            'Context-aware analysis',
            'Comprehensive reporting',
            'Improvement suggestions',
            'Audio bias detection',
            'Video bias detection',
            'Communication skills analysis',
            'Multimodal bias assessment'
        ]
    }