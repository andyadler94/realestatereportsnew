# Real Estate Reports API

A FastAPI-based API for generating and managing real estate reports.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your environment variables:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

- The project follows a modular structure:
  - `app/`: Main application package
    - `api/`: API routes and endpoints
    - `models/`: Database models
    - `schemas/`: Pydantic models for request/response validation
    - `services/`: Business logic
    - `utils/`: Utility functions
  - `tests/`: Test suite

## Testing

Run tests with pytest:
```bash
pytest
``` 