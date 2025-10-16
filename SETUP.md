# Setup Guide - Face Recognition Attendance System

This guide will walk you through setting up the Face Recognition Attendance System from scratch.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 14 or higher** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git** - [Download Git](https://git-scm.com/downloads)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd FACE-R
```

### 2. Environment Configuration

#### Backend Environment

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and update the following values:

```env
# Database credentials (update with your PostgreSQL credentials)
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=face_recognition_db

# Security (IMPORTANT: Change this in production!)
SECRET_KEY=your-super-secret-key-here-change-this

# CORS (add your frontend URL if different)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### Frontend Environment

```bash
cd frontend
copy .env.example .env
```

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Database Setup

#### Create PostgreSQL Database

**Option A: Using PostgreSQL command line**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE face_recognition_db;

# Exit
\q
```

**Option B: Using pgAdmin**

1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name it `face_recognition_db`
5. Click "Save"

#### Initialize Database Tables

```bash
cd database
python init_db.py
```

You should see output indicating successful table creation.

### 4. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: The first time you run the backend, InsightFace will download the ArcFace model (~600MB). This is a one-time download.

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 6. Running the Application

#### Start Backend Server

Open a terminal in the `backend` directory:

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Start server
python main.py
```

The backend API will start at `http://localhost:8000`

You can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Start Frontend Development Server

Open a **new terminal** in the `frontend` directory:

```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

### 7. Access the Application

Open your browser and navigate to:

```
http://localhost:5173
```

## Troubleshooting

### Database Connection Error

**Error**: `could not connect to server: Connection refused`

**Solution**:
1. Ensure PostgreSQL is running
2. Check your database credentials in `.env`
3. Verify the database exists: `psql -U postgres -l`

### Port Already in Use

**Backend Error**: `Address already in use: 8000`

**Solution**:
1. Change `API_PORT` in `.env` to a different port (e.g., 8001)
2. Update `VITE_API_URL` in `frontend/.env` accordingly

**Frontend Error**: `Port 5173 is in use`

**Solution**: The Vite dev server will automatically try the next available port.

### InsightFace Model Download Issues

**Error**: `Failed to download model`

**Solution**:
1. Ensure you have a stable internet connection
2. The model will be downloaded to `~/.insightface/models/`
3. Manual download: Visit [InsightFace Model Zoo](https://github.com/deepinsight/insightface/tree/master/python-package)

### Webcam Not Working

**Error**: `getUserMedia() failed`

**Solutions**:
1. Ensure you're using HTTPS or localhost (browsers require secure context)
2. Grant camera permissions when prompted
3. Check if another application is using the webcam
4. Restart your browser

### FAISS Installation Issues

**Error**: `No module named 'faiss'`

**Solution**:
```bash
# Try CPU version
pip install faiss-cpu

# Or if you have CUDA GPU:
pip install faiss-gpu
```

If FAISS continues to cause issues, you can disable it:
```env
USE_FAISS=false
```

### CORS Errors in Browser Console

**Error**: `Access to XMLHttpRequest at 'http://localhost:8000'... has been blocked by CORS policy`

**Solution**:
1. Ensure `CORS_ORIGINS` in backend `.env` includes your frontend URL
2. Restart the backend server after changing `.env`

## Verification Checklist

- [ ] PostgreSQL is running
- [ ] Database `face_recognition_db` exists
- [ ] Database tables are created (employees, attendance_logs)
- [ ] Backend server is running on port 8000
- [ ] Frontend is running on port 5173
- [ ] Can access frontend at http://localhost:5173
- [ ] Can access API docs at http://localhost:8000/docs
- [ ] Webcam access is granted in browser

## Next Steps

Once everything is running:

1. **Register an Employee**
   - Navigate to "Register Employee"
   - Fill in employee details
   - Capture 20-50 face images
   - Submit registration

2. **Test Face Recognition**
   - Go to Dashboard
   - The system will auto-recognize faces from webcam (if implemented)
   - Or use the API endpoint `/recognize_face` to test

3. **View Attendance**
   - Check "Attendance History" for records
   - Export data as CSV

## Production Deployment

For production deployment:

1. **Security**:
   - Change `SECRET_KEY` to a strong random value
   - Use environment-specific `.env` files
   - Enable HTTPS
   - Set `API_RELOAD=false`

2. **Database**:
   - Use a production PostgreSQL instance
   - Set up regular backups
   - Configure connection pooling

3. **Backend**:
   - Use a production WSGI server (e.g., Gunicorn)
   - Set up reverse proxy (Nginx)
   - Configure logging

4. **Frontend**:
   - Build production bundle: `npm run build`
   - Serve static files through Nginx or CDN
   - Update `VITE_API_URL` to production API URL

5. **Monitoring**:
   - Set up application monitoring
   - Configure alerts for errors
   - Monitor face recognition accuracy

## Support

For issues and questions:
- Check the main README.md
- Review API documentation at `/docs`
- Check application logs in `logs/app.log`

## Quick Start Script (Windows)

Save this as `start.bat`:

```batch
@echo off
echo Starting Face Recognition Attendance System...

:: Start Backend
start cmd /k "cd backend && venv\Scripts\activate && python main.py"

:: Wait for backend to start
timeout /t 5

:: Start Frontend
start cmd /k "cd frontend && npm run dev"

echo System started! Backend: http://localhost:8000, Frontend: http://localhost:5173
```

## Quick Start Script (Linux/macOS)

Save this as `start.sh`:

```bash
#!/bin/bash
echo "Starting Face Recognition Attendance System..."

# Start Backend
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "System started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
```

Make it executable:
```bash
chmod +x start.sh
```
