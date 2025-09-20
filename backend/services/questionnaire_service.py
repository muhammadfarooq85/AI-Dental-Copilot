from typing import List, Dict, Any, Optional
from .llm_service import LLMService
from .oral_health_agent import OralHealthAgent
import os
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


class QuestionnaireService:
    """Service for handling questionnaire analysis and risk assessment using LangChain and AI/ML API"""
    
    def __init__(self, use_agent: bool = True):
        """Initialize the questionnaire service with LangChain integration"""
        self.use_agent = use_agent
        
        if use_agent:
            # Use LangChain agent for comprehensive analysis
            self.agent = OralHealthAgent()
        else:
            # Use direct LLM service for simpler analysis
            self.llm_service = LLMService()
    
    def analyze_questionnaire(self, answers: List[Dict], patient_info: Dict = {}) -> Dict[str, Any]:
        """Analyze questionnaire responses using LangChain and AI/ML API"""
        try:
            logger.info(f"Starting questionnaire analysis with {len(answers)} answers")
            logger.info(f"Patient info: {patient_info}")
            logger.info(f"Use agent: {self.use_agent}")
            
            # Validate answers before processing
            for i, answer in enumerate(answers):
                logger.debug(f"Validating answer {i}: {answer}")
                if not isinstance(answer, dict):
                    logger.error(f"Answer {i} is not a dict: {type(answer)}")
                    raise ValueError(f"Answer {i} is not a dict")
                if 'question_id' not in answer:
                    logger.error(f"Answer {i} missing question_id: {answer}")
                    raise ValueError(f"Answer {i} missing question_id")
                if 'answer' not in answer:
                    logger.error(f"Answer {i} missing answer field: {answer}")
                    raise ValueError(f"Answer {i} missing answer field")
                
                # Log answer content for debugging
                answer_content = answer.get('answer', '')
                logger.debug(f"Answer {i} content: '{answer_content}' (type: {type(answer_content)})")
            
            # Prepare questionnaire data for analysis
            questionnaire_data = {
                "answers": answers,
                "patient_info": patient_info,
                "questionnaire_id": f"q_{hash(str(answers))}"  # Generate unique ID
            }
            
            logger.info(f"Prepared questionnaire data with ID: {questionnaire_data['questionnaire_id']}")
            logger.debug(f"Questionnaire data structure: {json.dumps(questionnaire_data, indent=2)}")
            
            if self.use_agent:
                # Use LangChain agent for comprehensive analysis
                logger.info("Using LangChain agent for analysis")
                try:
                    result = self.agent.analyze_questionnaire(questionnaire_data)
                    logger.info("Agent analysis completed successfully")
                    logger.debug(f"Agent result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
                    
                    # Convert agent result to expected format
                    logger.info("Formatting agent response")
                    formatted_result = self._format_agent_response(result)
                    logger.info("Agent response formatting completed")
                    return formatted_result
                except Exception as agent_error:
                    logger.error(f"Agent analysis failed: {str(agent_error)}", exc_info=True)
                    logger.info("Falling back to LLM service")
                    # Fallback to LLM service
                    result = self.llm_service.analyze_questionnaire_with_llm(questionnaire_data)
                    logger.info("LLM analysis completed")
                    return self._format_llm_response(result)
            else:
                # Use direct LLM service
                logger.info("Using direct LLM service for analysis")
                result = self.llm_service.analyze_questionnaire_with_llm(questionnaire_data)
                logger.info("LLM analysis completed")
                logger.info("Formatting LLM response")
                return self._format_llm_response(result)
                
        except Exception as e:
            logger.error(f"Error in analyze_questionnaire: {str(e)}", exc_info=True)
            # Fallback to basic analysis if LangChain fails
            logger.info("Using fallback analysis due to error")
            return self._fallback_analysis(answers, patient_info, str(e))
    
    def _format_agent_response(self, agent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Format agent response to match expected API format"""
        try:
            risk_assessment = agent_result.get("risk_assessment", {})
            symptoms_analysis = agent_result.get("symptoms_analysis", {})
            recommendations = agent_result.get("recommendations", {})
            
            return {
                "analysis": agent_result.get("analysis_summary", "Analysis completed"),
                "summary_paragraph": agent_result.get("summary_paragraph", "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status."),
                "risk_assessment": f"Your risk level is {risk_assessment.get('level', 'Unknown')}",
                "recommendations": recommendations.get("immediate_actions", []) + 
                                 recommendations.get("lifestyle_changes", []),
                "next_steps": agent_result.get("next_steps", []),
                "confidence_score": risk_assessment.get("confidence", 0.8),
                "detailed_insights": {
                    "risk_factors": risk_assessment.get("key_factors", []),
                    "symptoms": symptoms_analysis.get("primary_symptoms", []),
                    "total_questions_answered": len(agent_result.get("answers", [])),
                    "ai_analysis": True,
                    "agent_used": True
                },
                "patient_education": agent_result.get("patient_education", ""),
                "follow_up_questions": agent_result.get("follow_up_questions", []),
                "metadata": agent_result.get("metadata", {})
            }
        except Exception as e:
            return self._create_error_response(f"Error formatting agent response: {str(e)}")
    
    def _format_llm_response(self, llm_result: Dict[str, Any]) -> Dict[str, Any]:
        """Format LLM response to match expected API format"""
        try:
            risk_assessment = llm_result.get("risk_assessment", {})
            symptoms_analysis = llm_result.get("symptoms_analysis", {})
            recommendations = llm_result.get("recommendations", {})
            
            return {
                "analysis": llm_result.get("analysis_summary", "Analysis completed"),
                "summary_paragraph": llm_result.get("summary_paragraph", "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status."),
                "risk_assessment": f"Your risk level is {risk_assessment.get('level', 'Unknown')}",
                "recommendations": recommendations.get("immediate_actions", []) + 
                                 recommendations.get("lifestyle_changes", []),
                "next_steps": llm_result.get("next_steps", []),
                "confidence_score": risk_assessment.get("confidence", 0.8),
                "detailed_insights": {
                    "risk_factors": risk_assessment.get("key_factors", []),
                    "symptoms": symptoms_analysis.get("primary_symptoms", []),
                    "total_questions_answered": len(llm_result.get("answers", [])),
                    "ai_analysis": True,
                    "llm_used": True
                },
                "patient_education": llm_result.get("patient_education", ""),
                "follow_up_questions": llm_result.get("follow_up_questions", []),
                "metadata": llm_result.get("metadata", {})
            }
        except Exception as e:
            return self._create_error_response(f"Error formatting LLM response: {str(e)}")
    
    def _fallback_analysis(self, answers: List[Dict], patient_info: Dict, error_msg: str) -> Dict[str, Any]:
        """Fallback analysis when LangChain/AI services fail"""
        risk_factors = []
        symptoms = []
        
        for answer in answers:
            if answer.get('question_id') == 'q4' and answer.get('answer', '').lower() in ['yes', 'true']:
                risk_factors.append("Tobacco use")
            elif answer.get('question_id') == 'q5' and answer.get('answer', '').lower() in ['daily', 'multiple times daily']:
                risk_factors.append("Heavy alcohol consumption")
            elif answer.get('question_id') == 'q6' and answer.get('answer', '').lower() in ['yes', 'true']:
                risk_factors.append("Family history of oral cancer")
            elif answer.get('question_id') == 'q2':
                symptoms.append(answer.get('answer', ''))
        
        risk_level = "High" if len(risk_factors) >= 3 else "Medium" if len(risk_factors) >= 1 else "Low"
        
        # Generate comprehensive patient education for fallback
        patient_education = self._generate_fallback_patient_education(risk_level, risk_factors, symptoms)
        
        # Generate summary paragraph for fallback
        summary_parts = []
        summary_parts.append(f"Based on your questionnaire responses, your oral health risk level is {risk_level.lower()}.")
        
        if risk_factors:
            summary_parts.append(f"Key risk factors identified include: {', '.join(risk_factors)}.")
        
        if symptoms:
            summary_parts.append(f"You reported symptoms such as: {', '.join(symptoms)}.")
        
        summary_parts.append("Maintaining good oral hygiene, regular dental check-ups, and addressing any risk factors are essential for optimal oral health.")
        summary_paragraph = " ".join(summary_parts)
        
        return {
            "analysis": f"Based on your responses, we've identified {len(risk_factors)} risk factors and {len(symptoms)} symptoms. (Note: AI analysis temporarily unavailable)",
            "summary_paragraph": summary_paragraph,
            "risk_assessment": f"Your risk level is {risk_level}",
            "recommendations": [
                "Consult with a healthcare professional",
                "Maintain good oral hygiene",
                "Avoid tobacco and excessive alcohol",
                "Schedule regular dental check-ups"
            ],
            "next_steps": [
                "Schedule an appointment with your dentist",
                "Consider consulting an oral medicine specialist",
                "Monitor symptoms and report any changes"
            ],
            "confidence_score": 0.6,  # Lower confidence due to fallback
            "detailed_insights": {
                "risk_factors": risk_factors,
                "symptoms": symptoms,
                "total_questions_answered": len(answers),
                "ai_analysis": False,
                "fallback_used": True,
                "error_message": error_msg
            },
            "patient_education": patient_education
        }
    
    def _generate_fallback_patient_education(self, risk_level: str, risk_factors: List[str], symptoms: List[str]) -> str:
        """Generate comprehensive patient education for fallback analysis"""
        
        education_parts = []
        
        # Introduction about oral health importance
        education_parts.append("Your oral health is a crucial component of your overall well-being and quality of life. The mouth serves as the gateway to your body, and maintaining good oral hygiene can significantly impact your general health, preventing various systemic conditions and improving your daily comfort and confidence.")
        
        # Risk level specific education
        if risk_level.lower() == "high":
            education_parts.append("Based on your responses, we've identified several risk factors that require immediate attention. High-risk individuals should prioritize regular dental check-ups every 3-6 months and maintain excellent oral hygiene practices. Early intervention and consistent monitoring are crucial for managing these risk factors effectively and preventing potential complications.")
        elif risk_level.lower() == "medium":
            education_parts.append("Your responses indicate some risk factors that warrant attention and proactive care. Medium-risk individuals should maintain regular dental visits every 6 months and be vigilant about oral hygiene practices. Proactive care and early intervention can help prevent the progression of potential issues and maintain optimal oral health.")
        else:
            education_parts.append("Your responses suggest a generally low-risk profile, which is excellent for your oral health. However, maintaining preventive care through regular dental visits and consistent good oral hygiene practices remains important for long-term oral health and early detection of any potential issues.")
        
        # Risk factors specific education
        if risk_factors:
            risk_text = ", ".join(risk_factors)
            education_parts.append(f"Regarding your identified risk factors ({risk_text}), it's important to understand how these factors can impact your oral health. Each risk factor can contribute to various oral health conditions, and addressing them through lifestyle changes and professional care can significantly improve your oral health outcomes.")
        
        # Symptoms specific education
        if symptoms:
            symptom_text = ", ".join(symptoms)
            education_parts.append(f"Concerning your reported symptoms ({symptom_text}), it's important to understand that these could indicate various conditions ranging from minor irritations to more serious concerns. Professional evaluation is essential for accurate diagnosis and appropriate treatment. Early detection and proper management of symptoms can prevent complications and improve treatment outcomes.")
        
        # General oral health education
        education_parts.append("General oral health maintenance includes brushing your teeth twice daily with fluoride toothpaste, flossing daily to remove plaque between teeth, using mouthwash as recommended by your dentist, and avoiding tobacco products and excessive alcohol consumption. A balanced diet rich in fruits and vegetables while limiting sugary foods and drinks also supports oral health and provides essential nutrients for healthy teeth and gums.")
        
        # Prevention and early detection
        education_parts.append("Prevention is always better than treatment when it comes to oral health. Regular self-examinations of your mouth, being aware of any changes in appearance or sensation, and seeking prompt professional care when concerns arise are key to maintaining optimal oral health. Early detection of oral health issues significantly improves treatment outcomes, reduces the complexity of care needed, and often results in less invasive and more cost-effective treatments.")
        
        # Professional care importance
        education_parts.append("While self-care is important, professional dental care provides specialized expertise in detecting issues that may not be visible or noticeable to you. Your dentist can identify early signs of problems, provide professional cleanings that remove plaque and tartar buildup that regular brushing cannot, and offer personalized advice based on your specific oral health needs, risk factors, and lifestyle. Regular professional care is an investment in your long-term oral and overall health.")
        
        return " ".join(education_parts)
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response when analysis fails"""
        return {
            "analysis": f"Analysis encountered an error: {error_message}",
            "summary_paragraph": "We apologize for the technical difficulty. Please consult with a healthcare professional for a proper oral health assessment and personalized guidance.",
            "risk_assessment": "Unable to assess risk level",
            "recommendations": [
                "Consult with a healthcare professional",
                "Try the analysis again later"
            ],
            "next_steps": [
                "Contact support for assistance",
                "Schedule a direct consultation"
            ],
            "confidence_score": 0.0,
            "detailed_insights": {
                "error": True,
                "error_message": error_message,
                "ai_analysis": False
            },
            "patient_education": "Your oral health is important for your overall well-being. Regular dental check-ups, proper oral hygiene including brushing twice daily and flossing, avoiding tobacco and excessive alcohol, and maintaining a balanced diet are key to good oral health. If you're experiencing any symptoms or concerns, please consult with a healthcare professional for proper evaluation and personalized guidance."
        }
    
    def quick_analysis(self, answers: List[Dict]) -> Dict[str, Any]:
        """Perform quick risk analysis using LangChain services"""
        try:
            # Prepare questionnaire data for quick analysis
            questionnaire_data = {
                "answers": answers,
                "questionnaire_id": f"quick_{hash(str(answers))}"
            }
            
            if self.use_agent:
                # Use agent's quick analysis
                result = self.agent.get_quick_analysis(questionnaire_data)
                return {
                    "risk_level": result.get("risk_level", "Unknown"),
                    "risk_factors_count": len(result.get("risk_factors", [])),
                    "symptoms_identified": result.get("symptoms", []),
                    "recommendation": result.get("recommendation", "Consult with a healthcare professional"),
                    "ai_analysis": True,
                    "agent_used": True
                }
            else:
                # Use LLM service quick analysis
                result = self.llm_service.get_quick_analysis(questionnaire_data)
                return {
                    "risk_level": result.get("risk_level", "Unknown"),
                    "risk_factors_count": len(result.get("risk_factors", [])),
                    "symptoms_identified": result.get("symptoms", []),
                    "recommendation": result.get("recommendation", "Consult with a healthcare professional"),
                    "ai_analysis": True,
                    "llm_used": True
                }
                
        except Exception as e:
            # Fallback to basic analysis
            return self._fallback_quick_analysis(answers, str(e))
    
    def _fallback_quick_analysis(self, answers: List[Dict], error_msg: str) -> Dict[str, Any]:
        """Fallback quick analysis when LangChain services fail"""
        risk_factors = 0
        symptoms = []
        
        for answer in answers:
            if answer.get('question_id') == "q4" and answer.get('answer', '').lower() in ["yes", "true"]:
                risk_factors += 2
            elif answer.get('question_id') == "q5" and answer.get('answer', '').lower() in ["daily", "multiple times daily"]:
                risk_factors += 1
            elif answer.get('question_id') == "q6" and answer.get('answer', '').lower() in ["yes", "true"]:
                risk_factors += 2
            elif answer.get('question_id') == "q2":
                symptoms.append(answer.get('answer', ''))
        
        # Determine risk level
        if risk_factors >= 4:
            risk_level = "High"
        elif risk_factors >= 2:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return {
            "risk_level": risk_level,
            "risk_factors_count": risk_factors,
            "symptoms_identified": symptoms,
            "recommendation": "Please consult with a healthcare professional for a thorough examination.",
            "ai_analysis": False,
            "fallback_used": True,
            "error_message": error_msg
        }
    
    