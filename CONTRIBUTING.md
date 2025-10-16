# Contributing to Face Recognition Attendance System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the Repository**
   - Click the "Fork" button on GitHub
   - Clone your fork locally

2. **Set Up Development Environment**
   - Follow instructions in [SETUP.md](SETUP.md)
   - Ensure all tests pass

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8  # Development tools
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Database Setup

```bash
cd database
python init_db.py
```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, Node version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case explanation**
- **Expected benefits**
- **Possible implementation approach**

### Code Contributions

#### Areas for Contribution

- **Face Recognition**
  - Improve accuracy
  - Add support for more face detection models
  - Optimize recognition speed
  
- **Backend**
  - Add authentication/authorization
  - Improve API performance
  - Add more endpoints
  - Enhance error handling
  
- **Frontend**
  - Improve UI/UX
  - Add more visualizations
  - Enhance accessibility
  - Add dark mode
  
- **Documentation**
  - Improve existing docs
  - Add tutorials
  - Translate documentation
  
- **Testing**
  - Add unit tests
  - Add integration tests
  - Add E2E tests

## Coding Standards

### Python (Backend)

Follow PEP 8 style guide:

```bash
# Format code
black backend/

# Check style
flake8 backend/
```

**Key Points:**
- Use 4 spaces for indentation
- Maximum line length: 88 characters (Black default)
- Use type hints where possible
- Write docstrings for functions/classes
- Use meaningful variable names

**Example:**
```python
def process_face_embedding(
    image: np.ndarray,
    model: FaceAnalysis
) -> Optional[np.ndarray]:
    """
    Process face image and extract embedding.
    
    Args:
        image: Input image as numpy array
        model: Face analysis model
        
    Returns:
        512D embedding vector or None if no face detected
    """
    try:
        faces = model.get(image)
        if len(faces) == 0:
            return None
        return faces[0].embedding
    except Exception as e:
        logger.error(f"Error processing embedding: {e}")
        return None
```

### TypeScript/React (Frontend)

Follow Airbnb style guide:

```bash
# Lint code
npm run lint
```

**Key Points:**
- Use functional components with hooks
- Use TypeScript for type safety
- Use meaningful component names
- Keep components small and focused
- Use proper prop types

**Example:**
```typescript
interface EmployeeCardProps {
  employee: Employee;
  onDelete: (id: string) => void;
}

const EmployeeCard: React.FC<EmployeeCardProps> = ({ employee, onDelete }) => {
  const handleDelete = () => {
    if (confirm(`Delete ${employee.name}?`)) {
      onDelete(employee.employee_id);
    }
  };

  return (
    <div className="card">
      <h3>{employee.name}</h3>
      <p>{employee.department}</p>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
};
```

### Git Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add employee photo upload
fix: resolve face detection timeout issue
docs: update API documentation
refactor: optimize embedding comparison
test: add unit tests for attendance service
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Writing Tests

**Backend (pytest):**
```python
def test_face_embedding_extraction():
    """Test face embedding extraction"""
    service = FaceRecognitionService()
    image = cv2.imread('test_image.jpg')
    embedding = service.extract_face_embedding(image)
    
    assert embedding is not None
    assert embedding.shape == (512,)
    assert np.linalg.norm(embedding) > 0
```

**Frontend (Jest/React Testing Library):**
```typescript
import { render, screen } from '@testing-library/react';
import EmployeeCard from './EmployeeCard';

test('renders employee information', () => {
  const employee = {
    employee_id: 'EMP001',
    name: 'John Doe',
    department: 'Engineering'
  };
  
  render(<EmployeeCard employee={employee} />);
  
  expect(screen.getByText('John Doe')).toBeInTheDocument();
  expect(screen.getByText('Engineering')).toBeInTheDocument();
});
```

## Pull Request Process

1. **Update Documentation**
   - Update README.md if needed
   - Update API.md for API changes
   - Add inline code comments

2. **Test Your Changes**
   - Run all tests
   - Test manually in development
   - Ensure no breaking changes

3. **Create Pull Request**
   - Use clear title and description
   - Reference related issues
   - Include screenshots for UI changes
   - Request review from maintainers

4. **Pull Request Template**

   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing completed
   - [ ] All tests pass
   
   ## Screenshots (if applicable)
   
   ## Related Issues
   Closes #123
   ```

5. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Respond to comments

6. **Merge**
   - Maintainer will merge once approved
   - Delete your branch after merge

## Project Structure

```
FACE-R/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core configuration
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── utils/    # Utility functions
│   └── tests/        # Backend tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   ├── types/      # TypeScript types
│   │   └── utils/      # Utility functions
│   └── tests/          # Frontend tests
├── database/         # Database scripts
└── docs/            # Additional documentation
```

## Development Tips

### Backend

1. **Use logging instead of print**
   ```python
   logger.info(f"Processing employee {employee_id}")
   ```

2. **Handle exceptions properly**
   ```python
   try:
       result = process_data()
   except SpecificError as e:
       logger.error(f"Error: {e}")
       raise HTTPException(status_code=400, detail=str(e))
   ```

3. **Use async where beneficial**
   ```python
   async def get_employees(db: Session):
       # Async database operations
   ```

### Frontend

1. **Use hooks for state management**
   ```typescript
   const [data, setData] = useState<Employee[]>([]);
   const [loading, setLoading] = useState(false);
   ```

2. **Handle loading and error states**
   ```typescript
   if (loading) return <Spinner />;
   if (error) return <ErrorMessage message={error} />;
   ```

3. **Memoize expensive computations**
   ```typescript
   const sortedEmployees = useMemo(
     () => employees.sort((a, b) => a.name.localeCompare(b.name)),
     [employees]
   );
   ```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [InsightFace Documentation](https://github.com/deepinsight/insightface)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Questions?

- Open an issue with the "question" label
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
