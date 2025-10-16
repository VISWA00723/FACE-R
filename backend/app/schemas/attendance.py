"""
Attendance schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


class AttendanceLogResponse(BaseModel):
    id: int
    employee_id: str
    employee_name: Optional[str] = None
    department: Optional[str] = None
    log_date: date
    in_time: Optional[datetime]
    out_time: Optional[datetime]
    duration: Optional[float]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AttendanceTodayResponse(BaseModel):
    date: date
    total_employees: int
    present: int
    absent: int
    in_count: int
    out_count: int
    attendance_logs: List[AttendanceLogResponse]


class AttendanceHistoryResponse(BaseModel):
    total: int
    attendance_logs: List[AttendanceLogResponse]
