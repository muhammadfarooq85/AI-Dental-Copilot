from typing import Dict, Any, List, Optional
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskAssessmentTool(BaseTool):
    """Tool for assessing oral health risk factors based on patient's history questionnaire"""

    name: str = "risk_assessment"
    description: str = "Assess oral health risk factors based on patient's history questionnaire responses"

    def _run(self, questionnaire_data: str) -> str:
        """
        Calculate risk assessment based on the following 5 questions:
        1. Do you have any sores or ulcers in your mouth? (q1)
        2. Is there any swelling or redness in your mouth? (q2)
        3. Are you experiencing any unusual pain in your mouth? (q3)
        4. Have you noticed any changes in the inner lining of your mouth recently? (q4)
        5. Have you noticed any lumps or thickened areas in your mouth or neck? (q5)
        If 3 or more answers are 'yes', risk is higher.
        """
        try:
            data = json.loads(questionnaire_data)
            answers = data.get("answers", [])

            # Map question IDs to their meaning for clarity
            question_map = {
                "q1": "Sores or ulcers in mouth",
                "q2": "Swelling or redness in mouth",
                "q3": "Unusual pain in mouth",
                "q4": "Changes in inner lining of mouth",
                "q5": "Lumps or thickened areas in mouth or neck"
            }

            yes_count = 0
            risk_factors = []

            for answer in answers:
                question_id = answer.get("question_id", "")
                answer_text = answer.get("answer", "").strip().lower()
                if question_id in question_map:
                    if answer_text in ["yes", "true"]:
                        yes_count += 1
                        risk_factors.append(question_map[question_id])

            # Determine risk level
            if yes_count >= 3:
                risk_level = "High"
            elif yes_count == 2:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            return json.dumps({
                "risk_level": risk_level,
                "yes_count": yes_count,
                "risk_factors": risk_factors,
                "total_questions": 5
            })

        except Exception as e:
            return json.dumps({
                "error": f"Error in risk assessment: {str(e)}",
                "risk_level": "Unknown"
            })


class SymptomAnalysisTool(BaseTool):
    """Tool for analyzing symptoms from questionnaire responses"""
    
    name: str = "symptom_analysis"
    description: str = "Analyze symptoms and their patterns from questionnaire responses"
    
    def _run(self, questionnaire_data: str) -> str:
        """Analyze symptoms from questionnaire data"""
        try:
            data = json.loads(questionnaire_data)
            answers = data.get("answers", [])
            
            symptoms = []
            symptom_categories = {
                "visual": ["white patches", "red patches", "lumps", "swelling"],
                "pain": ["pain", "discomfort", "burning sensation"],
                "functional": ["difficulty swallowing", "speech problems", "numbness"],
                "systemic": ["weight loss", "fatigue", "fever"]
            }
            
            categorized_symptoms = {category: [] for category in symptom_categories.keys()}
            
            # Extract symptoms from answers
            for answer in answers:
                question_id = answer.get("question_id", "")
                answer_text = answer.get("answer", "").lower()
                
                if question_id == "q2":  # Symptom type question
                    symptoms.append(answer_text)
                    
                    # Categorize symptoms
                    for category, keywords in symptom_categories.items():
                        if any(keyword in answer_text for keyword in keywords):
                            categorized_symptoms[category].append(answer_text)
                
                elif question_id == "q10":  # Additional symptoms
                    if answer_text and answer_text != "none":
                        symptoms.append(answer_text)
            
            # Determine severity
            severity_indicators = ["severe", "intense", "unbearable", "constant"]
            severity = "Mild"
            if any(indicator in " ".join(symptoms).lower() for indicator in severity_indicators):
                severity = "Severe"
            elif len(symptoms) > 3:
                severity = "Moderate"
            
            return json.dumps({
                "symptoms": symptoms,
                "categorized_symptoms": categorized_symptoms,
                "severity": severity,
                "total_symptoms": len(symptoms),
                "concerning_symptoms": [s for s in symptoms if any(word in s.lower() for word in ["lump", "swelling", "bleeding", "numbness"])]
            })
            
        except Exception as e:
            return json.dumps({
                "error": f"Error in symptom analysis: {str(e)}",
                "symptoms": [],
                "severity": "Unknown"
            })


