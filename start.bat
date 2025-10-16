@echo off
echo ========================================
echo Face Recognition Attendance System
echo ========================================
echo.

:: Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

:: Check if backend venv exists
if not exist "backend\venv" (
    echo ERROR: Backend virtual environment not found!
    echo Please run: cd backend && python -m venv venv
    pause
    exit /b 1
)

:: Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo ERROR: Frontend dependencies not installed!
    echo Please run: cd frontend && npm install
    pause
    exit /b 1
)

echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && python main.py"

echo Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo Starting Frontend Development Server...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo System Started Successfully!
echo ========================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause >nul
