"""
Configuration settings for the Media Authentication System.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "deepfake_detection"
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    ALLOWED_VIDEO_EXTENSIONS: List[str] = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
    ALLOWED_AUDIO_EXTENSIONS: List[str] = [".wav", ".mp3", ".flac", ".m4a", ".aac"]
    
    # Model Configuration
    IMAGE_MODEL_PATH: str = "./ml_models/image_model.pth"
    VIDEO_MODEL_PATH: str = "./ml_models/video_model.pth"
    AUDIO_MODEL_PATH: str = "./ml_models/audio_model.pth"
    
    # Model Settings
    IMAGE_INPUT_SIZE: int = 224
    VIDEO_FRAME_RATE: int = 1  # Extract 1 frame per second
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_MAX_DURATION: int = 30  # seconds
    
    # Confidence Thresholds
    CONFIDENCE_THRESHOLD: float = 0.7
    HIGH_CONFIDENCE_THRESHOLD: float = 0.9
    
    # Monitoring Configuration
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3000
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "videos"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "temp"), exist_ok=True) 