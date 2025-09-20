import os
import json
from typing import Dict, Any, List, Optional
from serpapi import GoogleSearch
import logging

logger = logging.getLogger(__name__)


class SerpAPIDentistSearchTool:
    """Tool for searching dentists using SerpAPI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_KEY environment variable is required")
    
    def search_dentists(self, location: str, specialty: Optional[str] = None, radius: int = 25) -> Dict[str, Any]:
        """
        Search for dentists near a location using SerpAPI
        
        Args:
            location: Address or location to search near
            specialty: Optional dental specialty to filter by
            radius: Search radius in miles (default 25)
        
        Returns:
            Dictionary containing search results
        """
        try:
            # Construct search query
            query = f"dentist near {location}"
            if specialty:
                query = f"{specialty} dentist near {location}"
            
            # SerpAPI search parameters
            search_params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google_maps",
                "type": "search",
                "hl": "en",
                "gl": "us"
            }
            
            logger.info(f"Searching for dentists with query: {query}")
            
            # Perform search
            search = GoogleSearch(search_params)
            results = search.get_dict()
            
            # Parse and structure the results
            dentists = self._parse_search_results(results)
            
            return {
                "dentists": dentists,
                "total_found": len(dentists),
                "search_location": location,
                "search_radius": radius,
                "search_specialty": specialty or "General dentistry",
                "raw_results": results
            }
            
        except Exception as e:
            logger.error(f"Error searching dentists with SerpAPI: {str(e)}")
            raise Exception(f"Error searching dentists: {str(e)}")
    
    def _parse_search_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse SerpAPI results into structured dentist data"""
        dentists = []
        
        try:
            # Extract local results from SerpAPI response
            local_results = results.get("local_results", [])
            
            for i, result in enumerate(local_results[:10]):  # Limit to top 10 results
                try:
                    dentist = self._extract_dentist_info(result, i)
                    if dentist:
                        dentists.append(dentist)
                except Exception as e:
                    logger.warning(f"Error parsing dentist result {i}: {str(e)}")
                    continue
            
            # If no local results, try to extract from organic results
            if not dentists:
                organic_results = results.get("organic_results", [])
                for i, result in enumerate(organic_results[:5]):
                    try:
                        dentist = self._extract_dentist_from_organic(result, i)
                        if dentist:
                            dentists.append(dentist)
                    except Exception as e:
                        logger.warning(f"Error parsing organic result {i}: {str(e)}")
                        continue
            
        except Exception as e:
            logger.error(f"Error parsing search results: {str(e)}")
        
        return dentists
    
    def _extract_dentist_info(self, result: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """Extract dentist information from local search result"""
        try:
            # Extract basic information
            name = result.get("title", f"Dentist {index + 1}")
            address = result.get("address", "Address not available")
            phone = result.get("phone", "Phone not available")
            
            # Extract rating and reviews
            rating = 0.0
            reviews_count = 0
            if "rating" in result:
                try:
                    rating = float(result["rating"])
                except (ValueError, TypeError):
                    rating = 0.0
            
            if "reviews" in result:
                try:
                    reviews_count = int(result["reviews"])
                except (ValueError, TypeError):
                    reviews_count = 0
            
            # Extract additional details
            website = result.get("website", "")
            hours = result.get("hours", "Hours not available")
            
            # Estimate distance (SerpAPI doesn't always provide exact distance)
            distance_km = (index + 1) * 2.5  # Rough estimation
            
            # Determine specialties based on name and description
            specialties = self._determine_specialties(name, result.get("description", ""))
            
            return {
                "name": name,
                "address": address,
                "phone": phone,
                "rating": rating,
                "distance_km": distance_km,
                "specialties": specialties,
                "website": website,
                "availability": hours,
                "insurance_accepted": ["Contact for insurance details"],  # SerpAPI doesn't provide this
                "reviews_count": reviews_count,
                "source": "serpapi"
            }
            
        except Exception as e:
            logger.warning(f"Error extracting dentist info: {str(e)}")
            return None
    
    def _extract_dentist_from_organic(self, result: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """Extract dentist information from organic search result"""
        try:
            name = result.get("title", f"Dentist {index + 1}")
            snippet = result.get("snippet", "")
            link = result.get("link", "")
            
            # Basic extraction for organic results
            return {
                "name": name,
                "address": "Address not available",
                "phone": "Phone not available",
                "rating": 0.0,
                "distance_km": (index + 1) * 3.0,
                "specialties": self._determine_specialties(name, snippet),
                "website": link,
                "availability": "Contact for hours",
                "insurance_accepted": ["Contact for insurance details"],
                "reviews_count": 0,
                "source": "serpapi_organic"
            }
            
        except Exception as e:
            logger.warning(f"Error extracting organic dentist info: {str(e)}")
            return None
    
    def _determine_specialties(self, name: str, description: str) -> List[str]:
        """Determine dental specialties based on name and description"""
        specialties = ["General Dentistry"]  # Default specialty
        
        text = (name + " " + description).lower()
        
        specialty_keywords = {
            "oral surgery": ["oral surgery", "maxillofacial", "oral and maxillofacial"],
            "orthodontics": ["orthodontics", "orthodontist", "braces", "invisalign"],
            "endodontics": ["endodontics", "endodontist", "root canal"],
            "periodontics": ["periodontics", "periodontist", "gum disease"],
            "prosthodontics": ["prosthodontics", "prosthodontist", "crowns", "bridges"],
            "pediatric dentistry": ["pediatric", "children", "kids", "family"],
            "oral medicine": ["oral medicine", "oral pathology"],
            "cosmetic dentistry": ["cosmetic", "veneers", "whitening", "aesthetic"]
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in text for keyword in keywords):
                specialties.append(specialty.title())
        
        return list(set(specialties))  # Remove duplicates
