# Oral Cancer Detection Backend

A FastAPI-based backend service for oral cancer detection, questionnaire analysis, and intelligent dentist recommendations using LangChain agents and SerpAPI.

## Project Structure

```
OralDetetcionBakend/
├── main.py                 # Main FastAPI application entry point
├── config.py              # Application configuration settings
├── models.py              # Pydantic models for request/response schemas
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── services/             # Business logic services
│   ├── __init__.py
│   ├── model_service.py      # Image analysis and model inference
│   ├── questionnaire_service.py  # Questionnaire analysis logic
│   ├── dentist_service.py       # Dentist search and recommendations
│   ├── dentist_agent.py        # LangChain agent for intelligent dentist search
│   ├── serpapi_tool.py         # SerpAPI integration tool
│   └── llm_service.py          # LLM service for questionnaire analysis
├── routers/              # API route handlers
│   ├── __init__.py
│   ├── detection.py          # Image detection endpoints
│   ├── questionnaire.py      # Questionnaire endpoints
│   └── dentist.py            # Dentist search endpoints
├── utils/                # Utility functions
│   └── __init__.py
└── uploads/              # File upload directory
```

## Features

- **Image Analysis**: Upload images for oral cancer detection using AI models
- **Questionnaire Analysis**: Risk assessment based on patient responses using LangChain
- **Intelligent Dentist Search**: Find nearby dental specialists using LangChain agents and SerpAPI
- **Real-time Data**: Live dentist search with ratings, reviews, and contact information
- **Specialty Filtering**: Search for specific dental specialties (oral surgery, orthodontics, etc.)
- **RESTful API**: Clean, documented API endpoints
- **Modular Architecture**: Well-organized code structure for maintainability

## API Endpoints

### Detection

- `POST /detection/analyze` - Analyze uploaded image
- `POST /detection/analyze-base64` - Analyze base64 encoded image
- `GET /detection/model-info` - Get model information

### Questionnaire

- `POST /questionnaire/analyze` - Analyze questionnaire responses
- `GET /questionnaire/questions` - Get standard questions
- `POST /questionnaire/quick-analysis` - Quick risk assessment

### Dentist

- `POST /dentist/find-dentists` - Find nearby dentists
- `POST /dentist/recommend-specialist` - Find oral cancer specialists
- `GET /dentist/specialties` - Get dental specialties
- `GET /dentist/emergency-contacts` - Get emergency contacts

## Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python main.py
```

3. Access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Environment variables can be set in a `.env` file:

### Required

- `AIMLAPI_KEY`: API key for AI/ML services (required for LLM functionality)

### Optional

- `SERPAPI_KEY`: API key for SerpAPI (required for real dentist search data)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Auto-reload on changes (default: true)
- `LOG_LEVEL`: Logging level (default: info)

### Dentist Search Configuration

- Without `SERPAPI_KEY`: The system will use mock data for testing
- With `SERPAPI_KEY`: The system will use real-time data from SerpAPI for dentist search

## LangChain Agent Implementation

The dentist search functionality now uses a LangChain agent that intelligently searches for nearby dentists using SerpAPI. Here's how it works:

### Architecture

1. **SerpAPI Tool** (`services/serpapi_tool.py`): Direct integration with SerpAPI for real-time dentist data
2. **LangChain Agent** (`services/dentist_agent.py`): Intelligent agent that uses the SerpAPI tool
3. **Dentist Service** (`services/dentist_service.py`): Updated service that uses the agent with fallback to mock data

### Key Features

- **Real-time Search**: Uses SerpAPI to find actual dentists near the specified location
- **Intelligent Filtering**: Agent can filter by specialty (oral surgery, orthodontics, etc.)
- **Structured Results**: Returns at least 3 dentists with detailed information including:
  - Name and contact information
  - Address and distance
  - Rating and review count
  - Specialties offered
  - Availability/hours
  - Insurance information
- **Fallback Support**: Falls back to mock data if SerpAPI is unavailable

### Usage Example

```python
# The API automatically uses the LangChain agent when SERPAPI_KEY is set
POST /dentist/find-dentists
{
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "US",
    "radius_km": 25,
    "specialty": "oral surgery"
}
```

### Testing

Run the test script to verify the implementation:

```bash
python test_dentist_agent.py
```

## Development

The project follows a modular architecture:

- **Services**: Contain business logic and data processing
- **Routers**: Handle HTTP requests and responses
- **Models**: Define data schemas using Pydantic
- **Config**: Centralized configuration management
- **Agents**: LangChain agents for intelligent data processing

This structure makes the codebase maintainable, testable, and easy to extend.
