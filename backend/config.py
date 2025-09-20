import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # AI/ML API Configuration
    AIMLAPI_KEY: str = os.getenv("AIMLAPI_KEY", "")
    AIMLAPI_BASE_URL: str = os.getenv("AIMLAPI_BASE_URL", "https://api.aimlapi.com/v1")
    AIMLAPI_MODEL: str = os.getenv("AIMLAPI_MODEL", "gpt-4o")
    
    # SerpAPI Configuration
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
    
    # LangChain Configuration
    USE_AGENT: bool = os.getenv("USE_AGENT", "true").lower() == "true"
    AGENT_VERBOSE: bool = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "3"))
    
    # Analysis Configuration
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    FALLBACK_ENABLED: bool = os.getenv("FALLBACK_ENABLED", "true").lower() == "true"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = os.getenv("LOG_FILE", "oral_detection.log")
    
    # API Configuration
    API_TITLE: str = "Oral Detection Backend"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "AI-powered oral health analysis using LangChain and AI/ML API"
    
    @classmethod
    def setup_logging(cls):
        """Setup logging configuration"""
        # Convert string log level to logging constant
        log_level = getattr(logging, cls.LOG_LEVEL.upper(), logging.INFO)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format=cls.LOG_FORMAT,
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        
        # Set specific logger levels
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("fastapi").setLevel(logging.INFO)
        logging.getLogger("langchain").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        if not cls.AIMLAPI_KEY:
            raise ValueError("AIMLAPI_KEY environment variable is required")
        if not cls.SERPAPI_KEY:
            print("Warning: SERPAPI_KEY environment variable is not set. Dentist search will use mock data.")
        return True

# Create global settings instance
settings = Settings()

# Validate configuration on import
try:
    settings.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please set the AIMLAPI_KEY environment variable")