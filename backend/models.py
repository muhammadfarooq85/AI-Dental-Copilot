from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class DetectionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
    recommendations: list
    image_analysis: Dict[str, Any]


class DetectionRequest(BaseModel):
    image_base64: str
    patient_info: Dict[str, Any] = {}


class QuestionnaireAnswer(BaseModel):
    question_id: str
    answer: str
    question_text: str


class QuestionnaireRequest(BaseModel):
    answers: List[QuestionnaireAnswer]
    patient_info: Dict[str, Any] = {}
    additional_context: Optional[str] = None


class QuestionnaireResponse(BaseModel):
    analysis: str
    summary_paragraph: Optional[str] = None
    risk_assessment: str
    recommendations: List[str]
    next_steps: List[str]
    confidence_score: float
    detailed_insights: Dict[str, Any]
    patient_education: Optional[str] = None
    follow_up_questions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class LocationRequest(BaseModel):
    address: str
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "US"
    radius_km: int = 25
    specialty: Optional[str] = None


class DentistInfo(BaseModel):
    name: str
    address: str
    phone: str
    rating: float
    distance_km: float
    specialties: List[str]
    website: Optional[str] = None
    availability: str
    insurance_accepted: List[str]
    reviews_count: int


class DentistRecommendationResponse(BaseModel):
    dentists: List[DentistInfo]
    total_found: int
    search_location: str
    search_radius: int
    recommendations: List[str]
    additional_info: Dict[str, Any]
