# Utsav Games Backend

Multi-tenant game platform for celebrations and events.

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 14+ (or SQLite for development)
- Virtual environment

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize database:
```bash
alembic upgrade head
```

5. Run development server:
```bash
./run.sh
# Or: uvicorn app.main:app --reload
```

6. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
app/
├── api/          # API endpoints
├── models/       # Database models
├── schemas/      # Pydantic schemas
├── services/     # Business logic
├── utils/        # Utilities
└── websockets/   # WebSocket handlers
```

## Development

### Run tests:
```bash
pytest
```

### Format code:
```bash
black app/
```

### Database migrations:
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Documentation

See [API_DOCS.md](API_DOCS.md) for detailed API specifications.

## License

MIT
