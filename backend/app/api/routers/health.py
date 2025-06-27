"""
Health router for system health checks and monitoring.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import psutil
import os

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "media-authentication-api",
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics."""
    try:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_info = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "media-authentication-api",
            "version": "1.0.0",
            "system": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory.percent}%",
                "memory_available": f"{memory.available / (1024**3):.2f} GB",
                "disk_usage": f"{disk.percent}%",
                "disk_free": f"{disk.free / (1024**3):.2f} GB"
            },
            "services": {
                "api": "healthy",
                "database": "unknown",  # Will be updated when MongoDB is connected
                "models": "healthy"
            }
        }
        
        return health_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health/ready")
async def readiness_check():
    """Readiness check for Kubernetes deployments."""
    try:
        # Check if all required services are ready
        ready = True
        checks = {
            "api": True,
            "database": False,  # Will be True when MongoDB is connected
            "models": True
        }
        
        if not all(checks.values()):
            ready = False
        
        return {
            "ready": ready,
            "timestamp": datetime.now().isoformat(),
            "checks": checks
        }
    except Exception as e:
        return {
            "ready": False,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        } 