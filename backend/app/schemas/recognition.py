"""
Face recognition schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FaceRecognitionRequest(BaseModel):
    image: str = Field(..., description="Base64 encoded image")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image": "base64_encoded_image_string"
            }
        }


class FaceRecognitionResponse(BaseModel):
    recognized: bool
    employee_id: Optional[str] = None
    name: Optional[str] = None
    department: Optional[str] = None
    confidence: Optional[float] = None
    status: str  # IN or OUT
    timestamp: datetime
    message: str
