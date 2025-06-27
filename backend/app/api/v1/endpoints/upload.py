"""
File upload endpoints.
"""

import os
import uuid
import aiofiles
from datetime import datetime
from typing import List
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.core.database import db_manager, FileUpload
from app.core.monitoring import ModelMetrics
from app.ml.models import ModelManager

logger = structlog.get_logger()
router = APIRouter()


def get_file_type(filename: str) -> str:
    """Determine file type based on extension."""
    ext = Path(filename).suffix.lower()
    
    if ext in settings.ALLOWED_IMAGE_EXTENSIONS:
        return "image"
    elif ext in settings.ALLOWED_VIDEO_EXTENSIONS:
        return "video"
    elif ext in settings.ALLOWED_AUDIO_EXTENSIONS:
        return "audio"
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")


def get_upload_path(file_type: str, filename: str) -> str:
    """Get upload path for file."""
    return os.path.join(settings.UPLOAD_DIR, file_type, filename)


async def save_uploaded_file(file: UploadFile, file_path: str) -> bool:
    """Save uploaded file to disk."""
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        return True
    except Exception as e:
        logger.error("Failed to save uploaded file", error=str(e), file_path=file_path)
        return False


async def process_file_background(file_id: str, file_path: str, file_type: str):
    """Background task to process uploaded file."""
    try:
        logger.info("Starting background processing", file_id=file_id, file_type=file_type)
        
        # Update status to processing
        await db_manager.update_analysis_status(file_id, "processing")
        
        # Get model manager
        model_manager = ModelManager()
        
        # Get file information
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        upload_time = datetime.utcnow()
        
        # Process file based on type
        if file_type == "image":
            result = await model_manager.analyze_image(
                file_path, 
                file_id=file_id, 
                file_name=file_name, 
                file_size=file_size, 
                upload_time=upload_time
            )
        elif file_type == "video":
            result = await model_manager.analyze_video(
                file_path, 
                file_id=file_id, 
                file_name=file_name, 
                file_size=file_size, 
                upload_time=upload_time
            )
        elif file_type == "audio":
            result = await model_manager.analyze_audio(
                file_path, 
                file_id=file_id, 
                file_name=file_name, 
                file_size=file_size, 
                upload_time=upload_time
            )
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Save result to database
        await db_manager.save_analysis_result(result)
        
        logger.info("Background processing completed", file_id=file_id)
        
    except Exception as e:
        logger.error("Background processing failed", file_id=file_id, error=str(e))
        await db_manager.update_analysis_status(file_id, "failed", str(e))


@router.post("/")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a media file for deepfake detection analysis.
    
    Supports:
    - Images: JPG, JPEG, PNG, BMP, TIFF
    - Videos: MP4, AVI, MOV, MKV, WEBM
    - Audio: WAV, MP3, FLAC, M4A, AAC
    """
    
    # Validate file size
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE} bytes"
        )
    
    # Determine file type
    try:
        file_type = get_file_type(file.filename)
    except HTTPException:
        raise
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Create filename with ID
    file_extension = Path(file.filename).suffix
    safe_filename = f"{file_id}{file_extension}"
    
    # Get upload path
    file_path = get_upload_path(file_type, safe_filename)
    
    # Save file
    if not await save_uploaded_file(file, file_path):
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Create file upload record
    upload_record = FileUpload(
        file_id=file_id,
        file_name=file.filename,
        file_type=file_type,
        file_size=file_size,
        upload_time=datetime.utcnow(),
        file_path=file_path,
        status="uploaded"
    )
    
    # Save to database
    if not await db_manager.save_file_upload(upload_record):
        raise HTTPException(status_code=500, detail="Failed to save upload record")
    
    # Record metrics
    ModelMetrics.record_file_upload(file_type, "success")
    ModelMetrics.record_file_size(file_type, file_size)
    
    # Start background processing
    background_tasks.add_task(
        process_file_background, 
        file_id, 
        file_path, 
        file_type
    )
    
    logger.info(
        "File uploaded successfully",
        file_id=file_id,
        file_name=file.filename,
        file_type=file_type,
        file_size=file_size
    )
    
    return {
        "file_id": file_id,
        "file_name": file.filename,
        "file_type": file_type,
        "file_size": file_size,
        "status": "uploaded",
        "message": "File uploaded successfully. Analysis in progress."
    }


@router.post("/batch")
async def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    """
    Upload multiple media files for batch processing.
    """
    
    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files per batch")
    
    results = []
    
    for file in files:
        try:
            # Validate file size
            if file.size and file.size > settings.MAX_FILE_SIZE:
                results.append({
                    "file_name": file.filename,
                    "status": "error",
                    "error": f"File size exceeds maximum limit"
                })
                continue
            
            # Determine file type
            try:
                file_type = get_file_type(file.filename)
            except HTTPException:
                results.append({
                    "file_name": file.filename,
                    "status": "error",
                    "error": f"Unsupported file type"
                })
                continue
            
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            
            # Create filename with ID
            file_extension = Path(file.filename).suffix
            safe_filename = f"{file_id}{file_extension}"
            
            # Get upload path
            file_path = get_upload_path(file_type, safe_filename)
            
            # Save file
            if not await save_uploaded_file(file, file_path):
                results.append({
                    "file_name": file.filename,
                    "status": "error",
                    "error": "Failed to save file"
                })
                continue
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Create file upload record
            upload_record = FileUpload(
                file_id=file_id,
                file_name=file.filename,
                file_type=file_type,
                file_size=file_size,
                upload_time=datetime.utcnow(),
                file_path=file_path,
                status="uploaded"
            )
            
            # Save to database
            if not await db_manager.save_file_upload(upload_record):
                results.append({
                    "file_name": file.filename,
                    "status": "error",
                    "error": "Failed to save upload record"
                })
                continue
            
            # Record metrics
            ModelMetrics.record_file_upload(file_type, "success")
            ModelMetrics.record_file_size(file_type, file_size)
            
            # Start background processing
            background_tasks.add_task(
                process_file_background, 
                file_id, 
                file_path, 
                file_type
            )
            
            results.append({
                "file_id": file_id,
                "file_name": file.filename,
                "file_type": file_type,
                "file_size": file_size,
                "status": "uploaded"
            })
            
        except Exception as e:
            logger.error("Error processing file in batch", file_name=file.filename, error=str(e))
            results.append({
                "file_name": file.filename,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "batch_id": str(uuid.uuid4()),
        "total_files": len(files),
        "results": results
    } 