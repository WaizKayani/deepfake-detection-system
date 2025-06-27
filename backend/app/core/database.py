"""
Database configuration and models for MongoDB.
"""

import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel, Field
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Database client
client: Optional[AsyncIOMotorClient] = None
database: Optional[AsyncIOMotorDatabase] = None


class AnalysisResult(BaseModel):
    """Analysis result model."""
    file_id: str
    file_name: str
    file_type: str  # image, video, audio
    file_size: int
    upload_time: datetime
    analysis_time: datetime
    is_fake: bool
    confidence: float
    model_used: str
    processing_time: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: str = "completed"  # pending, processing, completed, failed
    error_message: Optional[str] = None


class FileUpload(BaseModel):
    """File upload model."""
    file_id: str
    file_name: str
    file_type: str
    file_size: int
    upload_time: datetime
    file_path: str
    status: str = "uploaded"  # uploaded, processing, completed, failed
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


async def init_db():
    """Initialize database connection."""
    global client, database
    
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        database = client[settings.DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        logger.info("Database connection established")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error("Failed to connect to database", error=str(e))
        raise


async def close_db():
    """Close database connection."""
    global client
    
    if client:
        client.close()
        logger.info("Database connection closed")


async def create_indexes():
    """Create database indexes for better performance."""
    try:
        # Analysis results indexes
        await database.analysis_results.create_index("file_id", unique=True)
        await database.analysis_results.create_index("upload_time")
        await database.analysis_results.create_index("file_type")
        await database.analysis_results.create_index("is_fake")
        
        # File uploads indexes
        await database.file_uploads.create_index("file_id", unique=True)
        await database.file_uploads.create_index("upload_time")
        await database.file_uploads.create_index("file_type")
        await database.file_uploads.create_index("status")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error("Failed to create indexes", error=str(e))


async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    if not database:
        await init_db()
    return database


class DatabaseManager:
    """Database operations manager."""
    
    def __init__(self):
        self.db = None
    
    async def get_db(self):
        """Get database instance."""
        if self.db is None:
            self.db = await get_database()
        return self.db
    
    async def save_analysis_result(self, result: AnalysisResult) -> bool:
        """Save analysis result to database."""
        try:
            db = await self.get_db()
            await db.analysis_results.insert_one(result.dict())
            logger.info("Analysis result saved", file_id=result.file_id)
            return True
        except Exception as e:
            logger.error("Failed to save analysis result", error=str(e))
            return False
    
    async def save_file_upload(self, upload: FileUpload) -> bool:
        """Save file upload record to database."""
        try:
            db = await self.get_db()
            await db.file_uploads.insert_one(upload.dict())
            logger.info("File upload saved", file_id=upload.file_id)
            return True
        except Exception as e:
            logger.error("Failed to save file upload", error=str(e))
            return False
    
    async def get_analysis_result(self, file_id: str) -> Optional[AnalysisResult]:
        """Get analysis result by file ID."""
        try:
            db = await self.get_db()
            result = await db.analysis_results.find_one({"file_id": file_id})
            if result:
                return AnalysisResult(**result)
            return None
        except Exception as e:
            logger.error("Failed to get analysis result", error=str(e))
            return None
    
    async def get_file_upload(self, file_id: str) -> Optional[FileUpload]:
        """Get file upload record by file ID."""
        try:
            db = await self.get_db()
            result = await db.file_uploads.find_one({"file_id": file_id})
            if result:
                return FileUpload(**result)
            return None
        except Exception as e:
            logger.error("Failed to get file upload", error=str(e))
            return None
    
    async def get_analysis_logs(
        self, 
        limit: int = 100, 
        skip: int = 0,
        file_type: Optional[str] = None,
        is_fake: Optional[bool] = None
    ) -> List[AnalysisResult]:
        """Get analysis logs with optional filtering."""
        try:
            db = await self.get_db()
            
            # Build filter
            filter_query = {}
            if file_type:
                filter_query["file_type"] = file_type
            if is_fake is not None:
                filter_query["is_fake"] = is_fake
            
            cursor = db.analysis_results.find(filter_query).sort(
                "analysis_time", -1
            ).skip(skip).limit(limit)
            
            results = []
            async for doc in cursor:
                results.append(AnalysisResult(**doc))
            
            return results
            
        except Exception as e:
            logger.error("Failed to get analysis logs", error=str(e))
            return []
    
    async def update_analysis_status(
        self, 
        file_id: str, 
        status: str, 
        error_message: Optional[str] = None
    ) -> bool:
        """Update analysis status."""
        try:
            db = await self.get_db()
            update_data = {"status": status}
            if error_message:
                update_data["error_message"] = error_message
            
            await db.analysis_results.update_one(
                {"file_id": file_id},
                {"$set": update_data}
            )
            logger.info("Analysis status updated", file_id=file_id, status=status)
            return True
        except Exception as e:
            logger.error("Failed to update analysis status", error=str(e))
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics."""
        try:
            db = await self.get_db()
            
            # Total files analyzed
            total_files = await db.analysis_results.count_documents({})
            
            # Files by type
            image_count = await db.analysis_results.count_documents({"file_type": "image"})
            video_count = await db.analysis_results.count_documents({"file_type": "video"})
            audio_count = await db.analysis_results.count_documents({"file_type": "audio"})
            
            # Predictions
            real_count = await db.analysis_results.count_documents({"is_fake": False})
            fake_count = await db.analysis_results.count_documents({"is_fake": True})
            
            # Average confidence
            pipeline = [
                {"$group": {"_id": None, "avg_confidence": {"$avg": "$confidence"}}}
            ]
            avg_confidence_result = await db.analysis_results.aggregate(pipeline).to_list(1)
            avg_confidence = avg_confidence_result[0]["avg_confidence"] if avg_confidence_result else 0
            
            return {
                "total_files": total_files,
                "by_type": {
                    "image": image_count,
                    "video": video_count,
                    "audio": audio_count
                },
                "by_prediction": {
                    "real": real_count,
                    "fake": fake_count
                },
                "average_confidence": round(avg_confidence, 3)
            }
            
        except Exception as e:
            logger.error("Failed to get statistics", error=str(e))
            return {}


# Global database manager instance
db_manager = DatabaseManager() 