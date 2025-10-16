"""
Database initialization script
Creates database tables and initial setup
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print("Warning: .env file not found. Using environment variables or defaults.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database():
    """Create the database if it doesn't exist"""
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "face_recognition_db")
    
    # Connect to PostgreSQL default database
    default_db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
    
    try:
        logger.info("Connecting to PostgreSQL...")
        engine = create_engine(default_db_url, isolation_level="AUTOCOMMIT")
        
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            )
            exists = result.fetchone()
            
            if exists:
                logger.info(f"Database '{db_name}' already exists")
            else:
                logger.info(f"Creating database '{db_name}'...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                logger.info(f"Database '{db_name}' created successfully")
        
        engine.dispose()
        
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise


def init_tables():
    """Initialize database tables"""
    from app.core.database import engine, Base
    from app.models import Employee, AttendanceLog
    
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Create indexes for better performance
        with engine.connect() as conn:
            logger.info("Creating indexes...")
            
            # Index on employee_id in attendance_logs
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_attendance_employee_id 
                ON attendance_logs(employee_id)
            """))
            
            # Index on log_date in attendance_logs
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_attendance_log_date 
                ON attendance_logs(log_date)
            """))
            
            # Composite index for common queries
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_attendance_employee_date 
                ON attendance_logs(employee_id, log_date)
            """))
            
            conn.commit()
            logger.info("Indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error initializing tables: {str(e)}")
        raise


def verify_setup():
    """Verify database setup"""
    from app.core.database import engine
    
    try:
        with engine.connect() as conn:
            # Check employees table
            result = conn.execute(text("SELECT COUNT(*) FROM employees"))
            emp_count = result.fetchone()[0]
            logger.info(f"Employees table: {emp_count} records")
            
            # Check attendance_logs table
            result = conn.execute(text("SELECT COUNT(*) FROM attendance_logs"))
            att_count = result.fetchone()[0]
            logger.info(f"Attendance_logs table: {att_count} records")
            
        logger.info("Database verification completed successfully")
        
    except Exception as e:
        logger.error(f"Error verifying setup: {str(e)}")
        raise


def main():
    """Main initialization function"""
    try:
        logger.info("=" * 60)
        logger.info("Face Recognition Attendance System - Database Initialization")
        logger.info("=" * 60)
        
        # Step 1: Create database
        logger.info("\n[Step 1/3] Creating database...")
        create_database()
        
        # Step 2: Create tables
        logger.info("\n[Step 2/3] Creating tables...")
        init_tables()
        
        # Step 3: Verify setup
        logger.info("\n[Step 3/3] Verifying setup...")
        verify_setup()
        
        logger.info("\n" + "=" * 60)
        logger.info("Database initialization completed successfully!")
        logger.info("=" * 60)
        logger.info("\nYou can now start the backend server with:")
        logger.info("  cd backend")
        logger.info("  python main.py")
        
    except Exception as e:
        logger.error(f"\nDatabase initialization failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
