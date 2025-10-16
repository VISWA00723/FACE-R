"""
Attendance Service for logging and managing attendance
"""
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from typing import List, Optional
from app.models.attendance import AttendanceLog
from app.models.employee import Employee
import logging

logger = logging.getLogger(__name__)


class AttendanceService:
    """
    Service for managing attendance logs
    """
    
    @staticmethod
    def log_attendance(
        db: Session,
        employee_id: str,
        status: str = "IN"
    ) -> AttendanceLog:
        """
        Log attendance for an employee
        
        Args:
            db: Database session
            employee_id: Employee ID
            status: Status (IN or OUT)
            
        Returns:
            AttendanceLog object
        """
        try:
            today = date.today()
            now = datetime.now()
            
            # Check if there's an existing log for today
            existing_log = db.query(AttendanceLog).filter(
                AttendanceLog.employee_id == employee_id,
                AttendanceLog.log_date == today
            ).first()
            
            if existing_log:
                # Update existing log
                if status == "OUT" and existing_log.in_time:
                    existing_log.out_time = now
                    existing_log.status = "OUT"
                    
                    # Calculate duration in hours
                    duration = (now - existing_log.in_time).total_seconds() / 3600
                    existing_log.duration = round(duration, 2)
                    
                    logger.info(f"Updated OUT time for employee {employee_id}")
                elif status == "IN" and existing_log.out_time:
                    # Employee came back, update to IN
                    existing_log.status = "IN"
                    logger.info(f"Updated status to IN for employee {employee_id}")
                
                db.commit()
                db.refresh(existing_log)
                return existing_log
            else:
                # Create new log
                new_log = AttendanceLog(
                    employee_id=employee_id,
                    log_date=today,
                    in_time=now if status == "IN" else None,
                    out_time=now if status == "OUT" else None,
                    status=status
                )
                
                db.add(new_log)
                db.commit()
                db.refresh(new_log)
                
                logger.info(f"Created new attendance log for employee {employee_id} with status {status}")
                return new_log
        except Exception as e:
            logger.error(f"Error logging attendance: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    def get_last_status(db: Session, employee_id: str) -> str:
        """
        Get the last status of an employee for today
        
        Args:
            db: Database session
            employee_id: Employee ID
            
        Returns:
            Status string (IN, OUT, or None)
        """
        today = date.today()
        
        log = db.query(AttendanceLog).filter(
            AttendanceLog.employee_id == employee_id,
            AttendanceLog.log_date == today
        ).first()
        
        return log.status if log else None
    
    @staticmethod
    def get_today_attendance(db: Session) -> List[AttendanceLog]:
        """
        Get all attendance logs for today
        
        Args:
            db: Database session
            
        Returns:
            List of AttendanceLog objects
        """
        today = date.today()
        
        logs = db.query(AttendanceLog).filter(
            AttendanceLog.log_date == today
        ).all()
        
        return logs
    
    @staticmethod
    def get_attendance_history(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        employee_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AttendanceLog]:
        """
        Get attendance history with filters
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            employee_id: Filter by employee ID
            limit: Maximum number of records
            offset: Offset for pagination
            
        Returns:
            List of AttendanceLog objects
        """
        query = db.query(AttendanceLog)
        
        if employee_id:
            query = query.filter(AttendanceLog.employee_id == employee_id)
        
        if start_date:
            query = query.filter(AttendanceLog.log_date >= start_date)
        
        if end_date:
            query = query.filter(AttendanceLog.log_date <= end_date)
        
        logs = query.order_by(AttendanceLog.log_date.desc(), AttendanceLog.created_at.desc())\
                   .limit(limit)\
                   .offset(offset)\
                   .all()
        
        return logs
    
    @staticmethod
    def get_attendance_count(
        db: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        employee_id: Optional[str] = None
    ) -> int:
        """
        Get count of attendance logs
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            employee_id: Filter by employee ID
            
        Returns:
            Count of logs
        """
        query = db.query(AttendanceLog)
        
        if employee_id:
            query = query.filter(AttendanceLog.employee_id == employee_id)
        
        if start_date:
            query = query.filter(AttendanceLog.log_date >= start_date)
        
        if end_date:
            query = query.filter(AttendanceLog.log_date <= end_date)
        
        return query.count()


attendance_service = AttendanceService()
