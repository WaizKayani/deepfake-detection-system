"""
Health check endpoints.
"""

from fastapi import APIRouter
import structlog
import psutil
import os

from app.core.database import db_manager
from app.core.monitoring import health_checker

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def health_check():
    """
    Basic health check endpoint.
    """
    
    return {
        "status": "healthy",
        "service": "media-authentication-system",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check():
    """
    Detailed health check with system metrics.
    """
    
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database health check
        db_healthy = await check_database_health()
        
        # Model health check
        model_healthy = await check_model_health()
        
        # Overall health
        overall_healthy = db_healthy and model_healthy and cpu_percent < 90 and memory.percent < 90
        
        return {
            "status": "healthy" if overall_healthy else "degraded",
            "service": "media-authentication-system",
            "version": "1.0.0",
            "system": {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_usage_percent": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2)
            },
            "components": {
                "database": {
                    "status": "healthy" if db_healthy else "unhealthy",
                    "connection": "established" if db_healthy else "failed"
                },
                "models": {
                    "status": "healthy" if model_healthy else "unhealthy",
                    "loaded": model_healthy
                },
                "api": {
                    "status": "healthy",
                    "endpoints": "all_available"
                }
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "service": "media-authentication-system",
            "version": "1.0.0",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }


@router.get("/database")
async def database_health_check():
    """
    Database-specific health check.
    """
    
    try:
        db_healthy = await check_database_health()
        
        return {
            "status": "healthy" if db_healthy else "unhealthy",
            "component": "database",
            "connection": "established" if db_healthy else "failed",
            "details": {
                "mongodb_uri": "configured",
                "database_name": "deepfake_detection",
                "collections": ["analysis_results", "file_uploads"]
            }
        }
        
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "component": "database",
            "error": str(e)
        }


@router.get("/models")
async def models_health_check():
    """
    Models-specific health check.
    """
    
    try:
        model_healthy = await check_model_health()
        
        return {
            "status": "healthy" if model_healthy else "unhealthy",
            "component": "models",
            "models": {
                "image_model": {
                    "status": "loaded" if model_healthy else "failed",
                    "type": "DummyImageModel",
                    "version": "1.0.0"
                },
                "video_model": {
                    "status": "loaded" if model_healthy else "failed",
                    "type": "DummyVideoModel",
                    "version": "1.0.0"
                },
                "audio_model": {
                    "status": "loaded" if model_healthy else "failed",
                    "type": "DummyAudioModel",
                    "version": "1.0.0"
                }
            }
        }
        
    except Exception as e:
        logger.error("Models health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "component": "models",
            "error": str(e)
        }


@router.get("/storage")
async def storage_health_check():
    """
    Storage health check.
    """
    
    try:
        # Check upload directories
        upload_dir = "./uploads"
        image_dir = os.path.join(upload_dir, "images")
        video_dir = os.path.join(upload_dir, "videos")
        audio_dir = os.path.join(upload_dir, "audio")
        
        dirs_exist = all([
            os.path.exists(upload_dir),
            os.path.exists(image_dir),
            os.path.exists(video_dir),
            os.path.exists(audio_dir)
        ])
        
        # Check disk space
        disk = psutil.disk_usage(upload_dir)
        disk_healthy = disk.percent < 90
        
        return {
            "status": "healthy" if dirs_exist and disk_healthy else "degraded",
            "component": "storage",
            "directories": {
                "upload_dir": {
                    "exists": os.path.exists(upload_dir),
                    "path": upload_dir
                },
                "image_dir": {
                    "exists": os.path.exists(image_dir),
                    "path": image_dir
                },
                "video_dir": {
                    "exists": os.path.exists(video_dir),
                    "path": video_dir
                },
                "audio_dir": {
                    "exists": os.path.exists(audio_dir),
                    "path": audio_dir
                }
            },
            "disk": {
                "usage_percent": disk.percent,
                "free_gb": round(disk.free / (1024**3), 2),
                "total_gb": round(disk.total / (1024**3), 2)
            }
        }
        
    except Exception as e:
        logger.error("Storage health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "component": "storage",
            "error": str(e)
        }


async def check_database_health() -> bool:
    """Check if database is healthy."""
    try:
        # Try to get database instance
        db = await db_manager.get_db()
        
        # Try a simple operation
        await db.command("ping")
        
        return True
        
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False


async def check_model_health() -> bool:
    """Check if models are healthy."""
    try:
        # In a real implementation, this would check if models are loaded
        # For now, just return True since we're using dummy models
        return True
        
    except Exception as e:
        logger.error("Model health check failed", error=str(e))
        return False


@router.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/container orchestration.
    """
    
    try:
        # Check all critical components
        db_ready = await check_database_health()
        models_ready = await check_model_health()
        
        # System resources
        cpu_ok = psutil.cpu_percent(interval=1) < 95
        memory_ok = psutil.virtual_memory().percent < 95
        
        ready = db_ready and models_ready and cpu_ok and memory_ok
        
        if ready:
            return {"status": "ready"}
        else:
            return {"status": "not_ready"}
            
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        return {"status": "not_ready"}


@router.get("/live")
async def liveness_check():
    """
    Liveness check for Kubernetes/container orchestration.
    """
    
    try:
        # Basic liveness check - just ensure the service is responding
        return {"status": "alive"}
        
    except Exception as e:
        logger.error("Liveness check failed", error=str(e))
        return {"status": "dead"} 