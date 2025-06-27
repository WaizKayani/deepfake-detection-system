"""
Logs and history endpoints.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
import structlog

from app.core.database import db_manager

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def get_analysis_logs(
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    file_type: Optional[str] = Query(None),
    is_fake: Optional[bool] = Query(None),
    status: Optional[str] = Query(None)
):
    """
    Get analysis logs with optional filtering.
    """
    
    # Validate filters
    if file_type and file_type not in ["image", "video", "audio"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if status and status not in ["pending", "processing", "completed", "failed"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    # Get logs from database
    logs = await db_manager.get_analysis_logs(
        limit=limit,
        skip=skip,
        file_type=file_type,
        is_fake=is_fake
    )
    
    # Apply status filter if provided
    if status:
        logs = [log for log in logs if log.status == status]
    
    return {
        "total_logs": len(logs),
        "limit": limit,
        "skip": skip,
        "filters": {
            "file_type": file_type,
            "is_fake": is_fake,
            "status": status
        },
        "logs": [
            {
                "file_id": log.file_id,
                "file_name": log.file_name,
                "file_type": log.file_type,
                "file_size": log.file_size,
                "upload_time": log.upload_time.isoformat(),
                "analysis_time": log.analysis_time.isoformat(),
                "is_fake": log.is_fake,
                "confidence": log.confidence,
                "model_used": log.model_used,
                "processing_time": log.processing_time,
                "status": log.status,
                "error_message": log.error_message
            }
            for log in logs
        ]
    }


@router.get("/statistics")
async def get_log_statistics():
    """
    Get detailed statistics from analysis logs.
    """
    
    stats = await db_manager.get_statistics()
    
    return {
        "statistics": stats,
        "description": "Analysis statistics from all processed files"
    }


@router.get("/recent")
async def get_recent_logs(
    hours: int = Query(24, ge=1, le=168)  # Max 1 week
):
    """
    Get recent analysis logs from the last N hours.
    """
    
    # This would require a more sophisticated query in a real implementation
    # For now, we'll get recent logs and filter by time
    logs = await db_manager.get_analysis_logs(limit=100)
    
    # Filter by time (simplified - would use proper date filtering in real implementation)
    recent_logs = logs[:20]  # Just return recent logs
    
    return {
        "hours": hours,
        "total_logs": len(recent_logs),
        "logs": [
            {
                "file_id": log.file_id,
                "file_name": log.file_name,
                "file_type": log.file_type,
                "is_fake": log.is_fake,
                "confidence": log.confidence,
                "analysis_time": log.analysis_time.isoformat(),
                "processing_time": log.processing_time
            }
            for log in recent_logs
        ]
    }


@router.get("/errors")
async def get_error_logs(
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get logs of failed analyses.
    """
    
    logs = await db_manager.get_analysis_logs(limit=limit)
    error_logs = [log for log in logs if log.status == "failed"]
    
    return {
        "total_errors": len(error_logs),
        "errors": [
            {
                "file_id": log.file_id,
                "file_name": log.file_name,
                "file_type": log.file_type,
                "analysis_time": log.analysis_time.isoformat(),
                "error_message": log.error_message,
                "processing_time": log.processing_time
            }
            for log in error_logs
        ]
    }


@router.get("/performance")
async def get_performance_metrics():
    """
    Get performance metrics from analysis logs.
    """
    
    logs = await db_manager.get_analysis_logs(limit=1000)
    
    if not logs:
        return {
            "average_processing_time": 0,
            "processing_time_by_type": {},
            "processing_time_by_model": {},
            "total_analyses": 0
        }
    
    # Calculate average processing time
    processing_times = [log.processing_time for log in logs if log.processing_time > 0]
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    # Processing time by file type
    processing_time_by_type = {}
    for log in logs:
        if log.processing_time > 0:
            if log.file_type not in processing_time_by_type:
                processing_time_by_type[log.file_type] = []
            processing_time_by_type[log.file_type].append(log.processing_time)
    
    for file_type in processing_time_by_type:
        processing_time_by_type[file_type] = sum(processing_time_by_type[file_type]) / len(processing_time_by_type[file_type])
    
    # Processing time by model
    processing_time_by_model = {}
    for log in logs:
        if log.processing_time > 0:
            if log.model_used not in processing_time_by_model:
                processing_time_by_model[log.model_used] = []
            processing_time_by_model[log.model_used].append(log.processing_time)
    
    for model in processing_time_by_model:
        processing_time_by_model[model] = sum(processing_time_by_model[model]) / len(processing_time_by_model[model])
    
    return {
        "average_processing_time": round(avg_processing_time, 3),
        "processing_time_by_type": {k: round(v, 3) for k, v in processing_time_by_type.items()},
        "processing_time_by_model": {k: round(v, 3) for k, v in processing_time_by_model.items()},
        "total_analyses": len(logs)
    } 