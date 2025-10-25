import re
from typing import List, Dict, Tuple, Any, Set
from collections import defaultdict

class BiasDetector:
    def __init__(self):
        # Your existing bias keywords (keep the same)
        self.biased_keywords = {
            'gender': {
                'keywords': [
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
        
        # Audio/Video bias patterns (simplified)
        self.audio_bias_patterns = {
            'speaking_pace': {
                'too_slow': {'threshold': 100, 'message': 'Slow speaking pace may disadvantage fast-speaking candidates'},
                'too_fast': {'threshold': 200, 'message': 'Fast speaking pace may disadvantage deliberate speakers'}
            },
            'clarity': {
                'low_clarity': {'threshold': 4, 'message': 'Low audio clarity may affect comprehension'}
            }
        }
        
        self.video_bias_patterns = {
            'engagement': {
                'low_engagement': {'threshold': 0.3, 'message': 'Low engagement may be due to technical issues or cultural differences'}
            },
            'visibility': {
                'low_visibility': {'threshold': 0.5, 'message': 'Poor visibility may disadvantage candidates with suboptimal setup'}
            }
        }

    def detect_audio_biases(self, speech_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Detect audio biases without DeepFace"""
        if not speech_analysis.get('success', False):
            return {
                'biases_detected': [],
                'severity': 'None',
                'recommendations': ['Audio analysis unavailable'],
                'bias_count': 0,
                'metrics_summary': {}
            }
        
        biases = []
        bias_count = 0
        
        # Speaking pace bias
        wpm = speech_analysis['speaking_pace_wpm']
        if wpm > 0:
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
        
        severity = self._calculate_audio_video_severity(bias_count)
        
        return {
            'biases_detected': biases,
            'bias_count': bias_count,
            'severity': severity,
            'recommendations': self._get_audio_bias_recommendations(biases),
            'metrics_summary': {
                'speaking_pace_wpm': wpm,
                'clarity_score': clarity
            }
        }

    def detect_video_biases(self, video_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Detect video biases without DeepFace"""
        if not video_analysis.get('success', False):
            return {
                'biases_detected': [],
                'severity': 'None',
                'recommendations': ['Video analysis unavailable'],
                'bias_count': 0,
                'metrics_summary': {}
            }
        
        biases = []
        bias_count = 0
        
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
        
        severity = self._calculate_audio_video_severity(bias_count)
        
        return {
            'biases_detected': biases,
            'bias_count': bias_count,
            'severity': severity,
            'recommendations': self._get_video_bias_recommendations(biases),
            'metrics_summary': {
                'facial_expression': video_analysis['facial_expression'],
                'engagement_score': engagement,
                'face_detection_ratio': face_ratio
            }
        }

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
        
        if not recommendations:
            recommendations.append("Audio presentation shows no significant bias concerns")
        
        return recommendations

    def _get_video_bias_recommendations(self, biases: List[Dict]) -> List[str]:
        """Get recommendations for video biases"""
        recommendations = []
        for bias in biases:
            if bias['type'] == 'Engagement Level':
                recommendations.append("Consider cultural differences in eye contact and engagement styles")
            elif bias['type'] == 'Visibility':
                recommendations.append("Provide clear technical requirements for video interviews")
        
        if not recommendations:
            recommendations.append("Video presentation shows no significant bias concerns")
        
        return recommendations

    def analyze_communication_skills(self, speech_analysis: Dict[str, Any], video_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze communication skills without DeepFace"""
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

# Keep your existing text bias detection methods here...
# (Copy all your existing detect_bias_in_text, analyze_question_fairness, etc. methods)

# Utility functions
def detect_audio_biases(speech_analysis: Dict[str, Any]) -> Dict[str, Any]:
    detector = BiasDetector()
    return detector.detect_audio_biases(speech_analysis)

def detect_video_biases(video_analysis: Dict[str, Any]) -> Dict[str, Any]:
    detector = BiasDetector()
    return detector.detect_video_biases(video_analysis)

def analyze_communication_skills(speech_analysis: Dict[str, Any], video_analysis: Dict[str, Any]) -> Dict[str, Any]:
    detector = BiasDetector()
    return detector.analyze_communication_skills(speech_analysis, video_analysis)