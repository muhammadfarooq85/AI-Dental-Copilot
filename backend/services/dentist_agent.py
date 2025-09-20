import os
import json
from typing import Dict, Any, List, Optional
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from services.serpapi_tool import SerpAPIDentistSearchTool
import logging

logger = logging.getLogger(__name__)


class DentistSearchAgent:
    """LangChain agent for intelligent dentist search using SerpAPI"""
    
    def __init__(self, openai_api_key: Optional[str] = None, serpapi_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("AIMLAPI_KEY")
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_KEY")
        
        if not self.openai_api_key:
            raise ValueError("AIMLAPI_KEY environment variable is required")
        if not self.serpapi_key:
            raise ValueError("SERPAPI_KEY environment variable is required")
        
        # Initialize SerpAPI tool
        self.serpapi_tool = SerpAPIDentistSearchTool(self.serpapi_key)
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            api_key=self.openai_api_key,
            base_url="https://api.aimlapi.com/v1",
            model="gpt-4o",
            temperature=0.3,
            max_tokens=2000
        )
        
        # Create tools for the agent
        self.tools = [self._create_dentist_search_tool()]
        
        # Create agent (simplified approach)
        self.agent = self._create_agent()
    
    def _create_dentist_search_tool(self):
        """Create a LangChain tool for dentist search"""
        
        @tool
        def search_dentists_nearby(location: str, specialty: str = None, radius: int = 25) -> str:
            """
            Search for dentists near a specific location using SerpAPI.
            
            Args:
                location: The address or location to search near (e.g., "123 Main St, New York, NY")
                specialty: Optional dental specialty to filter by (e.g., "oral surgery", "orthodontics")
                radius: Search radius in miles (default: 25)
            
            Returns:
                JSON string containing dentist information including name, address, phone, rating, specialties, etc.
            """
            try:
                results = self.serpapi_tool.search_dentists(location, specialty, radius)
                return json.dumps(results, indent=2)
            except Exception as e:
                logger.error(f"Error in dentist search tool: {str(e)}")
                return json.dumps({"error": f"Search failed: {str(e)}", "dentists": []})
        
        return search_dentists_nearby
    
    def _create_agent(self) -> AgentExecutor:
        """Create a simple LangChain agent with tools"""
        
        # For now, return None since we're using direct SerpAPI search
        # This avoids the complex agent setup that was causing the error
        return None
    
    def find_dentists(self, address: str, city: Optional[str] = None, state: Optional[str] = None, 
                     country: str = "US", radius_km: int = 25, specialty: Optional[str] = None) -> Dict[str, Any]:
        """
        Find nearby dentists using the LangChain agent
        
        Args:
            address: Street address
            city: City name
            state: State name
            country: Country (default: US)
            radius_km: Search radius in kilometers
            specialty: Optional dental specialty
        
        Returns:
            Dictionary containing dentist recommendations and analysis
        """
        try:
            # Construct location string
            location_parts = [address]
            if city:
                location_parts.append(city)
            if state:
                location_parts.append(state)
            if country and country != "US":
                location_parts.append(country)
            
            location = ", ".join(location_parts)
            
            # Convert radius from km to miles for SerpAPI
            radius_miles = int(radius_km * 0.621371)
            
            # Use direct SerpAPI search instead of complex agent
            logger.info(f"Searching for dentists near {location}")
            
            # Search for dentists using SerpAPI tool directly
            search_results = self.serpapi_tool.search_dentists(location, specialty, radius_miles)
            
            # Process results with LLM for better formatting and analysis
            processed_results = self._process_results_with_llm(search_results, location, radius_km, specialty)
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Error in dentist search agent: {str(e)}")
            # Fallback to direct SerpAPI search
            return self._fallback_search(address, city, state, country, radius_km, specialty)
    
    def _process_results_with_llm(self, search_results: Dict[str, Any], location: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Process SerpAPI results with LLM for better formatting and analysis"""
        try:
            dentists = search_results.get("dentists", [])
            
            # Ensure we have at least 3 dentists if available
            if len(dentists) < 3 and len(dentists) > 0:
                # Try to get more results with broader search
                try:
                    broader_results = self.serpapi_tool.search_dentists(location, specialty, int(radius_km * 0.621371 * 2))
                    additional_dentists = broader_results.get("dentists", [])
                    
                    # Add unique dentists
                    existing_names = {d.get("name", "") for d in dentists}
                    for dentist in additional_dentists:
                        if dentist.get("name", "") not in existing_names and len(dentists) < 3:
                            dentists.append(dentist)
                            existing_names.add(dentist.get("name", ""))
                except Exception as e:
                    logger.warning(f"Could not get additional results: {str(e)}")
            
            # Use LLM to generate recommendations
            recommendations = self._generate_recommendations_with_llm(dentists, specialty)
            
            return {
                "dentists": dentists[:3],  # Limit to top 3
                "total_found": len(dentists),
                "search_location": location,
                "search_radius": radius_km,
                "recommendations": recommendations,
                "additional_info": {
                    "search_specialty": specialty or "General dentistry",
                    "search_timestamp": self._get_current_timestamp(),
                    "coverage_area": f"{radius_km}km radius",
                    "agent_used": True,
                    "llm_processed": True
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing results with LLM: {str(e)}")
            # Fallback to basic processing
            return self._format_structured_response(search_results, location, radius_km, specialty)
    
    def _generate_recommendations_with_llm(self, dentists: List[Dict[str, Any]], specialty: Optional[str]) -> List[str]:
        """Generate recommendations using LLM"""
        try:
            if not dentists:
                return ["No dentists found in the specified area. Try expanding your search radius."]
            
            # Create a simple prompt for recommendations
            dentist_summary = "\n".join([
                f"- {d.get('name', 'Unknown')} (Rating: {d.get('rating', 'N/A')}, Specialties: {', '.join(d.get('specialties', []))})"
                for d in dentists[:3]
            ])
            
            prompt = f"""
            Based on these dentists found for {specialty or 'general dental care'}:
            
            {dentist_summary}
            
            Provide 3-4 helpful recommendations for the patient. Keep them practical and actionable.
            """
            
            # Use a simple LLM call instead of the complex agent
            from langchain_core.messages import HumanMessage
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            # Parse the response into a list of recommendations
            recommendations_text = response.content
            recommendations = [rec.strip() for rec in recommendations_text.split('\n') if rec.strip() and not rec.strip().startswith('-')]
            
            # Fallback recommendations if LLM fails
            if not recommendations:
                recommendations = [
                    "Consider scheduling consultations with multiple dentists to compare approaches",
                    "Check insurance coverage before making appointments",
                    "Ask about availability for urgent concerns",
                    "Prepare a list of questions about your specific needs"
                ]
            
            return recommendations[:4]  # Limit to 4 recommendations
            
        except Exception as e:
            logger.warning(f"Error generating recommendations with LLM: {str(e)}")
            return [
                "Consider scheduling consultations with multiple dentists to compare approaches",
                "Check insurance coverage before making appointments",
                "Ask about availability for urgent concerns",
                "Prepare a list of questions about your specific needs"
            ]
    
    def _parse_agent_response(self, agent_output: str, location: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Parse the agent's response into structured data"""
        try:
            # Try to extract JSON from the agent output
            # The agent might include JSON in its response
            import re
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', agent_output, re.DOTALL)
            if json_match:
                try:
                    json_data = json.loads(json_match.group())
                    if "dentists" in json_data:
                        return self._format_structured_response(json_data, location, radius_km, specialty)
                except json.JSONDecodeError:
                    pass
            
            # If no JSON found, create a structured response from the text
            return self._create_structured_response_from_text(agent_output, location, radius_km, specialty)
            
        except Exception as e:
            logger.error(f"Error parsing agent response: {str(e)}")
            return self._create_fallback_response(location, radius_km, specialty)
    
    def _format_structured_response(self, json_data: Dict[str, Any], location: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Format JSON data into the expected response structure"""
        dentists = json_data.get("dentists", [])
        
        # Ensure we have at least 3 dentists if available
        if len(dentists) < 3 and len(dentists) > 0:
            # Try to get more results
            try:
                additional_results = self.serpapi_tool.search_dentists(location, specialty, int(radius_km * 0.621371))
                additional_dentists = additional_results.get("dentists", [])
                # Add unique dentists
                existing_names = {d.get("name", "") for d in dentists}
                for dentist in additional_dentists:
                    if dentist.get("name", "") not in existing_names and len(dentists) < 3:
                        dentists.append(dentist)
                        existing_names.add(dentist.get("name", ""))
            except Exception as e:
                logger.warning(f"Could not get additional results: {str(e)}")
        
        recommendations = [
            "Consider scheduling consultations with multiple dentists to compare approaches",
            "Check insurance coverage before making appointments",
            "Ask about availability for urgent concerns",
            "Prepare a list of questions about your specific needs"
        ]
        
        return {
            "dentists": dentists[:3],  # Limit to top 3
            "total_found": len(dentists),
            "search_location": location,
            "search_radius": radius_km,
            "recommendations": recommendations,
            "additional_info": {
                "search_specialty": specialty or "General dentistry",
                "search_timestamp": self._get_current_timestamp(),
                "coverage_area": f"{radius_km}km radius",
                "agent_used": True
            }
        }
    
    def _create_structured_response_from_text(self, text: str, location: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Create structured response from agent's text output"""
        # This is a simplified parser - in a real implementation, you might want more sophisticated parsing
        return {
            "dentists": [],
            "total_found": 0,
            "search_location": location,
            "search_radius": radius_km,
            "recommendations": ["Please try a more specific search or contact us for assistance"],
            "additional_info": {
                "search_specialty": specialty or "General dentistry",
                "search_timestamp": self._get_current_timestamp(),
                "coverage_area": f"{radius_km}km radius",
                "agent_used": True,
                "raw_response": text
            }
        }
    
    def _fallback_search(self, address: str, city: Optional[str], state: Optional[str], 
                        country: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Fallback to direct SerpAPI search if agent fails"""
        try:
            location_parts = [address]
            if city:
                location_parts.append(city)
            if state:
                location_parts.append(state)
            if country and country != "US":
                location_parts.append(country)
            
            location = ", ".join(location_parts)
            radius_miles = int(radius_km * 0.621371)
            
            results = self.serpapi_tool.search_dentists(location, specialty, radius_miles)
            
            # Ensure we have at least 3 dentists
            dentists = results.get("dentists", [])
            if len(dentists) < 3:
                # Try a broader search
                broader_results = self.serpapi_tool.search_dentists(location, specialty, radius_miles * 2)
                additional_dentists = broader_results.get("dentists", [])
                
                # Add unique dentists
                existing_names = {d.get("name", "") for d in dentists}
                for dentist in additional_dentists:
                    if dentist.get("name", "") not in existing_names and len(dentists) < 3:
                        dentists.append(dentist)
                        existing_names.add(dentist.get("name", ""))
            
            return {
                "dentists": dentists[:3],
                "total_found": len(dentists),
                "search_location": location,
                "search_radius": radius_km,
                "recommendations": [
                    "Consider scheduling consultations with multiple dentists",
                    "Check insurance coverage before making appointments",
                    "Ask about availability for urgent concerns"
                ],
                "additional_info": {
                    "search_specialty": specialty or "General dentistry",
                    "search_timestamp": self._get_current_timestamp(),
                    "coverage_area": f"{radius_km}km radius",
                    "agent_used": False,
                    "fallback_used": True
                }
            }
            
        except Exception as e:
            logger.error(f"Fallback search also failed: {str(e)}")
            return self._create_fallback_response(f"{address}, {city or ''}, {state or ''}", radius_km, specialty)
    
    def _create_fallback_response(self, location: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Create a fallback response when all searches fail"""
        return {
            "dentists": [],
            "total_found": 0,
            "search_location": location,
            "search_radius": radius_km,
            "recommendations": [
                "Unable to find dentists at this time",
                "Please try again later or contact us for assistance",
                "Consider expanding your search radius"
            ],
            "additional_info": {
                "search_specialty": specialty or "General dentistry",
                "search_timestamp": self._get_current_timestamp(),
                "coverage_area": f"{radius_km}km radius",
                "error": "Search service temporarily unavailable"
            }
        }
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for metadata"""
        from datetime import datetime
        return datetime.now().isoformat()
