# Project Structure

Complete directory structure and file organization of the Face Recognition Attendance System.

## Root Directory

```
FACE-R/
├── backend/                    # Backend API (Python + FastAPI)
├── frontend/                   # Frontend UI (React + TypeScript)
├── database/                   # Database initialization scripts
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # Project overview
├── SETUP.md                    # Setup instructions
├── QUICKSTART.md               # Quick start guide
├── DEPLOYMENT.md               # Production deployment guide
├── API.md                      # API documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
├── PROJECT_STRUCTURE.md        # This file
├── start.bat                   # Windows start script
└── start.sh                    # Linux/macOS start script
```

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py            # App package initialization
│   │
│   ├── api/                   # API layer
│   │   ├── __init__.py
│   │   ├── app.py            # FastAPI application setup
│   │   └── endpoints/        # API endpoints
│   │       ├── __init__.py
│   │       ├── employee.py   # Employee management endpoints
│   │       ├── recognition.py # Face recognition endpoints
│   │       └── attendance.py # Attendance endpoints
│   │
│   ├── core/                  # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py         # Application settings
│   │   └── database.py       # Database connection
│   │
│   ├── models/                # Database models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── employee.py       # Employee model
│   │   └── attendance.py     # Attendance log model
│   │
│   ├── schemas/               # Pydantic schemas (validation)
│   │   ├── __init__.py
│   │   ├── employee.py       # Employee schemas
│   │   ├── attendance.py     # Attendance schemas
│   │   └── recognition.py    # Recognition schemas
│   │
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── face_recognition_service.py  # Face recognition logic
│   │   ├── attendance_service.py        # Attendance management
│   │   └── faiss_service.py            # FAISS vector search
│   │
│   └── utils/                 # Utility functions
│       └── __init__.py
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
└── tests/                     # Unit tests (to be added)
    └── __init__.py
```

### Backend File Details

| File | Purpose | Key Features |
|------|---------|--------------|
| `app/api/app.py` | FastAPI setup | CORS, routes, middleware |
| `app/api/endpoints/employee.py` | Employee CRUD | Register, list, get, delete |
| `app/api/endpoints/recognition.py` | Face recognition | Recognize, detect face |
| `app/api/endpoints/attendance.py` | Attendance | Today, history, stats, export |
| `app/core/config.py` | Configuration | Settings from .env |
| `app/core/database.py` | DB connection | Session management |
| `app/models/employee.py` | Employee model | ID, name, dept, embeddings |
| `app/models/attendance.py` | Attendance model | Date, time, status, duration |
| `app/services/face_recognition_service.py` | Face processing | MTCNN, ArcFace, embeddings |
| `app/services/attendance_service.py` | Attendance logic | Log, query, stats |
| `app/services/faiss_service.py` | Vector search | Fast similarity search |

## Frontend Structure

```
frontend/
├── src/
│   ├── components/            # Reusable components
│   │   └── Layout.tsx        # Main layout with navigation
│   │
│   ├── pages/                # Page components
│   │   ├── Dashboard.tsx     # Dashboard with stats
│   │   ├── RegisterEmployee.tsx  # Employee registration
│   │   ├── AttendanceHistory.tsx # Attendance history
│   │   └── EmployeeList.tsx  # Employee list
│   │
│   ├── services/             # API services
│   │   └── api.ts           # Axios API calls
│   │
│   ├── types/                # TypeScript types
│   │   └── index.ts         # Type definitions
│   │
│   ├── utils/                # Utility functions
│   │   └── helpers.ts       # Helper functions
│   │
│   ├── App.tsx              # Main App component
│   ├── main.tsx             # Application entry
│   └── index.css            # Global styles
│
├── public/                   # Static assets
│   └── vite.svg
│
├── index.html               # HTML template
├── package.json             # Node dependencies
├── tsconfig.json            # TypeScript config
├── tsconfig.node.json       # TypeScript Node config
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind CSS config
├── postcss.config.js        # PostCSS config
├── .eslintrc.cjs           # ESLint config
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment template
└── .gitignore              # Git ignore rules
```

### Frontend File Details

| File | Purpose | Key Features |
|------|---------|--------------|
| `components/Layout.tsx` | App layout | Navigation, sidebar |
| `pages/Dashboard.tsx` | Dashboard | Stats, charts, today's attendance |
| `pages/RegisterEmployee.tsx` | Registration | Webcam, capture images, submit |
| `pages/AttendanceHistory.tsx` | History | Filter, pagination, export |
| `pages/EmployeeList.tsx` | Employee list | View, delete employees |
| `services/api.ts` | API client | Axios, API calls |
| `types/index.ts` | TypeScript types | Interface definitions |
| `utils/helpers.ts` | Utilities | Format dates, download files |

## Database Structure

```
database/
├── init_db.py               # Database initialization script
└── migrations/              # Database migrations (future)
    └── README.md
