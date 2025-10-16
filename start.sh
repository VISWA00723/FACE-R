#!/bin/bash

echo "========================================"
echo "Face Recognition Attendance System"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "ERROR: Backend virtual environment not found!"
    echo "Please run: cd backend && python -m venv venv"
    exit 1
fi

# Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "ERROR: Frontend dependencies not installed!"
    echo "Please run: cd frontend && npm install"
    exit 1
fi

echo "Starting Backend Server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to initialize..."
sleep 8

echo "Starting Frontend Development Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "System Started Successfully!"
echo "========================================"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:5173"
echo ""
echo "Process IDs:"
echo "  Backend: $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

trap cleanup INT TERM

# Wait for processes
wait
