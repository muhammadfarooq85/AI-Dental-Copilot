from fastapi import APIRouter, HTTPException

from models import LocationRequest, DentistRecommendationResponse
from services.dentist_service import DentistService

router = APIRouter(prefix="/dentist", tags=["dentist"])

# Initialize service
dentist_service = DentistService()


@router.post("/find-dentists", response_model=DentistRecommendationResponse)
async def find_dentists(request: LocationRequest):
    """Find nearby dentists"""
    try:
        result = dentist_service.find_dentists(
            address=request.address,
            city=request.city,
            state=request.state,
            country=request.country,
            radius_km=request.radius_km,
            specialty=request.specialty
        )
        
        return DentistRecommendationResponse(
            dentists=result["dentists"],
            total_found=result["total_found"],
            search_location=result["search_location"],
            search_radius=result["search_radius"],
            recommendations=result["recommendations"],
            additional_info=result["additional_info"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding dentists: {str(e)}")