```

### Database Schema

#### `employees` Table
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    department VARCHAR NOT NULL,
    embedding_vector JSON NOT NULL,    -- 512D vector as JSON
    image_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_employee_id ON employees(employee_id);
```

#### `attendance_logs` Table
```sql
CREATE TABLE attendance_logs (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR NOT NULL,
    log_date DATE NOT NULL,
    in_time TIMESTAMP,
    out_time TIMESTAMP,
    duration FLOAT,                    -- Duration in hours
    status VARCHAR DEFAULT 'IN',       -- IN, OUT, ABSENT
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Indexes
CREATE INDEX idx_attendance_employee_id ON attendance_logs(employee_id);
CREATE INDEX idx_attendance_log_date ON attendance_logs(log_date);
CREATE INDEX idx_attendance_employee_date ON attendance_logs(employee_id, log_date);
```

## Data Flow

### Employee Registration Flow

```
User Input (Frontend)
    ↓
Capture Images (react-webcam)
    ↓
Convert to Base64
    ↓
POST /api/v1/register_employee
    ↓
Backend receives data
    ↓
Validate input (Pydantic)
    ↓
Process images (MTCNN)
    ↓
Extract embeddings (ArcFace)
    ↓
Average embeddings
    ↓
Store in PostgreSQL
    ↓
Add to FAISS index
    ↓
Return success response
    ↓
Update UI (Frontend)
```

### Face Recognition Flow

```
Camera Frame (Frontend)
    ↓
Convert to Base64
    ↓
POST /api/v1/recognize_face
    ↓
Backend receives image
    ↓
Detect face (MTCNN)
    ↓
Extract embedding (ArcFace)
    ↓
Search in FAISS (or direct comparison)
    ↓
Find best match
    ↓
Check threshold
    ↓
If recognized:
    ├─ Get employee details
    ├─ Determine IN/OUT status
    ├─ Log attendance
    └─ Return employee info
    ↓
Display result (Frontend)
```

### Attendance Query Flow

```
User requests attendance
    ↓
GET /api/v1/attendance_today
    ↓
Query database
    ↓
Join with employees table
    ↓
Calculate statistics
    ↓
Format response
    ↓
Return JSON
    ↓
Display in dashboard
```

## Configuration Files

### Environment Variables (`.env`)

```env
# Database
DATABASE_URL=postgresql://user:pass@host:port/db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=face_recognition_db

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# Face Recognition
FACE_RECOGNITION_THRESHOLD=0.6
MIN_FACE_SIZE=20
EMBEDDING_SIZE=512
MAX_IMAGES_PER_EMPLOYEE=50

# FAISS
USE_FAISS=true
FAISS_INDEX_PATH=./data/faiss_index.bin

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend Environment (`.env`)

```env
VITE_API_URL=http://localhost:8000
```

## Runtime Directories

These directories are created at runtime:

```
backend/
├── data/                    # FAISS index storage
│   ├── faiss_index.bin
│   └── faiss_index_metadata.pkl
│
├── logs/                    # Application logs
│   └── app.log
│
└── uploads/                 # Uploaded files (if any)
```

## Dependencies

### Backend Dependencies

```
fastapi          # Web framework
uvicorn          # ASGI server
sqlalchemy       # ORM
psycopg2-binary  # PostgreSQL driver
opencv-python    # Image processing
mtcnn            # Face detection
insightface      # Face recognition (ArcFace)
onnxruntime      # Model runtime
faiss-cpu        # Vector similarity search
numpy            # Numerical operations
pydantic         # Data validation
python-dotenv    # Environment variables
```

### Frontend Dependencies

```
react            # UI library
react-dom        # React DOM rendering
react-router-dom # Routing
react-webcam     # Webcam access
axios            # HTTP client
recharts         # Charts
lucide-react     # Icons
tailwindcss      # CSS framework
typescript       # Type safety
vite             # Build tool
```

## API Endpoints

### Employee Management
- `POST /api/v1/register_employee` - Register employee
- `GET /api/v1/employees` - List employees
- `GET /api/v1/employees/{id}` - Get employee
- `DELETE /api/v1/employees/{id}` - Delete employee

### Face Recognition
- `POST /api/v1/recognize_face` - Recognize face
- `POST /api/v1/detect_face` - Detect face (testing)

### Attendance
- `GET /api/v1/attendance_today` - Today's attendance
- `GET /api/v1/attendance_history` - Historical attendance
- `GET /api/v1/attendance_stats` - Statistics
- `GET /api/v1/attendance_export` - Export CSV

### System
- `GET /` - API info
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## Security Considerations

### Current Implementation
- ✅ Input validation (Pydantic)
- ✅ SQL injection protection (SQLAlchemy)
- ✅ CORS configuration
- ✅ Environment-based config
- ✅ Secure database connections

### Production Recommendations
- ⚠️ Add JWT authentication
- ⚠️ Implement rate limiting
- ⚠️ Enable HTTPS/SSL
- ⚠️ Add API key authentication
- ⚠️ Implement role-based access control
- ⚠️ Add request logging
- ⚠️ Enable audit trails

## Performance Optimization

### Backend
- Database indexes on frequent queries
- FAISS for O(log n) similarity search
- Connection pooling (SQLAlchemy)
- Lazy model loading
- Efficient embedding storage (JSON)

### Frontend
- Code splitting (Vite)
- Lazy loading of routes
- Image optimization
- Memoization (useMemo, useCallback)
- Virtual scrolling for large lists

## Testing Strategy

### Backend Tests (Planned)
```
backend/tests/
├── test_face_recognition.py
├── test_attendance.py
├── test_employee.py
└── test_api.py
```

### Frontend Tests (Planned)
```
frontend/src/tests/
├── Dashboard.test.tsx
├── RegisterEmployee.test.tsx
└── api.test.ts
```

## Deployment Architecture

### Development
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Frontend   │────▶│   Backend    │────▶│  PostgreSQL │
│ localhost:  │HTTP │ localhost:   │ SQL │  localhost: │
│    5173     │     │    8000      │     │    5432     │
└─────────────┘     └──────────────┘     └─────────────┘
```

