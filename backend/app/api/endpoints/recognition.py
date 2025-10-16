"""
Face recognition endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import numpy as np
import logging

from app.core.database import get_db
from app.models.employee import Employee
from app.schemas.recognition import FaceRecognitionRequest, FaceRecognitionResponse
from app.services.face_recognition_service import face_recognition_service
from app.services.faiss_service import faiss_service
from app.services.attendance_service import attendance_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/recognize_face", response_model=FaceRecognitionResponse)
async def recognize_face(
    request: FaceRecognitionRequest,
    db: Session = Depends(get_db)
):
    """
    Recognize face from image and log attendance
    
    - **image**: Base64 encoded image
    
    Returns recognized employee information and logs attendance (IN/OUT)
    """
    try:
        # Get all stored embeddings from database
        employees = db.query(Employee).all()
        
        if not employees:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No employees registered in the system"
            )
        
        # Prepare embeddings for comparison
        stored_embeddings = []
        for emp in employees:
            embedding = np.array(emp.embedding_vector, dtype=np.float32)
            stored_embeddings.append((emp.employee_id, embedding))
        
        # Try FAISS search if enabled
        employee_id = None
        confidence = None
        
        if settings.USE_FAISS and faiss_service and faiss_service.index.ntotal > 0:
            try:
                # Extract embedding from query image
                image = face_recognition_service.base64_to_image(request.image)
                query_embedding = face_recognition_service.extract_face_embedding(image)
                
                if query_embedding is not None:
                    # Search using FAISS
                    results = faiss_service.search(query_embedding, k=1)
                    
                    if results:
                        best_employee_id, distance = results[0]
                        
                        # Check if distance is below threshold
                        if distance < settings.FACE_RECOGNITION_THRESHOLD:
                            employee_id = best_employee_id
                            confidence = 1.0 - distance
                            logger.info(f"FAISS recognition: {employee_id} (distance: {distance:.4f})")
            except Exception as e:
                logger.error(f"FAISS search failed, falling back to direct comparison: {str(e)}")
        
        # Fallback to direct comparison if FAISS didn't work
        if employee_id is None:
            employee_id, confidence = face_recognition_service.recognize_face(
                request.image,
                stored_embeddings
            )
        
        # Check if face was recognized
        if employee_id is None:
            return FaceRecognitionResponse(
                recognized=False,
                employee_id=None,
                name=None,
                department=None,
                confidence=None,
                status="UNKNOWN",
                timestamp=datetime.now(),
                message="Face not recognized. Please ensure your face is clearly visible or register first."
            )
        
        # Get employee details
        employee = db.query(Employee).filter(
            Employee.employee_id == employee_id
        ).first()
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee data not found"
            )
        
        # Determine attendance status (IN or OUT)
        last_status = attendance_service.get_last_status(db, employee_id)
        
        # Toggle status: if last was IN, mark as OUT; if OUT or None, mark as IN
        new_status = "OUT" if last_status == "IN" else "IN"
        
        # Log attendance
        attendance_log = attendance_service.log_attendance(
            db=db,
            employee_id=employee_id,
            status=new_status
        )
        
        logger.info(f"Face recognized: {employee_id} - {employee.name}, Status: {new_status}")
        
        return FaceRecognitionResponse(
            recognized=True,
            employee_id=employee.employee_id,
            name=employee.name,
            department=employee.department,
            confidence=confidence,
            status=new_status,
            timestamp=datetime.now(),
            message=f"Welcome {employee.name}! Attendance marked as {new_status}."
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recognizing face: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to recognize face: {str(e)}"
        )


@router.post("/detect_face")
async def detect_face(
    request: FaceRecognitionRequest
):
    """
    Detect face in image without recognition (for testing)
    
    - **image**: Base64 encoded image
    
    Returns whether a face was detected
    """
    try:
        # Convert base64 to image
        image = face_recognition_service.base64_to_image(request.image)
        
        # Detect faces
        faces = face_recognition_service.detect_faces_mtcnn(image)
        
        if len(faces) == 0:
            return {
                "face_detected": False,
                "message": "No face detected in image"
            }
        
        return {
            "face_detected": True,
            "num_faces": len(faces),
            "message": f"Detected {len(faces)} face(s) in image"
        }
    
    except Exception as e:
        logger.error(f"Error detecting face: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect face: {str(e)}"
        )
