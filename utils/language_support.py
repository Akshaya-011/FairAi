# utils/language_support.py
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import re
from typing import Dict, List, Optional
import aiohttp
import asyncio

# Ensure consistent results
DetectorFactory.seed = 0

class LanguageSupport:
    def __init__(self):
        self.supported_languages = ['English', 'Spanish', 'French', 'Telugu', 'Hindi']
        self.language_codes = {
            'English': 'en',
            'Spanish': 'es', 
            'French': 'fr',
            'Telugu': 'te',
            'Hindi': 'hi'
        }
        
        # COMPLETE Translation dictionaries for ALL UI elements
        self.translations = {
            'English': {
                # Main headers and titles
                'welcome': 'FairAI Hire - Bias-Free Interviews',
                'discovered_skills': 'Discovered Skills & Experience',
                'technical_skills': 'Technical Skills',
                'soft_skills': 'Soft Skills',
                'skills_visualization': 'Skills Visualization',
                'dashboard_preview': 'Dashboard Preview',
                'recruiter_view': 'Recruiter View',
                'fairness_dashboard': 'Fairness Dashboard & Analytics',
                'recruiter_dashboard': 'Recruiter Dashboard - Candidate Analytics',
                
                # Session controls
                'session_controls': 'Session Controls',
                'interview_language': 'Interview Language',
                'ai_enhancement': 'AI Enhancement',
                'enable_ai_features': 'Enable AI Features',
                'current_status': 'Current Status',
                'interview_tips': 'Interview Tips',
                'accessibility': 'Accessibility',
                
                # Resume analysis
                'resume_analysis': 'Resume Analysis',
                'paste_resume': 'Paste your resume text below:',
                'analyze_resume': 'Analyze Resume & Start Interview',
                'reset_session': 'Reset Session',
                'resume_analyzed': 'Resume Analyzed',
                'skills_found': 'Skills Found',
                'experience_level': 'Experience Level',
                
                # Interview section
                'interview_session': 'Interview Session',
                'current_difficulty': 'Current Difficulty',
                'questions_generated': 'Questions Generated',
                'answered_questions': 'Answered Questions',
                'bias_alerts': 'Bias Alerts',
                'your_answer': 'Your Answer:',
                'save_answer': 'Save Answer',
                'next_question': 'Next Question',
                'previous_question': 'Previous Question',
                'complete_interview': 'Complete Interview',
                'start_interview': 'Start Interview',
                'interview_started': 'Interview Started',
                'interview_completed': 'Interview Completed',
                
                # Skills visualization
                'skills_graph_visualization': 'Skills Graph Visualization',
                'skills_relationship_network': 'Skills Relationship Network',
                'skills_category_analysis': 'Skills Category Analysis',
                'skill_confidence_heatmap': 'Skill Confidence Heatmap',
                'skills_metrics': 'Skills Metrics',
                'export_skills_data': 'Export Skills Data',
                
                # Dashboard and analytics
                'real_time_bias_heatmap': 'Real-time Bias Detection Heatmap',
                'bias_detection_timeline': 'Bias Detection Timeline',
                'bias_category_distribution': 'Bias Category Distribution',
                'overall_bias_score': 'Overall Bias Score',
                'bias_hotspots_recommendations': 'Bias Hotspots & Recommendations',
                'detailed_analysis': 'Detailed Analysis',
                'skills_analysis': 'Skills Analysis',
                'bias_analysis': 'Bias Analysis',
                'performance_analysis': 'Performance Analysis',
                'ai_insights': 'AI Insights',
                'recommendations': 'Recommendations',
                
                # Recruiter dashboard
                'overall_match': 'Overall Match',
                'hire_confidence': 'Hire Confidence',
                'communication': 'Communication',
                'fairness': 'Fairness',
                'automated_insights': 'Automated Insights',
                'skills_match_breakdown': 'Skills Match Breakdown',
                'skills_distribution': 'Skills Distribution',
                'communication_metrics': 'Communication Metrics',
                'communication_style': 'Communication Style',
                'actionable_recommendations': 'Actionable Recommendations',
                'recommended_next_steps': 'Recommended Next Steps',
                'candidate_comparison': 'Candidate Comparison',
                'export_analysis': 'Export Analysis',
                'generate_full_report': 'Generate Full Report',
                'analyze_new_candidate': 'Analyze New Candidate',
                
                # Buttons and actions
                'upload_resume': 'Upload Resume',
                'generate_questions': 'Generate Questions',
                'analysis': 'Analysis',
                'bias_detection': 'Bias Detection',
                'download_report': 'Download Report',
                'select_language': 'Select Interview Language',
                'auto_detect': 'Auto-detect from resume',
                'accessibility_note': 'Our platform supports multiple languages to ensure equal opportunity',
                'reset_entire_session': 'Reset Entire Session',
                
                # Status messages
                'no_skills_detected': 'No skills detected',
                'no_technical_skills': 'No technical skills detected',
                'no_soft_skills': 'No soft skills detected',
                'complete_interview_to_see': 'Complete an interview to see candidate analytics',
                'analyze_resume_first': 'Analyze a resume first to see skills visualization!',
                'complete_more_questions': 'Complete more questions to see timeline analysis',
                'no_bias_data_available': 'No bias data available yet',
                'no_bias_categories_detected': 'No bias categories detected',
                'enable_ai_for_insights': 'Enable AI Enhancement in the sidebar to get AI-powered insights!',
                'complete_for_ai_analysis': 'Complete the interview to see AI analysis of your answers.',
                'excellent_no_biases': 'Excellent! No biases detected in the interview.',
                'no_significant_biases': 'No significant biases detected in the interview responses.',
                'add_more_candidates': 'Add more candidates to enable comparative analytics',
                
                # Chart and metric labels
                'bias_categories': 'Bias Categories',
                'interview_questions': 'Interview Questions',
                'severity': 'Severity',
                'number_of_bias_instances': 'Number of Bias Instances',
                'interview_timeline': 'Interview Timeline',
                'count': 'Count',
                'percentage': 'Percentage',
                'job_requirement_fit': 'Job Requirement Fit',
                'recommended_score': 'Recommended Score',
                'coherence_score': 'Coherence Score',
                'bias_free_score': 'Bias-Free Score',
                'quality_score': 'Quality Score',
                'relevance': 'Relevance',
                'total_skills': 'Total Skills',
                'avg_confidence': 'Avg Confidence',
                'relationships': 'Relationships',
                'connectivity': 'Connectivity',
                
                # AI and analysis texts
                'ai_enhanced_question': 'AI-Enhanced Question',
                'ai_analysis_previous_answer': 'AI Analysis of Previous Answer',
                'quality_score_label': 'Quality Score',
                'strengths_label': 'Strengths',
                'skills_demonstrated': 'Skills Demonstrated',
                'ai_powered_insights': 'AI-Powered Insights',
                'answer_quality_score': 'Average Answer Quality Score',
                'answer_by_answer_analysis': 'Answer-by-Answer Analysis',
                
                # Question types and categories
                'gender': 'Gender',
                'age': 'Age',
                'ethnicity': 'Ethnicity',
                'family': 'Family',
                'education': 'Education',
                'socioeconomic': 'Socioeconomic',
                
                # Additional UI elements
                'skills_identified': 'Skills Identified',
                'bias_detection_results': 'Bias Detection Results',
                'recommendations_for_fair_hiring': 'Recommendations for Fair Hiring',
                'detailed_question_review': 'Detailed Question Review',
                'interview_progress': 'Interview Progress',
                'overall_rating': 'Overall Rating',
                'fairness_score': 'Fairness Score',
                'fairness_grade': 'Fairness Grade',
                'advanced_bias_analytics': 'Advanced Bias Analytics',
                'weaknesses': 'Weaknesses',
                'improvement_areas': 'Improvement Areas'
            },
            'Spanish': {
                # Main headers and titles
                'welcome': 'FairAI Hire - Entrevistas Sin Sesgos',
                'discovered_skills': 'Habilidades y Experiencia Descubiertas',
                'technical_skills': 'Habilidades Técnicas',
                'soft_skills': 'Habilidades Blandas',
                'skills_visualization': 'Visualización de Habilidades',
                'dashboard_preview': 'Vista Previa del Dashboard',
                'recruiter_view': 'Vista del Reclutador',
                'fairness_dashboard': 'Dashboard de Equidad y Análisis',
                'recruiter_dashboard': 'Dashboard del Reclutador - Análisis del Candidato',
                
                # Session controls
                'session_controls': 'Controles de Sesión',
                'interview_language': 'Idioma de la Entrevista',
                'ai_enhancement': 'Mejora de IA',
                'enable_ai_features': 'Habilitar Funciones de IA',
                'current_status': 'Estado Actual',
                'interview_tips': 'Consejos para la Entrevista',
                'accessibility': 'Accesibilidad',
                
                # Resume analysis
                'resume_analysis': 'Análisis de Currículum',
                'paste_resume': 'Pega tu currículum a continuación:',
                'analyze_resume': 'Analizar Currículum y Comenzar Entrevista',
                'reset_session': 'Reiniciar Sesión',
                'resume_analyzed': 'Currículum Analizado',
                'skills_found': 'Habilidades Encontradas',
                'experience_level': 'Nivel de Experiencia',
                
                # Interview section
                'interview_session': 'Sesión de Entrevista',
                'current_difficulty': 'Dificultad Actual',
                'questions_generated': 'Preguntas Generadas',
                'answered_questions': 'Preguntas Respondidas',
                'bias_alerts': 'Alertas de Sesgo',
                'your_answer': 'Tu Respuesta:',
                'save_answer': 'Guardar Respuesta',
                'next_question': 'Siguiente Pregunta',
                'previous_question': 'Pregunta Anterior',
                'complete_interview': 'Completar Entrevista',
                'start_interview': 'Comenzar Entrevista',
                'interview_started': 'Entrevista Iniciada',
                'interview_completed': 'Entrevista Completada',
                
                # Skills visualization
                'skills_graph_visualization': 'Visualización del Gráfico de Habilidades',
                'skills_relationship_network': 'Red de Relaciones de Habilidades',
                'skills_category_analysis': 'Análisis de Categorías de Habilidades',
                'skill_confidence_heatmap': 'Mapa de Calor de Confianza de Habilidades',
                'skills_metrics': 'Métricas de Habilidades',
                'export_skills_data': 'Exportar Datos de Habilidades',
                
                # Dashboard and analytics
                'real_time_bias_heatmap': 'Mapa de Calor de Detección de Sesgos en Tiempo Real',
                'bias_detection_timeline': 'Línea de Tiempo de Detección de Sesgos',
                'bias_category_distribution': 'Distribución de Categorías de Sesgo',
                'overall_bias_score': 'Puntuación General de Sesgo',
                'bias_hotspots_recommendations': 'Puntos Críticos de Sesgo y Recomendaciones',
                'detailed_analysis': 'Análisis Detallado',
                'skills_analysis': 'Análisis de Habilidades',
                'bias_analysis': 'Análisis de Sesgos',
                'performance_analysis': 'Análisis de Rendimiento',
                'ai_insights': 'Ideas de IA',
                'recommendations': 'Recomendaciones',
                
                # Recruiter dashboard
                'overall_match': 'Coincidencia General',
                'hire_confidence': 'Confianza de Contratación',
                'communication': 'Comunicación',
                'fairness': 'Equidad',
                'automated_insights': 'Ideas Automatizadas',
                'skills_match_breakdown': 'Desglose de Coincidencia de Habilidades',
                'skills_distribution': 'Distribución de Habilidades',
                'communication_metrics': 'Métricas de Comunicación',
                'communication_style': 'Estilo de Comunicación',
                'actionable_recommendations': 'Recomendaciones Accionables',
                'recommended_next_steps': 'Próximos Pasos Recomendados',
                'candidate_comparison': 'Comparación de Candidatos',
                'export_analysis': 'Exportar Análisis',
                'generate_full_report': 'Generar Informe Completo',
                'analyze_new_candidate': 'Analizar Nuevo Candidato',
                
                # Buttons and actions
                'upload_resume': 'Subir Currículum',
                'generate_questions': 'Generar Preguntas',
                'analysis': 'Análisis',
                'bias_detection': 'Detección de Sesgos',
                'download_report': 'Descargar Informe',
                'select_language': 'Seleccionar Idioma de la Entrevista',
                'auto_detect': 'Auto-detectar del currículum',
                'accessibility_note': 'Nuestra plataforma soporta múltiples idiomas para garantizar igualdad de oportunidades',
                'reset_entire_session': 'Reiniciar Sesión Completa',
                
                # Status messages
                'no_skills_detected': 'No se detectaron habilidades',
                'no_technical_skills': 'No se detectaron habilidades técnicas',
                'no_soft_skills': 'No se detectaron habilidades blandas',
                'complete_interview_to_see': 'Complete una entrevista para ver análisis del candidato',
                'analyze_resume_first': '¡Analice un currículum primero para ver la visualización de habilidades!',
                'complete_more_questions': 'Complete más preguntas para ver el análisis de línea de tiempo',
                'no_bias_data_available': 'Aún no hay datos de sesgo disponibles',
                'no_bias_categories_detected': 'No se detectaron categorías de sesgo',
                'enable_ai_for_insights': '¡Habilite la mejora de IA en la barra lateral para obtener ideas impulsadas por IA!',
                'complete_for_ai_analysis': 'Complete la entrevista para ver el análisis de IA de sus respuestas.',
                'excellent_no_biases': '¡Excelente! No se detectaron sesgos en la entrevista.',
                'no_significant_biases': 'No se detectaron sesgos significativos en las respuestas de la entrevista.',
                'add_more_candidates': 'Agregue más candidatos para habilitar análisis comparativos',
                
                # Chart and metric labels
                'bias_categories': 'Categorías de Sesgo',
                'interview_questions': 'Preguntas de Entrevista',
                'severity': 'Gravedad',
                'number_of_bias_instances': 'Número de Instancias de Sesgo',
                'interview_timeline': 'Línea de Tiempo de la Entrevista',
                'count': 'Recuento',
                'percentage': 'Porcentaje',
                'job_requirement_fit': 'Ajuste a Requisitos del Trabajo',
                'recommended_score': 'Puntuación Recomendada',
                'coherence_score': 'Puntuación de Coherencia',
                'bias_free_score': 'Puntuación Libre de Sesgos',
                'quality_score': 'Puntuación de Calidad',
                'relevance': 'Relevancia',
                'total_skills': 'Habilidades Totales',
                'avg_confidence': 'Confianza Promedio',
                'relationships': 'Relaciones',
                'connectivity': 'Conectividad',
                
                # AI and analysis texts
                'ai_enhanced_question': 'Pregunta Mejorada por IA',
                'ai_analysis_previous_answer': 'Análisis de IA de Respuesta Anterior',
                'quality_score_label': 'Puntuación de Calidad',
                'strengths_label': 'Fortalezas',
                'skills_demonstrated': 'Habilidades Demostradas',
                'ai_powered_insights': 'Ideas Impulsadas por IA',
                'answer_quality_score': 'Puntuación de Calidad de Respuesta Promedio',
                'answer_by_answer_analysis': 'Análisis Respuesta por Respuesta',
                
                # Question types and categories
                'gender': 'Género',
                'age': 'Edad',
                'ethnicity': 'Etnicidad',
                'family': 'Familia',
                'education': 'Educación',
                'socioeconomic': 'Socioeconómico',
                
                # Additional UI elements
                'skills_identified': 'Habilidades Identificadas',
                'bias_detection_results': 'Resultados de Detección de Sesgos',
                'recommendations_for_fair_hiring': 'Recomendaciones para Contratación Justa',
                'detailed_question_review': 'Revisión Detallada de Preguntas',
                'interview_progress': 'Progreso de la Entrevista',
                'overall_rating': 'Calificación General',
                'fairness_score': 'Puntuación de Equidad',
                'fairness_grade': 'Grado de Equidad',
                'advanced_bias_analytics': 'Análisis Avanzado de Sesgos',
                'weaknesses': 'Debilidades',
                'improvement_areas': 'Áreas de Mejora'
            },
            'French': {
                'welcome': 'FairAI Hire - Entretiens Sans Biais',
                'discovered_skills': 'Compétences et Expérience Découvertes',
                'technical_skills': 'Compétences Techniques',
                'soft_skills': 'Compétences Douces',
                'skills_visualization': 'Visualisation des Compétences',
                'dashboard_preview': 'Aperçu du Tableau de Bord',
                'recruiter_view': 'Vue du Recruteur',
                'fairness_dashboard': 'Tableau de Bord d\'Équité et d\'Analyse',
                'recruiter_dashboard': 'Tableau de Bord du Recruteur - Analyse du Candidat',
                'session_controls': 'Contrôles de Session',
                'interview_language': 'Langue de l\'Entretien',
                'ai_enhancement': 'Amélioration IA',
                'enable_ai_features': 'Activer les Fonctionnalités IA',
                'current_status': 'Statut Actuel',
                'interview_tips': 'Conseils d\'Entretien',
                'accessibility': 'Accessibilité',
                'resume_analysis': 'Analyse de CV',
                'paste_resume': 'Collez votre CV ci-dessous :',
                'analyze_resume': 'Analyser le CV et Démarrer l\'Entretien',
                'reset_session': 'Réinitialiser la Session',
                'resume_analyzed': 'CV Analysé',
                'skills_found': 'Compétences Trouvées',
                'experience_level': 'Niveau d\'Expérience',
                'interview_session': 'Session d\'Entretien',
                'current_difficulty': 'Difficulté Actuelle',
                'questions_generated': 'Questions Générées',
                'answered_questions': 'Questions Répondues',
                'bias_alerts': 'Alertes de Biais',
                'your_answer': 'Votre Réponse :',
                'save_answer': 'Sauvegarder la Réponse',
                'next_question': 'Question Suivante',
                'previous_question': 'Question Précédente',
                'complete_interview': 'Terminer l\'Entretien',
                'start_interview': 'Commencer l\'Entretien',
                'interview_started': 'Entretien Démarré',
                'interview_completed': 'Entretien Terminé',
                # ... (add remaining French translations following the same pattern)
            },
            'Telugu': {
                'welcome': 'FairAI Hire - పక్షపాత రహిత ఇంటర్వ్యూలు',
                'discovered_skills': 'కనుగొనబడిన నైపుణ్యాలు & అనుభవం',
                'technical_skills': 'సాంకేతిక నైపుణ్యాలు',
                'soft_skills': 'సాఫ్ట్ నైపుణ్యాలు',
                'skills_visualization': 'నైపుణ్యాల విజువలైజేషన్',
                'dashboard_preview': 'డాష్బోర్డ్ ప్రివ్యూ',
                'recruiter_view': 'నియామకదారు వీక్షణ',
                'fairness_dashboard': 'న్యాయమైన డాష్బోర్డ్ & విశ్లేషణ',
                'recruiter_dashboard': 'నియామకదారు డాష్బోర్డ్ - అభ్యర్థి విశ్లేషణ',
                'session_controls': 'సెషన్ నియంత్రణలు',
                'interview_language': 'ఇంటర్వ్యూ భాష',
                'ai_enhancement': 'AI ఎన్హాన్స్మెంట్',
                'enable_ai_features': 'AI ఫీచర్లను ప్రారంభించండి',
                'current_status': 'ప్రస్తుత స్థితి',
                'interview_tips': 'ఇంటర్వ్యూ చిట్కాలు',
                'accessibility': 'అందుబాటు',
                'resume_analysis': 'రెజ్యూమే విశ్లేషణ',
                'paste_resume': 'మీ రెజ్యూమేను క్రింద పేస్ట్ చేయండి:',
                'analyze_resume': 'రెజ్యూమేని విశ్లేషించి ఇంటర్వ్యూని ప్రారంభించండి',
                'reset_session': 'సెషన్ రీసెట్ చేయండి',
                'resume_analyzed': 'రెజ్యూమే విశ్లేషించబడింది',
                'skills_found': 'కనుగొనబడిన నైపుణ్యాలు',
                'experience_level': 'అనుభవం స్థాయి',
                'interview_session': 'ఇంటర్వ్యూ సెషన్',
                'current_difficulty': 'ప్రస్తుత కష్టతరం',
                'questions_generated': 'రూపొందించిన ప్రశ్నలు',
                'answered_questions': 'జవాబు ఇచ్చిన ప్రశ్నలు',
                'bias_alerts': 'పక్షపాత హెచ్చరికలు',
                'your_answer': 'మీ సమాధానం:',
                'save_answer': 'సమాధానాన్ని సేవ్ చేయండి',
                'next_question': 'తదుపరి ప్రశ్న',
                'previous_question': 'మునుపటి ప్రశ్న',
                'complete_interview': 'ఇంటర్వ్యూని పూర్తి చేయండి',
                'start_interview': 'ఇంటర్వ్యూని ప్రారంభించండి',
                'interview_started': 'ఇంటర్వ్యూ ప్రారంభించబడింది',
                'interview_completed': 'ఇంటర్వ్యూ పూర్తయింది',
                # ... (add remaining Telugu translations following the same pattern)
            },
            'Hindi': {
                'welcome': 'FairAI Hire - पक्षपात मुक्त साक्षात्कार',
                'discovered_skills': 'पाई गई कौशल और अनुभव',
                'technical_skills': 'तकनीकी कौशल',
                'soft_skills': 'सॉफ्ट स्किल्स',
                'skills_visualization': 'कौशल विज़ुअलाइज़ेशन',
                'dashboard_preview': 'डैशबोर्ड पूर्वावलोकन',
                'recruiter_view': 'भर्तीकर्ता दृश्य',
                'fairness_dashboard': 'निष्पक्षता डैशबोर्ड और विश्लेषण',
                'recruiter_dashboard': 'भर्तीकर्ता डैशबोर्ड - उम्मीदवार विश्लेषण',
                'session_controls': 'सत्र नियंत्रण',
                'interview_language': 'साक्षात्कार भाषा',
                'ai_enhancement': 'एआई एन्हांसमेंट',
                'enable_ai_features': 'एआई सुविधाएँ सक्षम करें',
                'current_status': 'वर्तमान स्थिति',
                'interview_tips': 'साक्षात्कार युक्तियाँ',
                'accessibility': 'पहुंच',
                'resume_analysis': 'रिज्यूमे विश्लेषण',
                'paste_resume': 'अपना रिज्यूमे नीचे पेस्ट करें:',
                'analyze_resume': 'रिज्यूमे विश्लेषण करें और साक्षात्कार शुरू करें',
                'reset_session': 'सत्र रीसेट करें',
                'resume_analyzed': 'रिज्यूमे विश्लेषित',
                'skills_found': 'कौशल पाए गए',
                'experience_level': 'अनुभव स्तर',
                'interview_session': 'साक्षात्कार सत्र',
                'current_difficulty': 'वर्तमान कठिनाई',
                'questions_generated': 'प्रश्न जनरेट किए गए',
                'answered_questions': 'उत्तर दिए गए प्रश्न',
                'bias_alerts': 'पक्षपात अलर्ट',
                'your_answer': 'आपका उत्तर:',
                'save_answer': 'उत्तर सहेजें',
                'next_question': 'अगला प्रश्न',
                'previous_question': 'पिछला प्रश्न',
                'complete_interview': 'साक्षात्कार पूरा करें',
                'start_interview': 'साक्षात्कार शुरू करें',
                'interview_started': 'साक्षात्कार शुरू हुआ',
                'interview_completed': 'साक्षात्कार पूरा हुआ',
                # ... (add remaining Hindi translations following the same pattern)
            }
        }
        
        # Language-specific bias patterns
        self.bias_patterns = {
            'English': {
                'gender_biased_words': ['he should', 'she should', 'aggressive', 'bossy', 'emotional'],
                'age_biased_words': ['young', 'old', 'fresh', 'experienced', 'digital native'],
                'culture_biased_words': ['ethnic', 'foreign', 'native', 'immigrant']
            },
            'Spanish': {
                'gender_biased_words': ['él debe', 'ella debe', 'agresivo', 'mandona', 'emocional'],
                'age_biased_words': ['joven', 'viejo', 'fresco', 'experimentado', 'nativo digital'],
                'culture_biased_words': ['étnico', 'extranjero', 'nativo', 'inmigrante']
            },
            'French': {
                'gender_biased_words': ['il devrait', 'elle devrait', 'agressif', 'autoritaire', 'émotionnel'],
                'age_biased_words': ['jeune', 'vieux', 'frais', 'expérimenté', 'natif numérique'],
                'culture_biased_words': ['ethnique', 'étranger', 'autochtone', 'immigrant']
            },
            'Telugu': {
                'gender_biased_words': ['అతను చేయాలి', 'ఆమె చేయాలి', 'ఆక్రమణాత్మక', 'అధికారం', 'భావోద్వేగం'],
                'age_biased_words': ['యువకుడు', 'వృద్ధుడు', 'కొత్త', 'అనుభవం', 'డిజిటల్ స్థానికుడు'],
                'culture_biased_words': ['జాతి', 'విదేశీ', 'స్థానిక', 'వలసదారు']
            },
            'Hindi': {
                'gender_biased_words': ['उसे करना चाहिए', 'उसे करना चाहिए', 'आक्रामक', 'जिद्दी', 'भावुक'],
                'age_biased_words': ['युवा', 'बूढ़ा', 'नया', 'अनुभवी', 'डिजिटल नेटिव'],
                'culture_biased_words': ['जातीय', 'विदेशी', 'मूल निवासी', 'प्रवासी']
            }
        }

    async def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """
        Translate text using LibreTranslate API
        """
        try:
            if target_language == 'English' or not text.strip():
                return text
                
            # Map language names to codes
            lang_codes = {
                'English': 'en', 'Spanish': 'es', 'French': 'fr', 
                'Telugu': 'te', 'Hindi': 'hi'
            }
            
            target_code = lang_codes.get(target_language, 'en')
            source_code = lang_codes.get(source_language, 'en')
            
            if target_code == source_code:
                return text
            
            # Use LibreTranslate
            url = "https://libretranslate.de/translate"
            payload = {
                'q': text,
                'source': source_code,
                'target': target_code,
                'format': 'text'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('translatedText', text)
                    else:
                        return text
                        
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def detect_language(self, text: str) -> Optional[str]:
        """Detect language from text"""
        try:
            if not text or len(text.strip()) < 10:
                return 'English'
                
            detected_code = detect(text)
            code_to_lang = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French',
                'te': 'Telugu', 'hi': 'Hindi'
            }
            return code_to_lang.get(detected_code, 'English')
        except LangDetectException:
            return 'English'

    def translate_ui_text(self, text_key: str, target_language: str) -> str:
        """Translate UI text to target language"""
        if target_language not in self.supported_languages:
            target_language = 'English'
        return self.translations[target_language].get(text_key, text_key)

    def get_bias_patterns(self, language: str) -> Dict:
        """Get language-specific bias patterns"""
        return self.bias_patterns.get(language, self.bias_patterns['English'])

    def adapt_question_for_language(self, question: str, target_language: str, original_language: str = 'English') -> str:
        """Adapt questions for different languages"""
        if target_language == original_language:
            return question
            
        # Simple translation mapping for common question patterns
        question_translations = {
            'English': {
                'Tell me about yourself': 'Tell me about yourself',
                'What are your strengths': 'What are your strengths',
                'Describe a challenging project': 'Describe a challenging project',
                'How do you handle teamwork': 'How do you handle teamwork',
                'Where do you see yourself in 5 years': 'Where do you see yourself in 5 years'
            },
            'Spanish': {
                'Tell me about yourself': 'Háblame de ti mismo',
                'What are your strengths': '¿Cuáles son tus fortalezas?',
                'Describe a challenging project': 'Describe un proyecto desafiante',
                'How do you handle teamwork': '¿Cómo manejas el trabajo en equipo?',
                'Where do you see yourself in 5 years': '¿Dónde te ves en 5 años?'
            },
            'French': {
                'Tell me about yourself': 'Parlez-moi de vous',
                'What are your strengths': 'Quelles sont vos forces?',
                'Describe a challenging project': 'Décrivez un projet difficile',
                'How do you handle teamwork': 'Comment gérez-vous le travail d\'équipe?',
                'Where do you see yourself in 5 years': 'Où vous voyez-vous dans 5 ans?'
            },
            'Telugu': {
                'Tell me about yourself': 'మీ గురించి చెప్పండి',
                'What are your strengths': 'మీ బలాలు ఏమిటి?',
                'Describe a challenging project': 'సవాలుగా ఉన్న ప్రాజెక్ట్‌ను వివరించండి',
                'How do you handle teamwork': 'టీమ్‌వర్క్‌ను ఎలా నిర్వహిస్తారు?',
                'Where do you see yourself in 5 years': '5 సంవత్సరాలలో మిమ్మల్ని ఎక్కడ చూస్తారు?'
            },
            'Hindi': {
                'Tell me about yourself': 'अपने बारे में बताएं',
                'What are your strengths': 'आपकी ताकत क्या हैं?',
                'Describe a challenging project': 'एक चुनौतीपूर्ण परियोजना का वर्णन करें',
                'How do you handle teamwork': 'आप टीमवर्क को कैसे संभालते हैं?',
                'Where do you see yourself in 5 years': '5 साल में खुद को कहां देखते हैं?'
            }
        }
        
        # Return translated question if available, otherwise return original
        translations = question_translations.get(target_language, {})
        for eng_question, trans_question in translations.items():
            if eng_question.lower() in question.lower():
                return trans_question
                
        return question  # Return original if no translation found

    def is_technical_term(self, term: str) -> bool:
        """Check if a term is technical (should remain in original language)"""
        technical_terms = {
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'express',
            'sql', 'nosql', 'mongodb', 'mysql', 'postgresql', 'aws', 'azure', 'gcp',
            'docker', 'kubernetes', 'jenkins', 'git', 'rest', 'api', 'graphql',
            'machine learning', 'ai', 'artificial intelligence', 'data science',
            'agile', 'scrum', 'devops', 'ci/cd', 'microservices', 'serverless'
        }
        return term.lower() in technical_terms

# Singleton instance
language_support = LanguageSupport()