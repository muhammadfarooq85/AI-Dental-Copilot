# AI Dental Copilot Backend

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
│   ├── oral_health_agent.py  # LangChain agent for comprehensive oral health analysis
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
- **Questionnaire Analysis**: Comprehensive risk assessment and analysis using LangChain oral health agent
- **Intelligent Dentist Search**: Find nearby dental specialists using LangChain agents and SerpAPI
- **Real-time Data**: Live dentist search with ratings, reviews, and contact information
- **Specialty Filtering**: Search for specific dental specialties (oral surgery, orthodontics, etc.)
- **RESTful API**: Clean, documented API endpoints
- **Modular Architecture**: Well-organized code structure for maintainability

## API Endpoints

### Detection

- `POST /detection/analyze` - Analyze uploaded image

### Questionnaire

- `POST /questionnaire/analyze` - Analyze questionnaire responses

### Dentist

- `POST /dentist/find-dentists` - Find nearby dentists

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

## Oral Health Agent Implementation

The questionnaire analysis functionality uses a sophisticated LangChain agent (`oral_health_agent.py`) that provides comprehensive oral health assessment and analysis. This agent is the core component used by the questionnaire service for intelligent analysis of patient responses.

### Architecture

The Oral Health Agent consists of four specialized tools that work together to provide comprehensive analysis:

1. **RiskAssessmentTool**: Calculates risk factors and determines overall risk level
2. **SymptomAnalysisTool**: Analyzes symptoms and their patterns from questionnaire responses
3. **RecommendationTool**: Generates personalized recommendations based on analysis results
4. **PatientEducationTool**: Creates detailed educational content about oral health

### Key Features

- **Comprehensive Risk Assessment**: Evaluates 5 key risk factors based on questionnaire responses
- **Symptom Pattern Analysis**: Categorizes and analyzes symptoms across different categories (visual, pain, functional, systemic)
- **Personalized Recommendations**: Generates tailored advice including immediate actions, lifestyle changes, and medical follow-up
- **Patient Education**: Creates detailed, personalized educational content explaining oral health importance and preventive care
- **Fallback Support**: Includes robust error handling with fallback to direct LLM analysis
- **Memory Management**: Maintains conversation context for better analysis

### Risk Assessment Logic

The agent evaluates responses to 5 critical questions:

1. Sores or ulcers in mouth (q1)
2. Swelling or redness in mouth (q2)
3. Unusual pain in mouth (q3)
4. Changes in inner lining of mouth (q4)
5. Lumps or thickened areas in mouth or neck (q5)

**Risk Level Calculation:**

- **High Risk**: 3 or more "yes" responses
- **Medium Risk**: 2 "yes" responses
- **Low Risk**: 1 or fewer "yes" responses

### Agent Tools

#### RiskAssessmentTool

- Calculates risk factors based on questionnaire responses
- Maps question IDs to specific risk factors
- Determines overall risk level (High/Medium/Low)
- Returns structured risk assessment data

#### SymptomAnalysisTool

- Analyzes symptoms from questionnaire responses
- Categorizes symptoms into visual, pain, functional, and systemic categories
- Determines symptom severity (Mild/Moderate/Severe)
- Identifies concerning symptoms that require immediate attention

#### RecommendationTool

- Generates personalized recommendations based on risk level and symptoms
- Provides immediate actions, lifestyle changes, and medical follow-up advice
- Tailors recommendations to specific risk factors and symptoms
- Includes monitoring and prevention strategies

#### PatientEducationTool

- Creates comprehensive educational content about oral health
- Generates personalized content based on patient's specific responses
- Explains risk factors, symptoms, and preventive care
- Provides clear, patient-friendly language for better understanding

### Usage in Questionnaire Service

The `QuestionnaireService` uses the Oral Health Agent as its primary analysis engine:

```python
# Initialize with agent enabled (default)
questionnaire_service = QuestionnaireService(use_agent=True)

# Analyze questionnaire responses
result = questionnaire_service.analyze_questionnaire(answers, patient_info)
```

### Configuration

The agent requires the following environment variables:

- `AIMLAPI_KEY`: Required for LLM functionality
- `AIMLAPI_BASE_URL`: Optional, defaults to "https://api.aimlapi.com/v1"

### Error Handling

The agent includes robust error handling:

- **Agent Fallback**: Falls back to direct LLM analysis if agent fails
- **Tool Fallback**: Individual tools have error handling with graceful degradation
- **Response Validation**: Validates and sanitizes all responses
- **Logging**: Comprehensive logging for debugging and monitoring

### Integration with Questionnaire Service

The questionnaire service automatically uses the oral health agent when `use_agent=True` (default). The service handles:

- Input validation and formatting
- Agent invocation and response parsing
- Fallback to LLM service if agent fails
- Response formatting for API consistency

## Development

The project follows a modular architecture:

- **Services**: Contain business logic and data processing
- **Routers**: Handle HTTP requests and responses
- **Models**: Define data schemas using Pydantic
- **Config**: Centralized configuration management
- **Agents**: LangChain agents for intelligent data processing

This structure makes the codebase maintainable, testable, and easy to extend.
