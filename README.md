# Blood & Organ Donation Matcher

A full-stack web app to register donors, search and match nearest compatible donors for patients, and send alerts via email/SMS. Built with React (Vite), FastAPI, and Postgres. Includes a simple Python reliability model.

## Stack
- Backend: FastAPI, SQLAlchemy, Postgres
- Frontend: React + Vite + TypeScript
- ML: Lightweight reliability estimator persisted to file

## Quickstart (without Docker)

Prereqs: Node 18+, Python 3.11+, Postgres 15+

1) Database
- Start Postgres locally and create DB `donation_db` with user/password `donation/donation_password` or set `DATABASE_URL`.

2) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env .env.local 2>/dev/null || true
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The API runs at http://localhost:8000, docs at http://localhost:8000/docs

3) Frontend
```bash
cd frontend
npm install
cp .env.example .env 2>/dev/null || true
npm run dev
```
The app runs at http://localhost:5173

## Docker (compose)
If you have Docker, you can use the provided compose file:
```bash
docker compose -f docker-compose.yml up -d --build
```
Services:
- db: Postgres on 5432
- backend: FastAPI on 8000
- frontend: Vite on 5173

## Key API Endpoints
- POST `/api/donors/` register donor
- GET `/api/matches/search` query by blood group and location
- POST `/api/patients/` create patient request
- POST `/api/notifications/alert/{patient_id}` notify top donors
- POST `/api/ml/train` train reliability model (optional)
- GET `/api/ml/predict` get reliability for all donors

Visit Swagger UI: http://localhost:8000/docs

## Notes
- Email/SMS require environment variables (SMTP or Twilio) in `backend/.env`.
- Reliability model saves to `app/data/reliability_model.pkl` inside backend container.
- Blood compatibility and distance ranking included out of the box. 
