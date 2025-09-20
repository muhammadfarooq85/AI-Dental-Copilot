from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from config import settings
from routers import detection, questionnaire, dentist

# Setup logging
settings.setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
logger.info(f"Log level: {settings.LOG_LEVEL}")
logger.info(f"Using agent: {settings.USE_AGENT}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(detection.router)
app.include_router(questionnaire.router)
app.include_router(dentist.router)


@app.get("/")
async def root():
    return {
        "message": "Oral Cancer Detection API",
        "version": settings.API_VERSION,
        "status": "active",
        "endpoints": {
            "detection": "/detection",
            "questionnaire": "/questionnaire", 
            "dentist": "/dentist",
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
    )