class RecommendationTool(BaseTool):
    """Tool for generating personalized recommendations"""
    
    name: str = "generate_recommendations"
    description: str = "Generate personalized recommendations based on analysis results"
    
    def _run(self, analysis_data: str) -> str:
        """Generate recommendations based on analysis"""
        try:
            data = json.loads(analysis_data)
            risk_level = data.get("risk_level", "Unknown")
            symptoms = data.get("symptoms", [])
            risk_factors = data.get("risk_factors", [])
            
            recommendations = {
                "immediate_actions": [],
                "lifestyle_changes": [],
                "medical_follow_up": [],
                "monitoring": []
            }
            
            # Immediate actions based on risk level
            if risk_level == "High":
                recommendations["immediate_actions"].extend([
                    "Schedule an urgent appointment with an oral medicine specialist",
                    "Consider consulting an oncologist for further evaluation",
                    "Document all symptoms with photos if possible"
                ])
            elif risk_level == "Medium":
                recommendations["immediate_actions"].extend([
                    "Schedule a dental appointment within 1-2 weeks",
                    "Monitor symptoms daily and note any changes"
                ])
            else:
                recommendations["immediate_actions"].extend([
                    "Schedule a routine dental check-up",
                    "Continue monitoring oral health"
                ])
            
            # Lifestyle recommendations
            if "Tobacco use" in risk_factors:
                recommendations["lifestyle_changes"].append("Quit smoking/tobacco use immediately")
            if "Heavy alcohol consumption" in risk_factors:
                recommendations["lifestyle_changes"].append("Reduce alcohol consumption")
            
            recommendations["lifestyle_changes"].extend([
                "Maintain excellent oral hygiene (brush twice daily, floss daily)",
                "Use alcohol-free mouthwash",
                "Eat a balanced diet rich in fruits and vegetables",
                "Avoid excessive sun exposure to lips"
            ])
            
            # Medical follow-up
            if any("lump" in s.lower() or "swelling" in s.lower() for s in symptoms):
                recommendations["medical_follow_up"].append("Consider biopsy for any lumps or swellings")
            
            if "difficulty swallowing" in symptoms:
                recommendations["medical_follow_up"].append("Consult with an ENT specialist")
            
            recommendations["medical_follow_up"].extend([
                "Regular dental cleanings every 6 months",
                "Annual oral cancer screening",
                "Follow up on any concerning symptoms"
            ])
            
            # Monitoring recommendations
            recommendations["monitoring"] = [
                "Check mouth weekly for any changes",
                "Note any new symptoms or changes in existing ones",
                "Keep a symptom diary",
                "Take photos of any visible changes"
            ]
            
            return json.dumps(recommendations)
            
        except Exception as e:
            return json.dumps({
                "error": f"Error generating recommendations: {str(e)}",
                "immediate_actions": ["Consult with a healthcare professional"],
                "lifestyle_changes": ["Maintain good oral hygiene"],
                "medical_follow_up": ["Schedule dental appointment"]
            })


