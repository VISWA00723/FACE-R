# Face Recognition Attendance System

A production-ready face recognition attendance system with real-time tracking, built with FastAPI, React, and PostgreSQL. Features a fully responsive UI that works seamlessly on mobile, tablet, and desktop devices.

## ✨ Features

### Core Functionality
- **Employee Registration**: Register employees with up to 50 face images from multiple angles
- **Real-time Face Recognition**: Automatic IN/OUT logging using ArcFace embeddings
- **Admin Dashboard**: Live attendance tracking with statistics and historical reports
- **Verify Face**: Test face detection and recognition without marking attendance
- **High Accuracy**: Uses ArcFace (InsightFace) for 512D embeddings
- **Fast Search**: Optional FAISS integration for vector similarity search
- **Export Reports**: Download attendance data in CSV format

### UI/UX Features
- **📱 Fully Responsive Design**: Optimized for mobile (320px+), tablet (768px+), and desktop (1024px+)
- **🍔 Mobile Navigation**: Hamburger menu with smooth slide-out sidebar
- **📊 Dual View System**: Desktop tables automatically switch to mobile-friendly cards
- **📸 iOS Compatible**: Camera works on iPhone/iPad Safari browsers
- **🎨 Modern UI**: Clean design with Tailwind CSS, smooth animations, and transitions
- **♿ Accessibility**: Touch-friendly tap targets (44px minimum) and keyboard navigation
- **🌐 HTTPS Support**: Works with dev tunnels for remote access

## Tech Stack

### Backend
- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL
- OpenCV
- MTCNN (Face Detection)
- InsightFace (ArcFace Embeddings)
- FAISS (Optional, for fast vector search)

### Frontend
- React 18+ with TypeScript
- Vite (Build tool)
- React Router (Navigation)
- Axios (API client)
- react-webcam (Camera integration)
- Recharts (Data visualization & charts)
- TailwindCSS (Responsive styling)
- Lucide React (Modern icons)

## Project Structure

```
FACE-R/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   └── tsconfig.json
├── database/
│   └── init_db.py
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- Node.js 18+ and npm
- PostgreSQL 14+

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FACE-R
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials and other configurations.

### 3. Database Setup

Create PostgreSQL database:

```bash
createdb face_recognition_db
```

Run the database initialization script:

```bash
cd database
python init_db.py
```

### 4. Backend Setup

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Download InsightFace model (will be downloaded automatically on first run, or manually):

```bash
# The model will be auto-downloaded, but you can pre-download it
# It will download buffalo_l model (~600MB)
```

Run the backend:

```bash
python main.py
```

The API will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### 5. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📖 Usage

### Register an Employee

1. Navigate to "Register Employee" page
2. Fill in employee details (ID, Name, Department)
3. Click "Open Camera" to activate webcam
4. Capture 20-50 face images from different angles
5. Review captured images and remove any poor quality shots
6. Click "Register Employee" to submit

**Tips for Best Results:**
- Capture from different angles (front, left, right, up, down)
- Ensure good lighting conditions
- Face the camera directly
- Remove glasses or masks if possible

### Verify Face Detection (Testing)

1. Navigate to "Verify Face" page
2. Click "Open Camera" and capture a test image
3. Click "Verify Face" to test detection
4. Review results:
   - ✅ Green: Face detected and recognized
   - ⚠️ Orange: Face detected but not recognized
   - ❌ Red: No face detected
5. **Note**: This page is for testing only - no attendance is marked

### View Dashboard

1. Navigate to "Dashboard"
2. View real-time statistics (Total Employees, Present, Absent, IN/OUT counts)
3. Check attendance trend chart (last 7 days)
4. Review today's attendance logs
5. Auto-refreshes every 30 seconds

### View Attendance History

1. Navigate to "Attendance History"
2. Use filters to search by date range or employee ID
3. View paginated attendance records
4. Export filtered data as CSV
5. **Mobile**: Swipe through card views for easy browsing

### Manage Employees

1. Navigate to "Employees" page
2. View all registered employees with image counts
3. Delete employees if needed (removes all data including attendance)

### Face Recognition Flow

1. Camera captures frame
2. MTCNN detects faces
3. ArcFace generates 512D embeddings
4. System compares with stored embeddings
5. If match found (threshold < 0.6), logs attendance
6. Automatically tracks IN/OUT based on last log

## 🔌 API Endpoints

### Employee Management
- `POST /api/v1/register_employee` - Register new employee with images
- `GET /api/v1/employees` - Get all employees (with pagination)
- `GET /api/v1/employees/{employee_id}` - Get specific employee details
- `DELETE /api/v1/employees/{employee_id}` - Delete employee and all associated data

### Face Recognition
- `POST /api/v1/recognize_face` - Recognize face and mark attendance
- `POST /api/v1/detect_face` - Detect face without marking attendance (for testing)

### Attendance
- `GET /api/v1/attendance_today` - Get today's attendance with statistics
- `GET /api/v1/attendance_history` - Get historical attendance (with filters)
- `GET /api/v1/attendance_stats` - Get attendance statistics and trends
- `GET /api/v1/attendance_export` - Export attendance data as CSV

**API Documentation**: Available at `http://localhost:8000/docs` (Swagger UI)

