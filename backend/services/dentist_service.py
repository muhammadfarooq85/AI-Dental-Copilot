from typing import Dict, Any, Optional, List
from services.dentist_agent import DentistSearchAgent
import logging

logger = logging.getLogger(__name__)


class DentistService:
    """Service for handling dentist search and recommendations using LangChain agent"""
    
    def __init__(self):
        try:
            self.dentist_agent = DentistSearchAgent()
            self.use_agent = True
            logger.info("DentistSearchAgent initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize DentistSearchAgent: {str(e)}. Falling back to mock data.")
            self.dentist_agent = None
            self.use_agent = False
            self.mock_dentists = self._get_mock_dentists()
    
    def find_dentists(self, address: str, city: Optional[str] = None, state: Optional[str] = None, 
                     country: str = "US", radius_km: int = 25, specialty: Optional[str] = None) -> Dict[str, Any]:
        """Find nearby dentists based on location and specialty using LangChain agent"""
        
        if self.use_agent and self.dentist_agent:
            try:
                logger.info(f"Using LangChain agent to search for dentists near {address}")
                return self.dentist_agent.find_dentists(
                    address=address,
                    city=city,
                    state=state,
                    country=country,
                    radius_km=radius_km,
                    specialty=specialty
                )
            except Exception as e:
                logger.error(f"Agent search failed: {str(e)}. Falling back to mock data.")
                return self._fallback_to_mock_search(address, city, state, country, radius_km, specialty)
        else:
            logger.info("Using mock data for dentist search")
            return self._fallback_to_mock_search(address, city, state, country, radius_km, specialty)
    
    def _fallback_to_mock_search(self, address: str, city: Optional[str], state: Optional[str], 
                                country: str, radius_km: int, specialty: Optional[str]) -> Dict[str, Any]:
        """Fallback to mock data when agent is not available"""
        
        # Filter by specialty if specified
        filtered_dentists = self.mock_dentists.copy()
        if specialty:
            filtered_dentists = [d for d in filtered_dentists if any(specialty.lower() in s.lower() for s in d["specialties"])]
        
        # Sort by rating and distance
        filtered_dentists.sort(key=lambda x: (x["rating"], -x["distance_km"]), reverse=True)
        
        recommendations = [
            "Consider scheduling a consultation with the highest-rated specialist",
            "Check insurance coverage before making an appointment",
            "Ask about availability for urgent concerns",
            "Prepare a list of questions about your symptoms"
        ]
        
        return {
            "dentists": filtered_dentists,
            "total_found": len(filtered_dentists),
            "search_location": f"{address}, {city or ''}, {state or ''}",
            "search_radius": radius_km,
            "recommendations": recommendations,
            "additional_info": {
                "search_specialty": specialty or "General dentistry",
                "search_timestamp": "2024-01-01T00:00:00Z",
                "coverage_area": f"{radius_km}km radius",
                "mock_data_used": True
            }
        }
    
    def get_specialties(self) -> List[str]:
        """Get list of dental specialties"""
        return [
            "General Dentistry",
            "Oral and Maxillofacial Surgery",
            "Oral Pathology",
            "Oral Medicine",
            "Periodontics",
            "Endodontics",
            "Orthodontics",
            "Prosthodontics",
            "Pediatric Dentistry",
            "Oral Cancer Specialist",
            "Head and Neck Surgery"
        ]
    
    def get_emergency_contacts(self) -> Dict[str, Any]:
        """Get emergency dental contacts and information"""
        return {
            "emergency_services": [
                {
                    "name": "Emergency Dental Service",
                    "phone": "1-800-DENTIST",
                    "description": "24/7 emergency dental care"
                },
                {
                    "name": "Oral Cancer Emergency",
                    "phone": "911",
                    "description": "For immediate medical emergencies"
                }
            ],
            "urgent_care_centers": [
                {
                    "name": "Urgent Care Dental",
                    "description": "Walk-in dental urgent care",
                    "hours": "24/7"
                }
            ],
            "when_to_seek_emergency": [
                "Severe pain that doesn't respond to over-the-counter medication",
                "Significant bleeding from the mouth",
                "Difficulty breathing or swallowing",
                "Signs of infection (fever, swelling, pus)",
                "Trauma to the mouth or face"
            ]
        }
    
    def _get_mock_dentists(self) -> List[Dict[str, Any]]:
        """Get mock dentist data for testing"""
        return [
            {
                "name": "Dr. Sarah Johnson - Oral Medicine Specialist",
                "address": "123 Main St, {city}, {state}",
                "phone": "(555) 123-4567",
                "rating": 4.8,
                "distance_km": 2.3,
                "specialties": ["Oral Medicine", "Oral Pathology"],
                "website": "https://example-dental.com",
                "availability": "Monday-Friday 9AM-5PM",
                "insurance_accepted": ["Aetna", "Blue Cross", "Cigna"],
                "reviews_count": 127
            },
            {
                "name": "Dr. Michael Chen - Oral & Maxillofacial Surgery",
                "address": "456 Oak Ave, {city}, {state}",
                "phone": "(555) 234-5678",
                "rating": 4.6,
                "distance_km": 5.7,
                "specialties": ["Oral Surgery", "Head & Neck Surgery"],
                "website": "https://chen-oral-surgery.com",
                "availability": "Monday-Thursday 8AM-6PM",
                "insurance_accepted": ["Aetna", "Medicare", "Medicaid"],
                "reviews_count": 89
            },
            {
                "name": "Dr. Emily Rodriguez - General Dentistry",
                "address": "789 Pine St, {city}, {state}",
                "phone": "(555) 345-6789",
                "rating": 4.7,
                "distance_km": 3.1,
                "specialties": ["General Dentistry", "Preventive Care"],
                "website": "https://rodriguez-dental.com",
                "availability": "Monday-Saturday 8AM-7PM",
                "insurance_accepted": ["Blue Cross", "Delta Dental", "MetLife"],
                "reviews_count": 203
            },
            {
                "name": "Dr. James Wilson - Oral Cancer Specialist",
                "address": "321 Elm St, {city}, {state}",
                "phone": "(555) 456-7890",
                "rating": 4.9,
                "distance_km": 4.2,
                "specialties": ["Oral Cancer", "Oral Pathology", "Oral Medicine"],
                "website": "https://wilson-oral-cancer.com",
                "availability": "Tuesday-Friday 9AM-4PM",
                "insurance_accepted": ["Aetna", "Blue Cross", "Cigna", "Medicare"],
                "reviews_count": 156
            }
        ]