class PatientEducationTool(BaseTool):
    """Tool for generating comprehensive patient education content"""
    
    name: str = "patient_education"
    description: str = "Generate detailed educational content for patients about oral health based on their specific responses"
    
    def _run(self, analysis_data: str) -> str:
        """Generate comprehensive patient education content based on analysis"""
        try:
            data = json.loads(analysis_data)
            answers = data.get("answers", [])
            risk_level = data.get("risk_assessment", {}).get("level", "Unknown")
            symptoms = data.get("symptoms_analysis", {}).get("primary_symptoms", [])
            
            # Extract risk factors from answers if not provided directly
            risk_factors = []
            if answers:
                # Map question IDs to their meaning for risk factors
                question_map = {
                    "q1": "Sores or ulcers in mouth",
                    "q2": "Swelling or redness in mouth", 
                    "q3": "Unusual pain in mouth",
                    "q4": "Changes in inner lining of mouth",
                    "q5": "Lumps or thickened areas in mouth or neck"
                }
                
                for answer in answers:
                    question_id = answer.get("question_id", "")
                    answer_text = answer.get("answer", "").strip().lower()
                    if question_id in question_map and answer_text in ["yes", "true"]:
                        risk_factors.append(question_map[question_id])
            
            # Generate personalized education based on responses
            education_parts = []
            
            # Introduction about oral health importance
            education_parts.append("Your oral health is a vital component of your overall well-being. The mouth serves as the gateway to your body, and maintaining good oral hygiene can significantly impact your general health, preventing various systemic conditions and improving your quality of life.")
            
            # Risk level specific education
            if risk_level.lower() == "high":
                education_parts.append("Based on your responses, we've identified several risk factors that require attention. High-risk individuals should prioritize regular dental check-ups every 3-6 months and maintain excellent oral hygiene practices. Early intervention and consistent monitoring are crucial for managing these risk factors effectively.")
            elif risk_level.lower() == "medium":
                education_parts.append("Your responses indicate some risk factors that warrant attention. Medium-risk individuals should maintain regular dental visits every 6 months and be vigilant about oral hygiene. Proactive care can help prevent the progression of potential issues.")
            else:
                education_parts.append("Your responses suggest a generally low-risk profile, which is excellent. However, maintaining preventive care through regular dental visits and good oral hygiene practices remains important for long-term oral health.")
            
            # Risk factors specific education
            if risk_factors:
                risk_text = ", ".join(risk_factors)
                education_parts.append(f"Regarding your identified risk factors ({risk_text}), it's important to understand how these factors can impact your oral health. Each risk factor can contribute to various oral health conditions, and addressing them through lifestyle changes and professional care can significantly improve your oral health outcomes.")
            
            # Symptom-specific education
            if symptoms and any(s != "yes" for s in symptoms):
                symptom_text = ", ".join([s for s in symptoms if s != "yes"])
                education_parts.append(f"Concerning your reported symptoms ({symptom_text}), it's important to understand that these could indicate various conditions ranging from minor irritations to more serious concerns. Professional evaluation is essential for accurate diagnosis and appropriate treatment.")
            elif symptoms:
                education_parts.append("Regarding your reported symptoms, it's important to understand that these could indicate various conditions ranging from minor irritations to more serious concerns. Professional evaluation is essential for accurate diagnosis and appropriate treatment.")
            
            # General oral health education
            education_parts.append("General oral health maintenance includes brushing your teeth twice daily with fluoride toothpaste, flossing daily, using mouthwash as recommended, and avoiding tobacco products and excessive alcohol consumption. A balanced diet rich in fruits and vegetables while limiting sugary foods and drinks also supports oral health.")
            
            # Prevention and early detection
            education_parts.append("Prevention is always better than treatment. Regular self-examinations of your mouth, being aware of any changes in appearance or sensation, and seeking prompt professional care when concerns arise are key to maintaining optimal oral health. Early detection of oral health issues significantly improves treatment outcomes and reduces the complexity of care needed.")
            
            # Professional care importance
            education_parts.append("While self-care is important, professional dental care provides specialized expertise in detecting issues that may not be visible or noticeable to you. Your dentist can identify early signs of problems, provide professional cleanings that remove plaque and tartar buildup, and offer personalized advice based on your specific oral health needs and risk factors.")
            
            education_content = " ".join(education_parts)
            
            # Create a concise summary paragraph
            summary_parts = []
            summary_parts.append(f"Based on your questionnaire responses, your oral health risk level is {risk_level.lower()}.")
            
            if risk_factors:
                summary_parts.append(f"Key risk factors identified include: {', '.join(risk_factors)}.")
            
            if symptoms and any(s != "yes" for s in symptoms):
                symptom_text = ", ".join([s for s in symptoms if s != "yes"])
                summary_parts.append(f"You reported symptoms such as: {symptom_text}.")
            elif symptoms:
                summary_parts.append("You reported experiencing symptoms that warrant attention.")
            
            summary_parts.append("Maintaining good oral hygiene, regular dental check-ups, and addressing any risk factors are essential for optimal oral health.")
            
            summary_paragraph = " ".join(summary_parts)
            
            return json.dumps({
                "summary_paragraph": summary_paragraph,
                "education_content": education_content,
                "key_points": [
                    "Oral health impacts overall well-being",
                    "Risk level: " + risk_level,
                    "Regular professional care is essential",
                    "Early detection improves outcomes",
                    "Prevention through good hygiene practices",
                    "Professional evaluation for symptoms"
                ],
                "personalized": True,
                "risk_level": risk_level,
                "symptoms_addressed": len(symptoms) > 0
            })
            
        except Exception as e:
            return json.dumps({
                "error": f"Error generating patient education: {str(e)}",
                "education_content": "Your oral health is important for your overall well-being. Regular dental check-ups, proper oral hygiene including brushing twice daily and flossing, avoiding tobacco and excessive alcohol, and maintaining a balanced diet are key to good oral health. If you're experiencing any symptoms or concerns, please consult with a healthcare professional for proper evaluation and personalized guidance.",
                "key_points": [
                    "Oral health affects overall health",
                    "Regular dental care is important",
                    "Good oral hygiene is essential",
                    "Professional consultation for concerns"
                ],
                "personalized": False
            })


