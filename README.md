# Blood & Organ Donation Matcher

Stack: FastAPI (Python) + Postgres + React (Vite) + simple ML ranking.

## Quickstart (Docker)

1. Copy env template:

```
cp .env.example .env
```

2. Build and start services:

```
docker compose up --build
```

- API: http://localhost:8000/docs
- Frontend: http://localhost:5173

3. Seed sample donors:

```
docker compose exec backend python -m app.scripts.seed
```

## Configuration

- Edit `.env` for DB/SMTP/Twilio.
- Frontend uses `VITE_API_URL` (set in docker-compose) or defaults to `http://localhost:8000`. 
