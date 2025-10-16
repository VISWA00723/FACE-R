"""
Employee management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import numpy as np
import logging

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeList
from app.services.face_recognition_service import face_recognition_service
from app.services.faiss_service import faiss_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register_employee", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def register_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new employee with face images
    
    - **employee_id**: Unique employee identifier
    - **name**: Employee name
    - **department**: Department name
    - **images**: List of base64 encoded images (up to 50)
    """
    try:
        # Validate number of images
        if len(employee_data.images) > settings.MAX_IMAGES_PER_EMPLOYEE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Maximum {settings.MAX_IMAGES_PER_EMPLOYEE} images allowed"
            )
        
        if len(employee_data.images) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one image is required"
            )
        
        # Check if employee already exists
        existing_employee = db.query(Employee).filter(
            Employee.employee_id == employee_data.employee_id
        ).first()
        
        if existing_employee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with ID {employee_data.employee_id} already exists"
            )
        
        # Process images and extract embeddings
        logger.info(f"Processing {len(employee_data.images)} images for employee {employee_data.employee_id}")
        
        avg_embedding, successful_count = face_recognition_service.process_registration_images(
            employee_data.images
        )
        
        if avg_embedding is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to extract face embeddings from images. Please ensure faces are clearly visible."
            )
        
        # Create employee record
        new_employee = Employee(
            employee_id=employee_data.employee_id,
            name=employee_data.name,
            department=employee_data.department,
            embedding_vector=avg_embedding.tolist(),  # Convert numpy array to list for JSON storage
            image_count=successful_count
        )
        
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        
        # Add to FAISS index if enabled
        if settings.USE_FAISS and faiss_service:
            try:
                faiss_service.add_embedding(employee_data.employee_id, avg_embedding)
            except Exception as e:
                logger.error(f"Error adding to FAISS index: {str(e)}")
                # Don't fail the request if FAISS fails
        
        logger.info(f"Successfully registered employee {employee_data.employee_id}")
        
        return new_employee
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering employee: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register employee: {str(e)}"
        )


@router.get("/employees", response_model=EmployeeList)
async def get_all_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all registered employees
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        employees = db.query(Employee).offset(skip).limit(limit).all()
        total = db.query(Employee).count()
        
        return EmployeeList(
            total=total,
            employees=employees
        )
    except Exception as e:
        logger.error(f"Error fetching employees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch employees: {str(e)}"
        )


@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: str,
    db: Session = Depends(get_db)
):
    """
    Get employee details by ID
    
    - **employee_id**: Employee identifier
    """
    try:
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id
        ).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching employee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch employee: {str(e)}"
        )


@router.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an employee
    
    - **employee_id**: Employee identifier
    """
    try:
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id
        ).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        # Remove from FAISS index
        if settings.USE_FAISS and faiss_service:
            try:
                faiss_service.delete_embedding(employee_id)
            except Exception as e:
                logger.error(f"Error removing from FAISS index: {str(e)}")
        
        db.delete(employee)
        db.commit()
        
        logger.info(f"Successfully deleted employee {employee_id}")
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting employee: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete employee: {str(e)}"
        )
