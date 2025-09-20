import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)


class LLMService:
    """Service for handling LLM interactions with AI/ML API"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.aimlapi.com/v1"):
        self.api_key = api_key or os.getenv("AIMLAPI_KEY")
        self.base_url = base_url
        
        if not self.api_key:
            raise ValueError("AIMLAPI_KEY environment variable is required")
        
        # Initialize OpenAI client for direct API calls
        self.openai_client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
        
        # Initialize LangChain ChatOpenAI
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            base_url=base_url,
            model="gpt-4o",
            temperature=0.7,
            max_tokens=1000
        )
    
    def analyze_questionnaire_with_llm(self, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze questionnaire using LLM with structured prompts"""
        
        # Create system prompt for oral health analysis
        system_prompt = """You are an expert oral health specialist and medical AI assistant. 
        Your role is to analyze questionnaire responses and provide comprehensive, patient-friendly 
        oral health assessments and recommendations.

        Key responsibilities:
        1. Analyze questionnaire responses for oral health risk factors
        2. Identify symptoms and their potential significance
        3. Assess overall risk level (Low, Medium, High)
        4. Provide clear, actionable recommendations
        5. Generate patient-friendly explanations
        6. Suggest appropriate next steps
        7. Create comprehensive patient education content

        For patient education, provide detailed explanations about:
        - The importance of oral health for overall well-being
        - How oral health affects general health and quality of life
        - Risk factors specific to the patient's responses
        - General preventive care practices
        - The importance of regular professional dental care
        - Early detection and its benefits
        - Self-care practices and their significance

        Always maintain a professional, empathetic tone and provide evidence-based insights.
        Use simple language that patients can easily understand."""

        # Format questionnaire data for analysis
        questionnaire_text = self._format_questionnaire_for_analysis(questionnaire_data)
        
        user_prompt = f"""
        Please analyze the following oral health questionnaire responses and provide a comprehensive assessment:

        {questionnaire_text}

        Please provide your analysis in the following JSON format:
        {{
            "analysis_summary": "Brief summary of the analysis in simple terms",
            "risk_assessment": {{
                "level": "Low/Medium/High",
                "confidence": 0.0-1.0,
                "key_factors": ["list of main risk factors identified"]
            }},
            "symptoms_analysis": {{
                "primary_symptoms": ["list of main symptoms"],
                "symptom_severity": "Mild/Moderate/Severe",
                "concerning_patterns": ["any concerning symptom patterns"]
            }},
            "recommendations": {{
                "immediate_actions": ["urgent recommendations"],
                "lifestyle_changes": ["lifestyle recommendations"],
                "medical_follow_up": ["medical recommendations"]
            }},
            "next_steps": [
                "specific actionable next steps for the patient"
            ],
            "patient_education": "Comprehensive educational paragraph explaining oral health importance, risk factors, preventive care, and general health education tailored to their specific responses",
            "follow_up_questions": ["questions to ask in follow-up"]
        }}
        """

        try:
            # Validate prompts before creating messages
            if not system_prompt or not isinstance(system_prompt, str):
                logger.error(f"Invalid system prompt: {type(system_prompt)}")
                raise ValueError("System prompt is empty or not a string")
            
            if not user_prompt or not isinstance(user_prompt, str):
                logger.error(f"Invalid user prompt: {type(user_prompt)}")
                raise ValueError("User prompt is empty or not a string")
            
            # Use LangChain for structured analysis
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Log message details before sending
            logger.info(f"System message content length: {len(system_prompt)}")
            logger.info(f"User message content length: {len(user_prompt)}")
            logger.info(f"Number of messages: {len(messages)}")
            
            # Validate messages before sending
            for i, msg in enumerate(messages):
                if hasattr(msg, 'content'):
                    if msg.content is None:
                        logger.error(f"Message {i} has null content: {msg}")
                        raise ValueError(f"Message {i} has null content")
                    elif not isinstance(msg.content, str):
                        logger.error(f"Message {i} content is not a string: {type(msg.content)}")
                        raise ValueError(f"Message {i} content is not a string")
                    elif len(msg.content.strip()) == 0:
                        logger.warning(f"Message {i} has empty content after stripping")
                else:
                    logger.error(f"Message {i} has no content attribute: {msg}")
                    raise ValueError(f"Message {i} has no content attribute")
            
            logger.info("Invoking LLM with validated messages")
            response = self.llm.invoke(messages)
            
            logger.info(f"LLM response type: {type(response)}")
            logger.info(f"LLM response content length: {len(response.content) if hasattr(response, 'content') else 'No content attribute'}")
            
            # Parse JSON response
            analysis_result = json.loads(response.content)
            
            # Add metadata
            analysis_result["metadata"] = {
                "model_used": "gpt-4o-mini",
                "analysis_timestamp": self._get_current_timestamp(),
                "questionnaire_id": questionnaire_data.get("questionnaire_id", "unknown")
            }
            
            logger.info("Successfully parsed LLM response")
            return analysis_result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            # Fallback if JSON parsing fails
            return self._create_fallback_response(response.content, questionnaire_data)
        except Exception as e:
            logger.error(f"Error in LLM analysis: {str(e)}", exc_info=True)
            raise Exception(f"Error in LLM analysis: {str(e)}")
    
    def _format_questionnaire_for_analysis(self, questionnaire_data: Dict[str, Any]) -> str:
        """Format questionnaire data into readable text for LLM analysis"""
        
        formatted_text = "=== ORAL HEALTH QUESTIONNAIRE RESPONSES ===\n\n"
        
        # Add patient info if available
        if questionnaire_data.get("patient_info"):
            patient_info = questionnaire_data["patient_info"]
            formatted_text += f"Patient Information:\n"
            for key, value in patient_info.items():
                formatted_text += f"- {key.replace('_', ' ').title()}: {value}\n"
            formatted_text += "\n"
        
        # Add questionnaire answers
        answers = questionnaire_data.get("answers", [])
        formatted_text += "Questionnaire Responses:\n"
        
        for i, answer in enumerate(answers, 1):
            question_text = answer.get("question_text", f"Question {answer.get('question_id', i)}")
            answer_text = answer.get("answer", "No answer provided")
            formatted_text += f"{i}. {question_text}\n   Answer: {answer_text}\n\n"
        
        # Add additional context if available
        if questionnaire_data.get("additional_context"):
            formatted_text += f"Additional Context:\n{questionnaire_data['additional_context']}\n\n"
        
        return formatted_text
    
    def _create_fallback_response(self, llm_response: str, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured response when JSON parsing fails"""
        
        return {
            "analysis_summary": llm_response[:200] + "..." if len(llm_response) > 200 else llm_response,
            "risk_assessment": {
                "level": "Medium",
                "confidence": 0.6,
                "key_factors": ["Unable to parse detailed analysis"]
            },
            "symptoms_analysis": {
                "primary_symptoms": ["Analysis in progress"],
                "symptom_severity": "Unknown",
                "concerning_patterns": ["Requires manual review"]
            },
            "recommendations": {
                "immediate_actions": ["Consult with a healthcare professional"],
                "lifestyle_changes": ["Maintain good oral hygiene"],
                "medical_follow_up": ["Schedule dental appointment"]
            },
            "next_steps": [
                "Review the analysis with a healthcare provider",
                "Schedule a dental consultation"
            ],
            "patient_education": "Please consult with a healthcare professional for a detailed assessment.",
            "follow_up_questions": [
                "Would you like to schedule a follow-up consultation?",
                "Do you have any specific concerns about your oral health?"
            ],
            "metadata": {
                "model_used": "gpt-4o",
                "analysis_timestamp": self._get_current_timestamp(),
                "parsing_error": True,
                "raw_response": llm_response
            }
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_quick_analysis(self, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get a quick analysis without full processing"""
        
        # Simplified prompt for quick analysis
        quick_prompt = f"""
        Provide a quick oral health risk assessment based on these responses:
        {self._format_questionnaire_for_analysis(questionnaire_data)}
        
        Return only: {{"risk_level": "Low/Medium/High", "main_concern": "brief concern", "recommendation": "brief recommendation"}}
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=quick_prompt)])
            return json.loads(response.content)
        except:
            return {
                "risk_level": "Medium",
                "main_concern": "Requires professional assessment",
                "recommendation": "Consult with a healthcare professional"
            }