class OralHealthAgent:
    """LangChain agent for comprehensive oral health analysis"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.aimlapi.com/v1"):
        self.api_key = api_key or os.getenv("AIMLAPI_KEY")
        self.base_url = base_url

                # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        if not self.api_key:
            raise ValueError("AIMLAPI_KEY environment variable is required")
        
        # Initialize LLM with error handling
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            base_url=base_url,
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1500
        )
        
        # Create a wrapper for the LLM to handle null content issues
        self.llm = self._create_safe_llm_wrapper()
        
        # Initialize tools
        self.tools = [
            RiskAssessmentTool(),
            SymptomAnalysisTool(),
            RecommendationTool(),
            PatientEducationTool()
        ]
        
        # Create agent
        self.agent = self._create_agent()
        

    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent with tools"""
        
        # System prompt for the agent
        system_prompt = """You are an expert oral health AI assistant specializing in questionnaire analysis and risk assessment.

        Your role is to:
        1. Analyze questionnaire responses using specialized tools
        2. Assess oral health risk factors and symptoms
        3. Generate comprehensive, patient-friendly reports
        4. Provide actionable recommendations
        5. Create detailed patient education content

        Available tools:
        - risk_assessment: Calculate risk factors and overall risk level
        - symptom_analysis: Analyze symptoms and their patterns
        - generate_recommendations: Create personalized recommendations
        - patient_education: Generate comprehensive educational content about oral health

        Always use these tools to provide accurate, evidence-based analysis.
        Present information in clear, simple language that patients can understand.
        Be empathetic and supportive in your responses.
        Include detailed patient education that explains oral health importance, risk factors, and general preventive care."""

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create agent
        agent = create_openai_tools_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create agent executor with error handling
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            return_intermediate_steps=True,
            early_stopping_method="generate"
        )
        
        return agent_executor
    
    def analyze_questionnaire(self, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze questionnaire using the LangChain agent"""
        
        try:
            logger.info(f"Starting questionnaire analysis for data: {json.dumps(questionnaire_data, indent=2)}")
            
            # Format input for the agent
            input_text = f"""
            Please analyze this oral health questionnaire and provide a comprehensive assessment:
            
            Questionnaire Data: {json.dumps(questionnaire_data, indent=2)}
            
            Use the available tools to:
            1. Assess risk factors and determine risk level
            2. Analyze symptoms and their patterns
            3. Generate personalized recommendations
            
            Provide a detailed report in simple, patient-friendly language.
            """
            
            logger.info(f"Formatted input text length: {len(input_text)}")
            
            # Validate input text
            if not input_text or not isinstance(input_text, str):
                raise ValueError("Input text is empty or not a string")
            
            # Run the agent with proper error handling
            logger.info("Invoking agent with input and empty chat history")
            
            # Use a simpler approach to avoid message validation issues
            try:
                result = self.agent.invoke({
                    "input": input_text,
                    "chat_history": []
                })
            except Exception as agent_error:
                logger.error(f"Agent invocation failed: {str(agent_error)}")
                # Fallback to direct LLM call
                logger.info("Falling back to direct LLM analysis")
                return self._fallback_to_llm_analysis(questionnaire_data)
            
            logger.info(f"Agent result type: {type(result)}")
            logger.info(f"Agent result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
            
            # Parse and structure the response
            response = self._parse_agent_response(result)
            
            logger.info("Successfully parsed agent response")
            return response
            
        except Exception as e:
            logger.error(f"Error in analyze_questionnaire: {str(e)}", exc_info=True)
            return self._create_error_response(str(e))
    
    def _parse_agent_response(self, agent_result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the agent's response"""
        
        try:
            # Extract the main response
            output = agent_result.get("output", "")
            
            # Extract data from intermediate steps (tool calls)
            risk_level = "Medium"
            risk_factors = []
            symptoms = []
            recommendations = {}
            
            # Parse intermediate steps to extract tool results
            intermediate_steps = agent_result.get("intermediate_steps", [])
            for step in intermediate_steps:
                if isinstance(step, list) and len(step) >= 2:
                    action, observation = step[0], step[1]
                    if hasattr(action, 'tool') and hasattr(action, 'tool_input'):
                        tool_name = action.tool
                        tool_input = action.tool_input
                        
                        if tool_name == "risk_assessment":
                            try:
                                risk_data = json.loads(observation)
                                risk_level = risk_data.get("risk_level", "Medium")
                                risk_factors = risk_data.get("risk_factors", [])
                            except:
                                pass
                        
                        elif tool_name == "symptom_analysis":
                            try:
                                symptom_data = json.loads(observation)
                                symptoms = symptom_data.get("symptoms", [])
                            except:
                                pass
                        
                        elif tool_name == "generate_recommendations":
                            try:
                                recommendations = json.loads(observation)
                            except:
                                pass
            
            # Generate comprehensive patient education using the extracted data
            patient_education_tool = PatientEducationTool()
            education_data = {
                "answers": [],  # Would be populated from actual questionnaire data
                "risk_assessment": {"level": risk_level},
                "symptoms_analysis": {"primary_symptoms": symptoms}
            }
            
            try:
                education_result = patient_education_tool._run(json.dumps(education_data))
                education_info = json.loads(education_result)
                patient_education_content = education_info.get("education_content", "Based on your responses, we've conducted a comprehensive analysis of your oral health status.")
                summary_paragraph = education_info.get("summary_paragraph", "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status.")
            except Exception as e:
                logger.warning(f"Failed to generate patient education: {str(e)}")
                patient_education_content = "Your oral health is important for your overall well-being. Regular dental check-ups, proper oral hygiene including brushing twice daily and flossing, avoiding tobacco and excessive alcohol, and maintaining a balanced diet are key to good oral health. If you're experiencing any symptoms or concerns, please consult with a healthcare professional for proper evaluation and personalized guidance."
                summary_paragraph = "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status."
            
            return {
                "analysis_summary": output,
                "summary_paragraph": summary_paragraph,
                "risk_assessment": {
                    "level": risk_level,
                    "confidence": 0.8,
                    "key_factors": risk_factors
                },
                "symptoms_analysis": {
                    "primary_symptoms": symptoms,
                    "symptom_severity": "Moderate",
                    "concerning_patterns": ["Identified via analysis"]
                },
                "recommendations": {
                    "immediate_actions": recommendations.get("immediate_actions", []),
                    "lifestyle_changes": recommendations.get("lifestyle_changes", []),
                    "medical_follow_up": recommendations.get("medical_follow_up", [])
                },
                "next_steps": [
                    "Review the detailed analysis",
                    "Follow the provided recommendations",
                    "Schedule appropriate follow-up care"
                ],
                "patient_education": patient_education_content,
                "follow_up_questions": [
                    "Do you have any questions about the analysis?",
                    "Would you like to discuss any specific concerns?"
                ],
                "metadata": {
                    "agent_used": True,
                    "tools_utilized": ["risk_assessment", "symptom_analysis", "generate_recommendations", "patient_education"],
                    "analysis_timestamp": self._get_current_timestamp()
                },
                "raw_agent_output": output
            }
            
        except Exception as e:
            return self._create_error_response(f"Error parsing agent response: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response when analysis fails"""
        
        return {
            "analysis_summary": f"Analysis encountered an error: {error_message}",
            "risk_assessment": {
                "level": "Unknown",
                "confidence": 0.0,
                "key_factors": ["Error in analysis"]
            },
            "symptoms_analysis": {
                "primary_symptoms": ["Unable to analyze"],
                "symptom_severity": "Unknown",
                "concerning_patterns": ["Analysis failed"]
            },
            "recommendations": {
                "immediate_actions": ["Consult with a healthcare professional"],
                "lifestyle_changes": ["Maintain good oral hygiene"],
                "medical_follow_up": ["Schedule dental appointment"]
            },
            "next_steps": [
                "Contact support for assistance",
                "Try the analysis again",
                "Consult with a healthcare professional"
            ],
            "patient_education": "We apologize for the technical difficulty. Please consult with a healthcare professional for assessment.",
            "follow_up_questions": [
                "Would you like to try the analysis again?",
                "Do you need assistance with scheduling an appointment?"
            ],
            "metadata": {
                "error": True,
                "error_message": error_message,
                "analysis_timestamp": self._get_current_timestamp()
            }
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _create_safe_llm_wrapper(self):
        """Create a wrapper for the LLM that validates messages before sending"""
        original_llm = self.llm
        
        class SafeLLMWrapper:
            def __init__(self, llm):
                self.llm = llm
            
            def _validate_messages(self, messages):
                """Validate messages to ensure no null content"""
                validated_messages = []
                for i, msg in enumerate(messages):
                    logger.info(f"Validating message {i}: {type(msg)}")
                    
                    # Handle different message types
                    if hasattr(msg, 'content'):
                        if msg.content is None:
                            logger.warning(f"Message {i} has null content, replacing with empty string")
                            # Create a new message with empty content
                            if hasattr(msg, '__class__'):
                                new_msg = msg.__class__(content="")
                                validated_messages.append(new_msg)
                            else:
                                # Fallback: create a HumanMessage with empty content
                                from langchain_core.messages import HumanMessage
                                validated_messages.append(HumanMessage(content=""))
                        elif not isinstance(msg.content, str):
                            logger.warning(f"Message {i} content is not a string: {type(msg.content)}")
                            # Convert to string
                            if hasattr(msg, '__class__'):
                                new_msg = msg.__class__(content=str(msg.content))
                                validated_messages.append(new_msg)
                            else:
                                # Fallback: create a HumanMessage with string content
                                from langchain_core.messages import HumanMessage
                                validated_messages.append(HumanMessage(content=str(msg.content)))
                        else:
                            validated_messages.append(msg)
                    else:
                        logger.warning(f"Message {i} has no content attribute, skipping")
                        # Skip messages without content attribute
                        continue
                
                logger.info(f"Validated {len(validated_messages)} messages out of {len(messages)} original messages")
                return validated_messages
            
            def invoke(self, messages, **kwargs):
                """Invoke the LLM with validated messages"""
                try:
                    logger.info(f"Received {len(messages)} messages for validation")
                    
                    # Validate messages before sending
                    validated_messages = self._validate_messages(messages)
                    
                    if not validated_messages:
                        logger.error("No valid messages after validation")
                        raise ValueError("No valid messages to send to LLM")
                    
                    logger.info(f"Invoking LLM with {len(validated_messages)} validated messages")
                    
                    # Log each message content for debugging
                    for i, msg in enumerate(validated_messages):
                        logger.info(f"Message {i}: {type(msg).__name__} - Content length: {len(msg.content) if hasattr(msg, 'content') else 'No content'}")
                    
                    return self.llm.invoke(validated_messages, **kwargs)
                except Exception as e:
                    logger.error(f"LLM invocation failed: {str(e)}", exc_info=True)
                    raise e
            
            def __getattr__(self, name):
                """Delegate other attributes to the original LLM"""
                return getattr(self.llm, name)
        
        return SafeLLMWrapper(original_llm)
    
    def _fallback_to_llm_analysis(self, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback to direct LLM analysis when agent fails"""
        try:
            logger.info("Using fallback LLM analysis")
            
            # Use the tools directly
            risk_tool = RiskAssessmentTool()
            symptom_tool = SymptomAnalysisTool()
            rec_tool = RecommendationTool()
            
            # Get questionnaire data as JSON string
            questionnaire_json = json.dumps(questionnaire_data)
            
            # Run tools
            risk_result = risk_tool._run(questionnaire_json)
            symptom_result = symptom_tool._run(questionnaire_json)
            
            # Parse results
            risk_data = json.loads(risk_result)
            symptom_data = json.loads(symptom_result)
            
            # Generate recommendations
            analysis_data = {
                "risk_level": risk_data.get("risk_level", "Unknown"),
                "symptoms": symptom_data.get("symptoms", []),
                "risk_factors": risk_data.get("risk_factors", [])
            }
            
            rec_result = rec_tool._run(json.dumps(analysis_data))
            rec_data = json.loads(rec_result)
            
            # Generate patient education using the extracted data
            patient_education_tool = PatientEducationTool()
            education_data = {
                "answers": questionnaire_data.get("answers", []),
                "risk_assessment": {"level": risk_data.get("risk_level", "Unknown")},
                "symptoms_analysis": {"primary_symptoms": symptom_data.get("symptoms", [])}
            }
            
            try:
                education_result = patient_education_tool._run(json.dumps(education_data))
                education_info = json.loads(education_result)
                patient_education_content = education_info.get("education_content", "Based on your responses, we've conducted a comprehensive analysis of your oral health status.")
                summary_paragraph = education_info.get("summary_paragraph", "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status.")
            except Exception as e:
                logger.warning(f"Failed to generate patient education in fallback: {str(e)}")
                patient_education_content = "Your oral health is important for your overall well-being. Regular dental check-ups, proper oral hygiene including brushing twice daily and flossing, avoiding tobacco and excessive alcohol, and maintaining a balanced diet are key to good oral health. If you're experiencing any symptoms or concerns, please consult with a healthcare professional for proper evaluation and personalized guidance."
                summary_paragraph = "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status."
            
            # Format response
            return {
                "analysis_summary": f"Based on your responses, we've identified {len(risk_data.get('risk_factors', []))} risk factors and {len(symptom_data.get('symptoms', []))} symptoms.",
                "summary_paragraph": summary_paragraph,
                "risk_assessment": {
                    "level": risk_data.get("risk_level", "Unknown"),
                    "confidence": 0.8,
                    "key_factors": risk_data.get("risk_factors", [])
                },
                "symptoms_analysis": {
                    "primary_symptoms": symptom_data.get("symptoms", []),
                    "symptom_severity": symptom_data.get("severity", "Unknown"),
                    "concerning_patterns": symptom_data.get("concerning_symptoms", [])
                },
                "recommendations": {
                    "immediate_actions": rec_data.get("immediate_actions", []),
                    "lifestyle_changes": rec_data.get("lifestyle_changes", []),
                    "medical_follow_up": rec_data.get("medical_follow_up", [])
                },
                "next_steps": [
                    "Review the detailed analysis",
                    "Follow the provided recommendations",
                    "Schedule appropriate follow-up care"
                ],
                "patient_education": patient_education_content,
                "follow_up_questions": [
                    "Do you have any questions about the analysis?",
                    "Would you like to discuss any specific concerns?"
                ],
                "metadata": {
                    "agent_used": False,
                    "fallback_used": True,
                    "tools_utilized": ["risk_assessment", "symptom_analysis", "generate_recommendations", "patient_education"],
                    "analysis_timestamp": self._get_current_timestamp()
                }
            }
            
        except Exception as e:
            logger.error(f"Fallback analysis failed: {str(e)}", exc_info=True)
            return self._create_error_response(f"Fallback analysis failed: {str(e)}")
    
    def get_quick_analysis(self, questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get a quick analysis without full agent processing"""
        
        try:
            # Use just the risk assessment tool for quick analysis
            risk_tool = RiskAssessmentTool()
            risk_result = risk_tool._run(json.dumps(questionnaire_data))
            risk_data = json.loads(risk_result)
            
            return {
                "risk_level": risk_data.get("risk_level", "Unknown"),
                "risk_factors": risk_data.get("risk_factors", []),
                "recommendation": "Consult with a healthcare professional for detailed assessment"
            }
            
        except Exception as e:
            return {
                "risk_level": "Unknown",
                "risk_factors": [],
                "recommendation": "Error in analysis - please consult with a healthcare professional"
            }
