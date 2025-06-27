"""
Upload router for handling file uploads.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from app.core.config import settings

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a single file for analysis."""
    try:
        # Validate file type
        file_extension = os.path.splitext(file.filename)[1].lower()
        allowed_extensions = (
            settings.ALLOWED_IMAGE_EXTENSIONS +
            settings.ALLOWED_VIDEO_EXTENSIONS +
            settings.ALLOWED_AUDIO_EXTENSIONS
        )
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not supported"
            )
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload multiple files for analysis."""
    uploaded_files = []
    
    for file in files:
        try:
            # Validate file type
            file_extension = os.path.splitext(file.filename)[1].lower()
            allowed_extensions = (
                settings.ALLOWED_IMAGE_EXTENSIONS +
                settings.ALLOWED_VIDEO_EXTENSIONS +
                settings.ALLOWED_AUDIO_EXTENSIONS
            )
            
            if file_extension not in allowed_extensions:
                continue  # Skip unsupported files
            
            # Save file
            file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            uploaded_files.append({
                "filename": file.filename,
                "file_path": file_path
            })
        except Exception as e:
            continue  # Skip files that fail to upload
    
    return {
        "message": f"Uploaded {len(uploaded_files)} files",
        "files": uploaded_files
    } 