"""
Analysis result endpoints.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
import structlog

from app.core.database import db_manager, AnalysisResult
from app.core.config import settings

logger = structlog.get_logger()
router = APIRouter()


@router.get("/{file_id}")
async def get_analysis_result(file_id: str):
    """
    Get analysis result for a specific file.
    """
    
    # Get analysis result from database
    result = await db_manager.get_analysis_result(file_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    
    # Get file upload record
    upload_record = await db_manager.get_file_upload(file_id)
    
    response = {
        "file_id": result.file_id,
        "file_name": result.file_name,
        "file_type": result.file_type,
        "file_size": result.file_size,
        "upload_time": result.upload_time.isoformat(),
        "analysis_time": result.analysis_time.isoformat(),
        "is_fake": result.is_fake,
        "confidence": result.confidence,
        "model_used": result.model_used,
        "processing_time": result.processing_time,
        "status": result.status,
        "metadata": result.metadata
    }
    
    if upload_record:
        response["upload_metadata"] = upload_record.metadata
    
    if result.error_message:
        response["error_message"] = result.error_message
    
    return response


@router.get("/{file_id}/status")
async def get_analysis_status(file_id: str):
    """
    Get current analysis status for a file.
    """
    
    # Get file upload record
    upload_record = await db_manager.get_file_upload(file_id)
    
    if not upload_record:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get analysis result if available
    result = await db_manager.get_analysis_result(file_id)
    
    response = {
        "file_id": file_id,
        "file_name": upload_record.file_name,
        "file_type": upload_record.file_type,
        "upload_time": upload_record.upload_time.isoformat(),
        "upload_status": upload_record.status
    }
    
    if result:
        response.update({
            "analysis_status": result.status,
            "is_fake": result.is_fake,
            "confidence": result.confidence,
            "analysis_time": result.analysis_time.isoformat(),
            "processing_time": result.processing_time
        })
        
        if result.error_message:
            response["error_message"] = result.error_message
    else:
        response["analysis_status"] = "pending"
    
    return response


@router.get("/batch/{batch_id}")
async def get_batch_analysis_results(batch_id: str):
    """
    Get analysis results for a batch of files.
    Note: This is a simplified implementation. In a real system,
    you'd track batch IDs in the database.
    """
    
    # For now, return a message indicating batch tracking would be implemented
    return {
        "batch_id": batch_id,
        "message": "Batch result tracking not implemented in this version",
        "note": "Individual file results can be retrieved using /analyze/{file_id}"
    }


@router.get("/recent/{file_type}")
async def get_recent_analyses(
    file_type: str,
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    """
    Get recent analysis results for a specific file type.
    """
    
    # Validate file type
    if file_type not in ["image", "video", "audio"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Get recent analyses
    results = await db_manager.get_analysis_logs(
        limit=limit,
        skip=skip,
        file_type=file_type
    )
    
    return {
        "file_type": file_type,
        "total_results": len(results),
        "results": [
            {
                "file_id": result.file_id,
                "file_name": result.file_name,
                "is_fake": result.is_fake,
                "confidence": result.confidence,
                "analysis_time": result.analysis_time.isoformat(),
                "processing_time": result.processing_time
            }
            for result in results
        ]
    }


@router.get("/statistics/summary")
async def get_analysis_statistics():
    """
    Get summary statistics of all analyses.
    """
    
    stats = await db_manager.get_statistics()
    
    return {
        "summary": stats,
        "confidence_thresholds": {
            "low": settings.CONFIDENCE_THRESHOLD,
            "high": settings.HIGH_CONFIDENCE_THRESHOLD
        }
    } 