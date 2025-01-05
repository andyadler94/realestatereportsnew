from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from .api.properties import router as properties_router

# Create reports directory if it doesn't exist
os.makedirs("reports", exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving reports
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

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
        "documentation": "/docs",
        "redoc": "/redoc"
    } 