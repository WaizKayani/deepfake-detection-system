"""
Main FastAPI application for the Media Authentication System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.api.v1.endpoints import upload, analyze, logs, models, health

# Create FastAPI app instance
app = FastAPI(
    title="Media Authentication System",
    description="AI-powered deepfake detection for images, videos, and audio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Include API routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])
app.include_router(models.router, prefix="/api/v1", tags=["models"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Media Authentication System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "media-authentication-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    ) 