## Configuration

### Face Recognition Settings

- `FACE_RECOGNITION_THRESHOLD`: Similarity threshold (default: 0.6)
- `MIN_FACE_SIZE`: Minimum face size for detection (default: 20px)
- `EMBEDDING_SIZE`: ArcFace embedding dimension (512D)
- `MAX_IMAGES_PER_EMPLOYEE`: Maximum images per registration (50)

### Database Schema

**employees**
- id (Primary Key)
- employee_id (Unique)
- name
- department
- embedding_vector (JSONB - stores 512D vector)
- image_count
- created_at
- updated_at

**attendance_logs**
- id (Primary Key)
- employee_id (Foreign Key)
- log_date
- in_time
- out_time
- duration
- status (IN/OUT/ABSENT)
- created_at

## Performance Optimization

### FAISS Integration

Enable FAISS for faster similarity search with large employee databases:

```env
USE_FAISS=true
FAISS_INDEX_PATH=./data/faiss_index.bin
```

FAISS provides O(log n) search time vs O(n) with direct comparison.

### Caching

The system uses in-memory caching for embeddings to reduce database queries.

## 📱 Mobile & Remote Access

### Accessing from Mobile Devices

**Local Network Access:**
```bash
# Backend must listen on all interfaces (already configured)
# Frontend Vite config includes host: '0.0.0.0'

# Access from mobile device on same network:
http://[your-ip]:5173
# Example: http://192.168.1.100:5173
```

**Remote Access via Dev Tunnel (HTTPS):**
```bash
# VS Code: Forward port 5173 with public access
# Access from anywhere:
https://[your-tunnel-url]
```

### iOS/Safari Compatibility

The system is fully compatible with iOS Safari:
- ✅ Camera access works on iPhone/iPad
- ✅ Requires HTTPS (use dev tunnel)
- ✅ Grant camera permission when prompted
- ✅ Responsive design optimized for touch

**iOS Camera Settings:**
1. Safari will prompt for camera access
2. Tap "Allow" when requested
3. If denied: Settings → Safari → Camera → Allow
4. Clear cache if issues persist

### Responsive Breakpoints

- **Mobile**: 320px - 639px (Portrait & Landscape)
- **Tablet**: 640px - 1023px
- **Desktop**: 1024px+

## 🔧 Troubleshooting

### Camera Issues

