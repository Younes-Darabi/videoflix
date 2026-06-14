# Videoflix Backend

A Netflix-style video streaming backend built with Django REST Framework.

## Features

- User registration with email activation
- JWT authentication via HTTP-only cookies
- Password reset via email
- Video upload via Django Admin
- Automatic HLS conversion (480p, 720p, 1080p) using FFMPEG
- Background task processing with Django RQ
- Redis caching
- PostgreSQL database

## Tech Stack

- Django 6 + Django REST Framework
- PostgreSQL
- Redis + Django RQ
- FFMPEG (HLS streaming)
- Docker + Docker Compose

## Getting Started

### Requirements

- Docker
- Docker Compose

### Setup

1. Clone the repository
2. Copy `.env.template` to `.env` and fill in the values
3. Run:

```bash
docker-compose up --build
```

4. Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| GET | `/api/activate/<uid>/<token>/` | Activate account |
| POST | `/api/login/` | Login |
| POST | `/api/logout/` | Logout |
| POST | `/api/token/refresh/` | Refresh access token |
| POST | `/api/password_reset/` | Request password reset |
| POST | `/api/password_confirm/<uid>/<token>/` | Confirm password reset |

### Video

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/video/` | List all videos |
| GET | `/api/video/<id>/<resolution>/index.m3u8` | HLS manifest |
| GET | `/api/video/<id>/<resolution>/<segment>/` | HLS segment |

## Video Upload

Videos are uploaded exclusively through the Django Admin panel at `/admin/`.  
After upload, FFMPEG automatically converts the video to HLS format in 480p, 720p, and 1080p.

---

Developed with ❤️ by Younes