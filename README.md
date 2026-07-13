# TaskForge API

Full-stack task and project management app with a FastAPI backend and React frontend.

## Project structure

```
TaskForge_API/
├── app/                 # FastAPI backend
│   ├── routers/         # API route handlers
│   ├── auth.py          # JWT auth helpers
│   ├── config.py        # Environment configuration
│   ├── database.py      # SQLAlchemy setup
│   ├── main.py          # Application entry point
│   ├── models.py        # Database models
│   └── schemas.py       # Pydantic schemas
├── frontend/            # React + Vite frontend
├── requirements.txt     # Python dependencies
```

## Setup

### Backend

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # then edit SECRET_KEY
uvicorn app.main:app --reload
```

API runs at `http://127.0.0.1:8000`.

### Frontend (development)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:5173` and proxies API requests to the backend.

### Production build

```bash
cd frontend
npm run build
```

Then start the API — it serves the built app from `frontend/dist` when present.

## Environment variables

Copy `.env.example` to `.env` in the project root:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | SQLAlchemy database URL |
| `SECRET_KEY` | JWT signing secret (use a strong value in production) |
| `ALGORITHM` | JWT algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes |
