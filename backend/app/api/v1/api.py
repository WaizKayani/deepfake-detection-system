"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import upload, analyze, logs, models, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(analyze.router, prefix="/analyze", tags=["analyze"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(health.router, prefix="/health", tags=["health"]) 