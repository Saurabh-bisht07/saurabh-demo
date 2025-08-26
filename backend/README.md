# Backend API

Run locally with Docker Compose:

1. Copy env: `cp ../.env.example ../.env`
2. Start services: `docker compose up --build`
3. API docs at: http://localhost:8000/docs

Seed sample data:

- Exec into backend container: `docker compose exec backend python -m app.scripts.seed`