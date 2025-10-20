"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Face Recognition Attendance System"
    
    # Database
    DATABASE_URL: str
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "face_recognition_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Face Recognition
    FACE_RECOGNITION_THRESHOLD: float = 0.6
    MIN_FACE_SIZE: int = 20
    EMBEDDING_SIZE: int = 512
    MAX_IMAGES_PER_EMPLOYEE: int = 50
    
    # FAISS
    USE_FAISS: bool = True
    FAISS_INDEX_PATH: str = "./data/faiss_index.bin"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://192.168.5.28:5173,https://wnm8dbn7-5173.inc1.devtunnels.ms"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create necessary directories
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path("./data").mkdir(parents=True, exist_ok=True)
Path("./logs").mkdir(parents=True, exist_ok=True)
