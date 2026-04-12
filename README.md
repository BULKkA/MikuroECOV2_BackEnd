# Mikuro Blog Backend

FastAPI backend for Mikuro blog with PostgreSQL database.

## Features

- User authentication and authorization (JWT)
- Role-based access control (user, editor, admin)
- Blog posts with markdown support
- Comments system
- Reactions (like, love, dislike)
- Media upload
- Captcha verification

## Setup

1. Start PostgreSQL database:
```bash
docker compose up -d
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit http://localhost:8000/docs for interactive API documentation.

## Environment Variables

Copy `.env` file and adjust settings as needed:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `MEDIA_UPLOAD_PATH`: Path for uploaded files
- `MAX_FILE_SIZE`: Maximum file size for uploads
- `ALLOWED_MIME_TYPES`: List of allowed MIME types

## Docker

Build and run with Docker:

```bash
docker build -t mikuro-backend .
docker run -p 8000:8000 --env-file .env mikuro-backend
```