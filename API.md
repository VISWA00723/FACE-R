# API Documentation

Complete API reference for the Face Recognition Attendance System.

**Base URL**: `http://localhost:8000/api/v1`

**Content-Type**: `application/json`

## Authentication

Currently, the API does not require authentication. For production, implement JWT token authentication.

## Endpoints

### Health Check

#### GET /
Get API status

**Response**
```json
{
  "message": "Face Recognition Attendance System API",
  "version": "1.0.0",
  "status": "running"
}
```

#### GET /health
Health check endpoint

**Response**
```json
{
  "status": "healthy"
}
```

---

## Employee Management

### Register Employee

#### POST /api/v1/register_employee

Register a new employee with face images.

**Request Body**
```json
{
  "employee_id": "EMP001",
  "name": "John Doe",
  "department": "Engineering",
  "images": [
    "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
    "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
  ]
}
```

**Parameters**
- `employee_id` (string, required): Unique employee identifier
- `name` (string, required): Employee full name
- `department` (string, required): Department name
- `images` (array, required): Array of base64 encoded images (1-50 images)

**Response** `201 Created`
```json
{
  "id": 1,
  "employee_id": "EMP001",
  "name": "John Doe",
  "department": "Engineering",
  "image_count": 30,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error Responses**
- `400 Bad Request`: Invalid data or duplicate employee ID
- `500 Internal Server Error`: Server error

---

### Get All Employees

#### GET /api/v1/employees

Retrieve all registered employees.

**Query Parameters**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum records to return (default: 100)

**Response** `200 OK`
```json
{
  "total": 10,
  "employees": [
    {
      "id": 1,
      "employee_id": "EMP001",
      "name": "John Doe",
      "department": "Engineering",
      "image_count": 30,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ]
}
```

---

### Get Employee by ID

#### GET /api/v1/employees/{employee_id}

Retrieve specific employee details.

**Path Parameters**
- `employee_id` (string, required): Employee ID

**Response** `200 OK`
```json
{
  "id": 1,
  "employee_id": "EMP001",
  "name": "John Doe",
  "department": "Engineering",
  "image_count": 30,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

**Error Responses**
- `404 Not Found`: Employee not found

---

### Delete Employee

#### DELETE /api/v1/employees/{employee_id}

Delete an employee and all associated data.

**Path Parameters**
- `employee_id` (string, required): Employee ID

**Response** `204 No Content`

**Error Responses**
- `404 Not Found`: Employee not found

---

## Face Recognition

### Recognize Face

#### POST /api/v1/recognize_face

Recognize a face from an image and log attendance.

**Request Body**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Parameters**
- `image` (string, required): Base64 encoded image

**Response** `200 OK`

**Success (Face Recognized)**
```json
{
  "recognized": true,
  "employee_id": "EMP001",
  "name": "John Doe",
  "department": "Engineering",
  "confidence": 0.92,
  "status": "IN",
  "timestamp": "2024-01-15T09:00:00",
  "message": "Welcome John Doe! Attendance marked as IN."
}
```

**Not Recognized**
```json
{
  "recognized": false,
  "employee_id": null,
  "name": null,
  "department": null,
  "confidence": null,
  "status": "UNKNOWN",
  "timestamp": "2024-01-15T09:00:00",
  "message": "Face not recognized. Please ensure your face is clearly visible or register first."
}
```

**Status Values**
- `IN`: Employee checked in
- `OUT`: Employee checked out
- `UNKNOWN`: Face not recognized

**Error Responses**
- `404 Not Found`: No employees registered
- `500 Internal Server Error`: Recognition error

---

### Detect Face

#### POST /api/v1/detect_face

Detect if a face exists in an image (testing endpoint).

**Request Body**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response** `200 OK`
```json
{
  "face_detected": true,
  "num_faces": 1,
  "message": "Detected 1 face(s) in image"
}
```

---

## Attendance

### Get Today's Attendance

#### GET /api/v1/attendance_today

Retrieve today's attendance summary and logs.

**Response** `200 OK`
```json
{
  "date": "2024-01-15",
  "total_employees": 50,
  "present": 45,
  "absent": 5,
  "in_count": 40,
  "out_count": 5,
  "attendance_logs": [
    {
      "id": 1,
      "employee_id": "EMP001",
      "employee_name": "John Doe",
      "department": "Engineering",
      "log_date": "2024-01-15",
      "in_time": "2024-01-15T09:00:00",
      "out_time": "2024-01-15T18:00:00",
      "duration": 9.0,
      "status": "OUT",
      "created_at": "2024-01-15T09:00:00"
    }
  ]
}
```

---

### Get Attendance History

#### GET /api/v1/attendance_history

Retrieve historical attendance records with filters.

**Query Parameters**
- `start_date` (date, optional): Start date (YYYY-MM-DD)
- `end_date` (date, optional): End date (YYYY-MM-DD)
- `employee_id` (string, optional): Filter by employee ID
- `limit` (integer, optional): Max records (default: 100, max: 1000)
- `offset` (integer, optional): Offset for pagination (default: 0)

**Example Request**
```
GET /api/v1/attendance_history?start_date=2024-01-01&end_date=2024-01-31&limit=50&offset=0
```

**Response** `200 OK`
```json
{
  "total": 1500,
  "attendance_logs": [
    {
      "id": 1,
      "employee_id": "EMP001",
      "employee_name": "John Doe",
      "department": "Engineering",
      "log_date": "2024-01-15",
      "in_time": "2024-01-15T09:00:00",
      "out_time": "2024-01-15T18:00:00",
      "duration": 9.0,
      "status": "OUT",
      "created_at": "2024-01-15T09:00:00"
    }
  ]
}
```

---

### Get Attendance Statistics

#### GET /api/v1/attendance_stats

Get attendance statistics for a date range.

**Query Parameters**
- `start_date` (date, optional): Start date (default: 7 days ago)
- `end_date` (date, optional): End date (default: today)

**Response** `200 OK`
```json
{
  "start_date": "2024-01-08",
  "end_date": "2024-01-15",
  "total_employees": 50,
  "average_present": 45.5,
  "daily_stats": [
    {
      "date": "2024-01-15",
      "present": 45,
      "in": 40,
      "out": 5
    },
    {
      "date": "2024-01-14",
      "present": 46,
      "in": 42,
      "out": 4
    }
  ]
}
```

---

### Export Attendance

#### GET /api/v1/attendance_export

Export attendance data as CSV file.

**Query Parameters**
- `start_date` (date, optional): Start date (YYYY-MM-DD)
- `end_date` (date, optional): End date (YYYY-MM-DD)
- `employee_id` (string, optional): Filter by employee ID

**Response** `200 OK`
- Content-Type: `text/csv`
- File download with name: `attendance_export_YYYYMMDD_HHMMSS.csv`

**CSV Format**
```csv
Employee ID,Name,Department,Date,In Time,Out Time,Duration (hours),Status
EMP001,John Doe,Engineering,2024-01-15,2024-01-15 09:00:00,2024-01-15 18:00:00,9.00,OUT
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error description"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error description"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing:
- Rate limiting per IP
- Rate limiting per endpoint
- Authentication with API keys

---

## Base64 Image Format

Images should be encoded as base64 with optional data URL prefix:

**With Data URL**
```
data:image/jpeg;base64,/9j/4AAQSkZJRg...
```

**Without Data URL**
```
/9j/4AAQSkZJRg...
```

Both formats are supported.

---

## Best Practices

### Face Recognition
1. Ensure good lighting conditions
2. Face should be clearly visible
3. Minimum image size: 640x480
4. Supported formats: JPEG, PNG

### Employee Registration
1. Capture 20-50 images per employee
2. Use different angles (front, left, right, up, down)
3. Maintain consistent lighting
4. No glasses or masks if possible

### Performance
1. Use FAISS for faster recognition with large databases
2. Resize images to reasonable dimensions before sending
3. Compress images (JPEG quality 85-95)
4. Use pagination for large result sets

---

## Interactive API Documentation

For interactive API documentation with "Try it out" functionality, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide:
- Complete schema definitions
- Request/response examples
- Try out functionality
- Schema validation

---

## Code Examples

### Python

```python
import requests
import base64

# Register employee
with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    'http://localhost:8000/api/v1/register_employee',
    json={
        'employee_id': 'EMP001',
        'name': 'John Doe',
        'department': 'Engineering',
        'images': [f'data:image/jpeg;base64,{image_data}']
    }
)
print(response.json())

# Recognize face
response = requests.post(
    'http://localhost:8000/api/v1/recognize_face',
    json={'image': f'data:image/jpeg;base64,{image_data}'}
)
print(response.json())
```

### JavaScript/TypeScript

```javascript
// Register employee
const response = await fetch('http://localhost:8000/api/v1/register_employee', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    employee_id: 'EMP001',
    name: 'John Doe',
    department: 'Engineering',
    images: [base64Image]
  })
});
const data = await response.json();

// Get today's attendance
const attendance = await fetch('http://localhost:8000/api/v1/attendance_today');
const todayData = await attendance.json();
```

### cURL

```bash
# Register employee
curl -X POST http://localhost:8000/api/v1/register_employee \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "EMP001",
    "name": "John Doe",
    "department": "Engineering",
    "images": ["base64_image_data"]
  }'

# Get today's attendance
curl http://localhost:8000/api/v1/attendance_today

# Export attendance
curl "http://localhost:8000/api/v1/attendance_export?start_date=2024-01-01&end_date=2024-01-31" \
  -o attendance.csv
```

---

## Versioning

Current API version: **v1**

The API version is included in the URL path: `/api/v1/`

Future versions will be released as `/api/v2/`, etc.

---

## Support

For API issues or questions:
- Check the interactive documentation at `/docs`
- Review error messages in responses
- Check backend logs for detailed error information
- Open an issue on the project repository