**Camera not opening on iPhone:**
- Must use HTTPS (HTTP won't work on iOS)
- Check Safari settings: Settings → Safari → Camera → Allow
- Grant camera permission when prompted
- Clear Safari cache and reload

**Camera not opening on Desktop:**
- Ensure browser has camera permission
- Check if another app is using the camera
- Try a different browser (Chrome/Firefox recommended)
- Restart browser if camera was recently used

### Face Recognition Issues

**"No face detected":**
- Ensure proper lighting (not too bright/dark)
- Face should be clearly visible and centered
- Minimum face size is 20px (adjust MIN_FACE_SIZE if needed)
- Remove masks, sunglasses, or obstructions
- Try the "Verify Face" page to test detection

**"Low recognition accuracy":**
- Increase number of training images (20-50 recommended)
- Ensure diverse angles during registration
- Capture in similar lighting conditions
- Adjust FACE_RECOGNITION_THRESHOLD (lower = stricter)
- Re-register employee with better quality images

**"Face detected but not recognized":**
- Employee may not be registered
- Use "Verify Face" page to check
- Re-register with more/better images
- Check FACE_RECOGNITION_THRESHOLD setting

### Network Issues

**"Mixed Content Error" (HTTPS page, HTTP API):**
- API requests are blocked when frontend is HTTPS but backend is HTTP
- Solution: Use relative URLs (already configured)
- Vite proxy forwards requests to backend

**API Connection Error:**
- Verify backend is running on port 8000
- Check if proxy is configured in vite.config.ts
- Ensure CORS settings include your domain
- Test API directly at http://localhost:8000/docs

### Database Issues

**Database connection error:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists: `createdb face_recognition_db`
- Check credentials and permissions

**Database initialization fails:**
- Run: `python database/init_db.py`
- Check PostgreSQL version (14+ required)
- Verify user has CREATE permission

## 📸 Screenshots

### Desktop View
- **Dashboard**: Real-time statistics with attendance trend charts
- **Register Employee**: Webcam integration with image preview grid
- **Verify Face**: Test interface with detailed detection results
- **Attendance History**: Filterable table with export functionality
- **Employee List**: Complete employee directory with management options

### Mobile View
- **Responsive Navigation**: Hamburger menu with slide-out sidebar
- **Card-Based Layouts**: Touch-optimized attendance and employee cards
- **Mobile-First Forms**: Large, touch-friendly input fields and buttons
- **Adaptive Tables**: Tables automatically convert to cards on mobile

## 🎯 Key Highlights

- **Production Ready**: Robust error handling and validation
- **Scalable**: FAISS integration for handling large employee databases
- **Secure**: CORS configuration, input validation, SQL injection protection
- **Fast**: In-memory caching, optimized queries, lazy loading
- **Modern Stack**: Latest React, FastAPI, PostgreSQL versions
- **Developer Friendly**: Comprehensive API docs, TypeScript types, clean code structure
- **User Friendly**: Intuitive UI, helpful error messages, responsive design

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set production values in `.env`
2. **Database**: Use managed PostgreSQL service (AWS RDS, Azure, etc.)
3. **Backend**: Deploy with Gunicorn/Uvicorn workers
4. **Frontend**: Build with `npm run build` and serve static files
5. **HTTPS**: Required for camera access - use nginx/Apache with SSL
6. **CORS**: Update CORS_ORIGINS for production domains
7. **Secrets**: Change SECRET_KEY and use strong credentials

### Quick Deploy Commands

```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.api.app:app

# Frontend
cd frontend
npm run build
# Serve the dist/ folder with nginx or any static file server
```

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Support

- **Issues**: Create an issue in the repository for bugs or feature requests
- **Questions**: Use GitHub Discussions for questions and help
- **Contributing**: Pull requests are welcome! See CONTRIBUTING.md for guidelines

## 🙏 Acknowledgments

- **InsightFace**: For the excellent ArcFace model
- **MTCNN**: For reliable face detection
- **FastAPI**: For the amazing Python web framework
- **React**: For the powerful UI library

---

**Built with ❤️ using modern web technologies**
