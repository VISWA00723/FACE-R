"""
Attendance management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import Optional
import csv
import io
import logging

from app.core.database import get_db
from app.models.attendance import AttendanceLog
from app.models.employee import Employee
from app.schemas.attendance import (
    AttendanceLogResponse,
    AttendanceTodayResponse,
    AttendanceHistoryResponse
)
from app.services.attendance_service import attendance_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/attendance_today", response_model=AttendanceTodayResponse)
async def get_today_attendance(
    db: Session = Depends(get_db)
):
    """
    Get today's attendance summary and logs
    
    Returns:
    - Total employees registered
    - Present count (employees with attendance)
    - Absent count
    - IN count (currently in office)
    - OUT count (left office)
    - List of all attendance logs for today
    """
    try:
        today = date.today()
        
        # Get today's attendance logs
        logs = attendance_service.get_today_attendance(db)
        
        # Get total employees
        total_employees = db.query(Employee).count()
        
        # Count present, in, and out
        present_count = len(logs)
        in_count = sum(1 for log in logs if log.status == "IN")
        out_count = sum(1 for log in logs if log.status == "OUT")
        absent_count = total_employees - present_count
        
        # Enrich logs with employee details
        enriched_logs = []
        for log in logs:
            employee = db.query(Employee).filter(
                Employee.employee_id == log.employee_id
            ).first()
            
            log_response = AttendanceLogResponse(
                id=log.id,
                employee_id=log.employee_id,
                employee_name=employee.name if employee else "Unknown",
                department=employee.department if employee else "Unknown",
                log_date=log.log_date,
                in_time=log.in_time,
                out_time=log.out_time,
                duration=log.duration,
                status=log.status,
                created_at=log.created_at
            )
            enriched_logs.append(log_response)
        
        return AttendanceTodayResponse(
            date=today,
            total_employees=total_employees,
            present=present_count,
            absent=absent_count,
            in_count=in_count,
            out_count=out_count,
            attendance_logs=enriched_logs
        )
    
    except Exception as e:
        logger.error(f"Error fetching today's attendance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch today's attendance: {str(e)}"
        )


@router.get("/attendance_history", response_model=AttendanceHistoryResponse)
async def get_attendance_history(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    Get attendance history with optional filters
    
    - **start_date**: Filter by start date
    - **end_date**: Filter by end date
    - **employee_id**: Filter by specific employee
    - **limit**: Maximum number of records (default: 100, max: 1000)
    - **offset**: Offset for pagination (default: 0)
    """
    try:
        # Get attendance logs
        logs = attendance_service.get_attendance_history(
            db=db,
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id,
            limit=limit,
            offset=offset
        )
        
        # Get total count
        total = attendance_service.get_attendance_count(
            db=db,
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id
        )
        
        # Enrich logs with employee details
        enriched_logs = []
        for log in logs:
            employee = db.query(Employee).filter(
                Employee.employee_id == log.employee_id
            ).first()
            
            log_response = AttendanceLogResponse(
                id=log.id,
                employee_id=log.employee_id,
                employee_name=employee.name if employee else "Unknown",
                department=employee.department if employee else "Unknown",
                log_date=log.log_date,
                in_time=log.in_time,
                out_time=log.out_time,
                duration=log.duration,
                status=log.status,
                created_at=log.created_at
            )
            enriched_logs.append(log_response)
        
        return AttendanceHistoryResponse(
            total=total,
            attendance_logs=enriched_logs
        )
    
    except Exception as e:
        logger.error(f"Error fetching attendance history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch attendance history: {str(e)}"
        )


@router.get("/attendance_export")
async def export_attendance(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    db: Session = Depends(get_db)
):
    """
    Export attendance data as CSV
    
    - **start_date**: Filter by start date
    - **end_date**: Filter by end date
    - **employee_id**: Filter by specific employee
    
    Returns CSV file for download
    """
    try:
        # Get attendance logs (no limit for export)
        logs = attendance_service.get_attendance_history(
            db=db,
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id,
            limit=10000,  # Large limit for export
            offset=0
        )
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Employee ID",
            "Name",
            "Department",
            "Date",
            "In Time",
            "Out Time",
            "Duration (hours)",
            "Status"
        ])
        
        # Write data
        for log in logs:
            employee = db.query(Employee).filter(
                Employee.employee_id == log.employee_id
            ).first()
            
            writer.writerow([
                log.employee_id,
                employee.name if employee else "Unknown",
                employee.department if employee else "Unknown",
                log.log_date.strftime("%Y-%m-%d"),
                log.in_time.strftime("%Y-%m-%d %H:%M:%S") if log.in_time else "",
                log.out_time.strftime("%Y-%m-%d %H:%M:%S") if log.out_time else "",
                f"{log.duration:.2f}" if log.duration else "",
                log.status
            ])
        
        # Prepare response
        output.seek(0)
        
        # Generate filename
        filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    
    except Exception as e:
        logger.error(f"Error exporting attendance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export attendance: {str(e)}"
        )


@router.get("/attendance_stats")
async def get_attendance_stats(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Get attendance statistics for a date range
    
    - **start_date**: Start date for statistics
    - **end_date**: End date for statistics
    
    Returns daily attendance counts and averages
    """
    try:
        # Default to last 7 days if not specified
        if not end_date:
            end_date = date.today()
        if not start_date:
            start_date = end_date - timedelta(days=7)
        
        # Get logs for date range
        logs = attendance_service.get_attendance_history(
            db=db,
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )
        
        # Group by date
        daily_stats = {}
        for log in logs:
            log_date_str = log.log_date.strftime("%Y-%m-%d")
            if log_date_str not in daily_stats:
                daily_stats[log_date_str] = {
                    "date": log_date_str,
                    "present": 0,
                    "in": 0,
                    "out": 0
                }
            
            daily_stats[log_date_str]["present"] += 1
            if log.status == "IN":
                daily_stats[log_date_str]["in"] += 1
            elif log.status == "OUT":
                daily_stats[log_date_str]["out"] += 1
        
        # Convert to list and sort by date
        stats_list = sorted(daily_stats.values(), key=lambda x: x["date"])
        
        # Calculate averages
        total_employees = db.query(Employee).count()
        total_present = sum(day["present"] for day in stats_list)
        num_days = len(stats_list) if stats_list else 1
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_employees": total_employees,
            "average_present": round(total_present / num_days, 2),
            "daily_stats": stats_list
        }
    
    except Exception as e:
        logger.error(f"Error fetching attendance stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch attendance stats: {str(e)}"
        )
