from fastapi import APIRouter, HTTPException

from models import QuestionnaireRequest, QuestionnaireResponse
from services.questionnaire_service import QuestionnaireService

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])

# Initialize service
questionnaire_service = QuestionnaireService()


@router.post("/analyze", response_model=QuestionnaireResponse)
async def analyze_questionnaire(request: QuestionnaireRequest):
    """Analyze questionnaire responses"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Received questionnaire analysis request with {len(request.answers)} answers")
        logger.debug(f"Request data: {request}")
        
        # Convert to dict format for analysis
        answers_dict = [answer.dict() for answer in request.answers]
        logger.debug(f"Converted answers: {answers_dict}")
        
        # Validate request data
        if not answers_dict:
            logger.error("No answers provided in request")
            raise HTTPException(status_code=400, detail="No answers provided")
        
        # Perform analysis
        logger.info("Starting questionnaire analysis")
        result = questionnaire_service.analyze_questionnaire(answers_dict, request.patient_info)
        logger.info("Questionnaire analysis completed")
        
        # Validate result structure
        required_fields = ["analysis", "risk_assessment", "recommendations", "next_steps", "confidence_score", "detailed_insights"]
        for field in required_fields:
            if field not in result:
                logger.warning(f"Missing field in result: {field}")
        
        logger.info("Returning questionnaire response")
        return QuestionnaireResponse(
            analysis=result.get("analysis", "Analysis completed"),
            summary_paragraph=result.get("summary_paragraph", "Based on your questionnaire responses, we've conducted a comprehensive analysis of your oral health status."),
            risk_assessment=result.get("risk_assessment", "Unable to assess risk"),
            recommendations=result.get("recommendations", []),
            next_steps=result.get("next_steps", []),
            confidence_score=result.get("confidence_score", 0.0),
            detailed_insights=result.get("detailed_insights", {}),
            patient_education=result.get("patient_education", ""),
            follow_up_questions=result.get("follow_up_questions", []),
            metadata=result.get("metadata", {})
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_questionnaire: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error analyzing questionnaire: {str(e)}")


# @router.get("/questions")
# async def get_questionnaire_questions():
#     """Get the standard questionnaire questions"""
#     questions = questionnaire_service.get_questions()
#     return {"questions": questions}


# @router.post("/quick-analysis")
# async def quick_analysis(request: QuestionnaireRequest):
#     """Quick analysis without full processing"""
#     try:
#         answers_dict = [answer.dict() for answer in request.answers]
#         result = questionnaire_service.quick_analysis(answers_dict)
#         return result
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error in quick analysis: {str(e)}")
