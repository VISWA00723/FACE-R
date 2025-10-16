"""
FastAPI application setup
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.endpoints import employee, recognition, attendance
import logging

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

# Include routers
app.include_router(
    employee.router,
    prefix=f"{settings.API_V1_PREFIX}",
    tags=["Employee Management"]
)

app.include_router(
    recognition.router,
    prefix=f"{settings.API_V1_PREFIX}",
    tags=["Face Recognition"]
)

app.include_router(
    attendance.router,
    prefix=f"{settings.API_V1_PREFIX}",
    tags=["Attendance"]
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Face Recognition Attendance System API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
