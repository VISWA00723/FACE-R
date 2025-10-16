# Face Recognition Attendance System

A production-ready face recognition attendance system with real-time tracking, built with FastAPI, React, and PostgreSQL.

## Features

- **Employee Registration**: Register employees with up to 50 face images
- **Real-time Face Recognition**: Automatic IN/OUT logging using ArcFace embeddings
- **Admin Dashboard**: Live attendance tracking and historical reports
- **High Accuracy**: Uses ArcFace (InsightFace) for 512D embeddings
- **Fast Search**: Optional FAISS integration for vector similarity search
- **Export Reports**: Download attendance data in CSV format

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
- React 18+
- TypeScript
- Axios
- react-webcam
- Recharts (for data visualization)
- TailwindCSS

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

## Usage

### Register an Employee

1. Navigate to "Register Employee" page
2. Fill in employee details (ID, Name, Department)
3. Use webcam to capture up to 50 face images
4. Submit the registration

### View Attendance

1. Navigate to "Dashboard"
2. View today's attendance (IN/OUT status)
3. Check historical attendance with charts
4. Export reports as needed

### Face Recognition Flow

1. Camera captures frame
2. MTCNN detects faces
3. ArcFace generates 512D embeddings
4. System compares with stored embeddings
5. If match found (threshold < 0.6), logs attendance
6. Automatically tracks IN/OUT based on last log

## API Endpoints

### Employee Management
- `POST /api/v1/register_employee` - Register new employee with images
- `GET /api/v1/employees` - Get all employees
- `GET /api/v1/employees/{employee_id}` - Get specific employee

### Face Recognition
- `POST /api/v1/recognize_face` - Recognize face from image

### Attendance
- `GET /api/v1/attendance_today` - Get today's attendance
- `GET /api/v1/attendance_history` - Get historical attendance
- `GET /api/v1/attendance_export` - Export attendance as CSV

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

## Troubleshooting

### Issue: "No face detected"
- Ensure proper lighting
- Face should be clearly visible
- Try adjusting MIN_FACE_SIZE setting

### Issue: "Low recognition accuracy"
- Increase number of training images (up to 50)
- Ensure diverse angles and lighting during registration
- Adjust FACE_RECOGNITION_THRESHOLD

### Issue: Database connection error
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
