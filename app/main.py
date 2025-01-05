from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from typing import List

from .api.properties import router as properties_router

# Environment variables with defaults
PORT = int(os.getenv("PORT", "8000"))
RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", "development")
RAILWAY_STATIC_URL = os.getenv("RAILWAY_STATIC_URL", "")

# Create reports directory if it doesn't exist
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting up in {RAILWAY_ENVIRONMENT} environment...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Real Estate Reports API",
    description="API for generating detailed real estate property reports",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
allowed_origins = [
    "https://realestatereportsnew-production.up.railway.app",  # Railway production URL
    "http://localhost:3000",  # Local development
    "http://localhost:8000"
]

if RAILWAY_STATIC_URL:
    allowed_origins.append(RAILWAY_STATIC_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving reports
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# Include routers
app.include_router(properties_router, prefix="/api/v1/properties", tags=["properties"])

@app.get("/")
async def root():
    """
    Root endpoint returning API information.
    """
    return {
        "name": "Real Estate Reports API",
        "version": "1.0.0",
        "environment": RAILWAY_ENVIRONMENT,
        "documentation": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for Railway.app.
    """
    return {
        "status": "healthy",
        "environment": RAILWAY_ENVIRONMENT
    } 