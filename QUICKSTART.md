# Quick Start Guide

Get the Face Recognition Attendance System up and running in 10 minutes!

## Prerequisites Check

✅ Python 3.12+ installed
✅ Node.js 18+ installed
✅ PostgreSQL 14+ installed and running
✅ Git installed

## 5-Minute Setup

### Step 1: Clone and Configure (1 min)

```bash
# Clone repository
git clone <your-repo-url>
cd FACE-R

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/macOS

# Edit .env and update database credentials
```

**Important**: Update these values in `.env`:
```env
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
SECRET_KEY=generate-a-random-secret-key
```

### Step 2: Setup Database (2 min)

```bash
# Create database (from PostgreSQL)
createdb face_recognition_db

# Initialize tables
cd database
python init_db.py
cd ..
```

### Step 3: Setup Backend (3 min)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Install dependencies (may take 2-3 minutes)
pip install -r requirements.txt

cd ..
```

### Step 4: Setup Frontend (2 min)

```bash
cd frontend

# Copy frontend environment
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/macOS

# Install dependencies
npm install

cd ..
```

### Step 5: Start Everything (2 min)

**Option A: Using Start Script (Easiest)**

Windows:
```bash
start.bat
```

Linux/macOS:
```bash
chmod +x start.sh
./start.sh
```

**Option B: Manual Start**

Terminal 1 (Backend):
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
python main.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## Access the Application

🌐 **Frontend**: http://localhost:5173
📚 **API Docs**: http://localhost:8000/docs
🔧 **API**: http://localhost:8000

## First Steps

### 1. Register Your First Employee

1. Open http://localhost:5173
2. Navigate to "Register Employee"
3. Fill in details:
   - Employee ID: `EMP001`
   - Name: `Your Name`
   - Department: `Engineering`
4. Click "Open Camera"
5. Capture 20-30 images (different angles)
6. Click "Register Employee"

**Pro Tip**: Capture images from:
- Front view (10 images)
- Left side (5 images)
- Right side (5 images)
- Slightly up (5 images)
- Slightly down (5 images)

### 2. Test Face Recognition

Currently, recognition happens when you:
- Use the `/recognize_face` API endpoint
- Implement a live recognition component (coming soon)

**Test via API**:
```bash
# Capture an image and convert to base64, then:
curl -X POST http://localhost:8000/api/v1/recognize_face \
  -H "Content-Type: application/json" \
  -d '{"image": "your-base64-image-here"}'
```

### 3. View Dashboard

1. Navigate to "Dashboard"
2. See today's attendance summary
3. View attendance statistics chart
4. Check who's IN/OUT

### 4. Export Reports

1. Go to "Attendance History"
2. Set date filters (optional)
3. Click "Export CSV"
4. Open in Excel or Google Sheets

## Common Issues & Fixes

### Issue: "Database connection failed"

**Fix**:
```bash
# Check if PostgreSQL is running
# Windows: Check Services
# Linux: sudo systemctl status postgresql

# Test connection
psql -U postgres -d face_recognition_db
```

### Issue: "No module named 'app'"

**Fix**: Ensure you're in the `backend` directory and virtual environment is activated.

### Issue: "Port 8000 already in use"

**Fix**: Change port in `.env`:
```env
API_PORT=8001
```
And update `frontend/.env`:
```env
VITE_API_URL=http://localhost:8001
```

### Issue: "Webcam not working"

**Fix**:
- Allow camera permissions in browser
- Ensure no other app is using the camera
- Use HTTPS or localhost (required by browsers)

### Issue: "Face not detected"

**Checklist**:
- ✅ Good lighting
- ✅ Face clearly visible
- ✅ Camera working
- ✅ No obstructions (mask, glasses)

### Issue: "Model download failed"

**Fix**: The InsightFace model downloads automatically (~600MB). Ensure:
- Stable internet connection
- Sufficient disk space
- Check firewall settings

Model location: `~/.insightface/models/`

## Performance Tips

### 1. Enable FAISS (Already enabled by default)

In `.env`:
```env
USE_FAISS=true
```

### 2. Adjust Recognition Threshold

In `.env`:
```env
FACE_RECOGNITION_THRESHOLD=0.6  # Lower = stricter (0.4-0.8 recommended)
```

### 3. Optimize Image Count

- **Minimum**: 10 images (basic accuracy)
- **Recommended**: 20-30 images (good accuracy)
- **Maximum**: 50 images (best accuracy)

## Next Steps

### Production Deployment

Read [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Nginx + Gunicorn setup
- Docker deployment
- SSL/HTTPS configuration
- Security hardening
- Monitoring setup

### API Integration

Read [API.md](API.md) for:
- Complete endpoint reference
- Request/response examples
- Error handling
- Code examples in Python, JavaScript, cURL

### Customization

Read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Coding standards
- How to add features
- Testing guidelines

## Useful Commands

### Backend

```bash
# Start backend
cd backend && venv\Scripts\activate && python main.py

# Run tests
pytest tests/

# Check code style
black backend/ && flake8 backend/

# View logs
tail -f logs/app.log
```

### Frontend

```bash
# Start development server
cd frontend && npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Database

```bash
# Connect to database
psql -U postgres -d face_recognition_db

# Backup database
pg_dump -U postgres face_recognition_db > backup.sql

# Restore database
psql -U postgres face_recognition_db < backup.sql

# Check table sizes
psql -U postgres -d face_recognition_db -c "\dt+"
```

## Architecture Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │────────▶│   Backend    │────────▶│  PostgreSQL │
│  (React)    │  HTTP   │  (FastAPI)   │  SQL    │  Database   │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │  InsightFace │
                        │   (ArcFace)  │
                        └──────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │     FAISS    │
                        │ (Vector DB)  │
                        └──────────────┘
```

## Tech Stack Summary

| Component | Technology |
|-----------|------------|
| **Frontend** | React 18 + TypeScript + TailwindCSS |
| **Backend** | Python 3.12 + FastAPI |
| **Database** | PostgreSQL 14+ |
| **Face Detection** | MTCNN |
| **Face Recognition** | ArcFace (InsightFace) |
| **Vector Search** | FAISS |
| **API Docs** | Swagger UI + ReDoc |

## Getting Help

1. **Documentation**
   - README.md - Overview
   - SETUP.md - Detailed setup
   - API.md - API reference
   - DEPLOYMENT.md - Production deployment

2. **Interactive API Docs**
   - http://localhost:8000/docs

3. **Logs**
   - Backend: `logs/app.log`
   - Frontend: Browser console

4. **GitHub Issues**
   - Report bugs
   - Request features
   - Ask questions

## Success Checklist

- [ ] PostgreSQL running
- [ ] Database created and initialized
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can access frontend in browser
- [ ] Can access API docs
- [ ] Webcam access granted
- [ ] At least one employee registered
- [ ] Face recognition tested
- [ ] Dashboard displays data

## Congratulations! 🎉

You now have a fully functional face recognition attendance system running!

**What's Next?**
- Register more employees
- Test face recognition accuracy
- Customize the UI
- Deploy to production
- Integrate with your existing systems

For detailed information, refer to the comprehensive documentation in the repository.

---

**Need help?** Check the documentation or open an issue on GitHub!
