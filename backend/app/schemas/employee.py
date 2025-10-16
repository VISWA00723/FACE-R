"""
Employee schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class EmployeeCreate(BaseModel):
    employee_id: str = Field(..., description="Unique employee ID")
    name: str = Field(..., description="Employee name")
    department: str = Field(..., description="Department name")
    images: List[str] = Field(..., description="List of base64 encoded images (max 50)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": "EMP001",
                "name": "John Doe",
                "department": "Engineering",
                "images": ["base64_image_1", "base64_image_2"]
            }
        }


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    name: str
    department: str
    image_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EmployeeList(BaseModel):
    total: int
    employees: List[EmployeeResponse]