### Production
```
                      ┌──────────────┐
                      │   Nginx      │
                      │  (Reverse    │
                      │   Proxy)     │
                      └───────┬──────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
          ┌─────────▼─────────┐  ┌──────▼──────┐
          │   Frontend        │  │   Backend   │
          │   (Static)        │  │  (Gunicorn) │
          │   React Build     │  │   FastAPI   │
          └───────────────────┘  └──────┬──────┘
                                        │
                                 ┌──────▼──────┐
                                 │  PostgreSQL │
                                 │  (Managed)  │
                                 └─────────────┘
```

## Monitoring Points

### Application Metrics
- API response times
- Face recognition accuracy
- Database query performance
- FAISS search latency
- Error rates

### System Metrics
- CPU usage
- Memory usage
- Disk I/O
- Network bandwidth
- Database connections

### Business Metrics
- Daily attendance rate
- Average check-in time
- Recognition success rate
- Employee registration count

## Backup Strategy

### Database Backups
- Daily automatic backups
- Retention: 7 days (rolling)
- Location: `/var/backups/face-recognition/`

### File Backups
- FAISS index files
- Uploaded images (if stored)
- Configuration files

## Version Control

### Git Branching Strategy
```
main              # Production-ready code
├── develop       # Development branch
│   ├── feature/* # Feature branches
│   ├── bugfix/*  # Bug fix branches
│   └── hotfix/*  # Urgent fixes
```

### Ignored Files (.gitignore)
- `.env` files
- `node_modules/`
- `venv/`
- `__pycache__/`
- `*.pyc`
- `dist/`
- `build/`
- `logs/`
- `data/`

## Future Enhancements

### Planned Features
- [ ] Real-time websocket updates
- [ ] Mobile app (React Native)
- [ ] Multiple camera support
- [ ] Face anti-spoofing
- [ ] Shift management
- [ ] Leave management
- [ ] HR system integration
- [ ] Advanced analytics

### Technical Improvements
- [ ] Microservices architecture
- [ ] Redis caching layer
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Performance monitoring
- [ ] Error tracking (Sentry)

## Documentation

### Available Guides
- **README.md** - Project overview and features
- **SETUP.md** - Detailed setup instructions
- **QUICKSTART.md** - 10-minute quick start
- **DEPLOYMENT.md** - Production deployment
- **API.md** - Complete API reference
- **CONTRIBUTING.md** - Contribution guidelines
- **CHANGELOG.md** - Version history
- **PROJECT_STRUCTURE.md** - This file

### Online Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Support & Community

### Getting Help
1. Check documentation
2. Search existing issues
3. Ask in discussions
4. Open new issue

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Development workflow
- Testing requirements
- Pull request process

---

**Last Updated**: 2024-01-15
**Version**: 1.0.0
**Maintainers**: Project Team
