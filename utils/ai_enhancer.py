import subprocess
import json
import re
import logging
from typing import Dict, List, Optional

class AIEnhancer:
    def __init__(self, model_name: str = "llama2:7b"):
        """
        Initialize the AI Enhancer with Ollama
        
        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name
        self.available = self._check_ollama_availability()
        
        if self.available:
            logging.info(f"Ollama is available with model: {model_name}")
        else:
            logging.warning("Ollama not available. AI enhancement features will be disabled.")
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    def _call_ollama(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Call Ollama model with a prompt
        
        Args:
            prompt: The input prompt for the model
            max_tokens: Maximum tokens to generate
            
        Returns:
            Model response or None if failed
        """
        if not self.available:
            return None
            
        try:
            # Prepare the request for Ollama
            request = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.3
                }
            }
            
            # Call Ollama via subprocess
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logging.error(f"Ollama error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logging.error("Ollama request timed out")
            return None
        except Exception as e:
            logging.error(f"Error calling Ollama: {e}")
            return None
    
    def improve_question(self, question: str, context: str = "") -> Dict[str, str]:
        """
        Enhance a question to make it more effective and fair
        
        Args:
            question: Original question to improve
            context: Optional context about the role/skills
            
        Returns:
            Dictionary with improved question and explanation
        """
        if not self.available:
            return {
                "improved_question": question,
                "explanation": "AI enhancement not available",
                "success": False
            }
        
        prompt = f"""
        You are an expert HR professional specializing in fair and effective interviewing.
        
        Original question: "{question}"
        {f"Context: {context}" if context else ""}
        
        Please improve this interview question to be:
        1. More job-relevant and skill-focused
        2. Free from any potential bias (gender, age, ethnicity, etc.)
        3. Clear and easy to understand
        4. Open-ended to encourage detailed responses
        5. Legally appropriate and professional
        
        Return ONLY a JSON response with this exact structure:
        {{
            "improved_question": "the improved question here",
            "explanation": "brief explanation of improvements made"
        }}
        """
        
        response = self._call_ollama(prompt)
        
        if response:
            try:
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    result["success"] = True
                    return result
            except json.JSONDecodeError:
                logging.warning("Failed to parse JSON from Ollama response")
        
        # Fallback: simple improvement if AI fails
        improved = self._fallback_improve_question(question)
        return {
            "improved_question": improved,
            "explanation": "Enhanced for clarity and fairness (fallback)",
            "success": False
        }
    
    def analyze_answer_depth(self, answer: str, question: str, expected_skills: List[str] = None) -> Dict[str, any]:
        """
        Analyze the depth and quality of a candidate's answer
        
        Args:
            answer: Candidate's answer text
            question: The question that was asked
            expected_skills: List of skills expected in the answer
            
        Returns:
            Dictionary with analysis results
        """
        if not self.available:
            return self._fallback_analyze_answer(answer, expected_skills)
        
        skills_context = f"Expected skills: {', '.join(expected_skills)}" if expected_skills else "No specific skills expected"
        
        prompt = f"""
        You are analyzing a candidate's interview answer for depth and quality.
        
        Question: "{question}"
        Candidate's Answer: "{answer}"
        {skills_context}
        
        Analyze this answer and provide:
        1. Overall quality score (1-10)
        2. Key strengths demonstrated
        3. Areas for improvement
        4. Relevance to the question
        5. Evidence of specific skills mentioned
        
        Return ONLY a JSON response with this exact structure:
        {{
            "quality_score": 7,
            "strengths": ["list", "of", "strengths"],
            "improvements": ["suggestions", "for", "improvement"],
            "relevance_score": 8,
            "skills_demonstrated": ["list", "of", "skills", "shown"],
            "analysis_summary": "brief overall assessment"
        }}
        """
        
        response = self._call_ollama(prompt)
        
        if response:
            try:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    result["success"] = True
                    return result
            except json.JSONDecodeError:
                logging.warning("Failed to parse JSON from answer analysis")
        
        return self._fallback_analyze_answer(answer, expected_skills)
    
    def generate_follow_up_question(self, answer: str, original_question: str, skill_focus: str = None) -> Dict[str, str]:
        """
        Generate a smart follow-up question based on the candidate's answer
        
        Args:
            answer: Candidate's previous answer
            original_question: The original question asked
            skill_focus: Specific skill to focus on
            
        Returns:
            Dictionary with follow-up question and reasoning
        """
        if not self.available:
            return {
                "follow_up_question": f"Can you tell me more about your experience with {skill_focus}?" if skill_focus else "Can you elaborate on that?",
                "reasoning": "Basic follow-up question",
                "success": False
            }
        
        skill_context = f"Focus on skill: {skill_focus}" if skill_focus else ""
        
        prompt = f"""
        Based on a candidate's answer, generate a meaningful follow-up question.
        
        Original Question: "{original_question}"
        Candidate's Answer: "{answer}"
        {skill_context}
        
        Create a follow-up question that:
        1. Probes deeper into the candidate's experience
        2. Explores specific aspects they mentioned
        3. Tests critical thinking or problem-solving
        4. Remains fair and job-relevant
        5. Encourages detailed response
        
        Return ONLY a JSON response with this exact structure:
        {{
            "follow_up_question": "the follow-up question here",
            "reasoning": "why this follow-up is relevant"
        }}
        """
        
        response = self._call_ollama(prompt)
        
        if response:
            try:
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    result["success"] = True
                    return result
            except json.JSONDecodeError:
                logging.warning("Failed to parse JSON from follow-up generation")
        
        return {
            "follow_up_question": f"Could you provide a specific example related to {skill_focus}?" if skill_focus else "What was the outcome of that situation?",
            "reasoning": "Standard follow-up to get more details",
            "success": False
        }
    
    def _fallback_improve_question(self, question: str) -> str:
        """Fallback method for question improvement without AI"""
        # Simple rule-based improvements
        improvements = {
            "he": "they",
            "she": "they",
            "his": "their",
            "her": "their",
            "man": "person",
            "woman": "person"
        }
        
        improved = question
        for old, new in improvements.items():
            improved = improved.replace(old, new)
        
        # Ensure question is open-ended
        if improved.lower().startswith(('did you', 'have you', 'are you', 'do you')):
            improved = "Tell me about " + improved.lower()
        
        return improved
    
    def _fallback_analyze_answer(self, answer: str, expected_skills: List[str] = None) -> Dict[str, any]:
        """Fallback method for answer analysis without AI"""
        word_count = len(answer.split())
        sentence_count = len([s for s in answer.split('.') if s.strip()])
        
        # Simple scoring based on length and structure
        if word_count > 50 and sentence_count > 2:
            quality_score = 8
            strengths = ["Detailed response", "Good structure"]
        elif word_count > 25:
            quality_score = 6
            strengths = ["Adequate response"]
        else:
            quality_score = 4
            strengths = ["Brief response"]
        
        # Check for skill mentions
        skills_demonstrated = []
        if expected_skills:
            skills_demonstrated = [skill for skill in expected_skills if skill.lower() in answer.lower()]
        
        return {
            "quality_score": quality_score,
            "strengths": strengths,
            "improvements": ["Provide more specific examples", "Include measurable results"] if word_count < 40 else [],
            "relevance_score": 7,
            "skills_demonstrated": skills_demonstrated,
            "analysis_summary": f"Answer analyzed: {word_count} words, {len(skills_demonstrated)} skills demonstrated",
            "success": False
        }