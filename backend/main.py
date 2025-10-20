"""
Main FastAPI application entry point
"""
import os
import uvicorn
from app.core.config import settings

# Print database URL for debugging (remove in production)
print(f"Database URL: {settings.DATABASE_URL}")

if __name__ == "__main__":
    uvicorn.run(
        "app.api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
