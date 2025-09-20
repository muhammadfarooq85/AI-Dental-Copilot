from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import base64

from models import DetectionResponse, DetectionRequest
from services.model_service import ModelInference

router = APIRouter(prefix="/detection", tags=["detection"])


@router.post("/analyze", response_model=DetectionResponse)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze an uploaded image for oral cancer detection"""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Please upload a JPEG or PNG image."
            )
        
        # Read and process image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Initialize model inference
        model_inference = ModelInference()
        
        # Perform inference
        result = model_inference.predict(image_array)
        
        return DetectionResponse(
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            recommendations=result["recommendations"],
            image_analysis=result["image_analysis"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

