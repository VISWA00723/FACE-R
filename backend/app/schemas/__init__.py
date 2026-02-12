"""
Pydantic schemas for API validation
"""
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeList
from app.schemas.attendance import AttendanceLogResponse, AttendanceTodayResponse, AttendanceHistoryResponse
from app.schemas.recognition import FaceRecognitionRequest, FaceRecognitionResponse
from app.schemas.auth import LoginRequest, TokenResponse, UserInfo

__all__ = [
    "EmployeeCreate",
    "EmployeeResponse",
    "EmployeeList",
    "AttendanceLogResponse",
    "AttendanceTodayResponse",
    "AttendanceHistoryResponse",
    "FaceRecognitionRequest",
    "FaceRecognitionResponse",
    "LoginRequest",
    "TokenResponse",
    "UserInfo",
]
