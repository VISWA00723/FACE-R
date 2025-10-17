"""
Attendance log database model
"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"), nullable=False, index=True)
    log_date = Column(Date, nullable=False, index=True)
    in_time = Column(DateTime, nullable=True)
    out_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # Duration in hours
    status = Column(String, default="IN")  # IN, OUT, ABSENT
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    employee = relationship("Employee", back_populates="attendance_logs")
    
    def __repr__(self):
        return f"<AttendanceLog(employee_id={self.employee_id}, date={self.log_date}, status={self.status})>"
