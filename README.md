# TaskForge

A full-stack task and project management app with JWT authentication, 
built to practice real-world backend architecture — auth, protected 
routes, and relational data modeling between users, projects, and tasks.

**Live:** https://task-forge-tech.vercel.app  
**API Docs:** https://taskforge-7mfj.onrender.com/docs

## What it does

Users register, log in, and manage their own projects and tasks. 
Each project can hold multiple tasks. All data is scoped per user — 
you only ever see your own projects and tasks, enforced at the API level 
via JWT.

## Features

- JWT-based authentication (register, login, protected routes)
- Full CRUD on projects and tasks
- User-scoped data isolation
- Interactive Swagger docs for the entire API
- Deployed frontend (Vercel) + backend (Render)

## Tech Stack

**Frontend:** React, Vite  
**Backend:** FastAPI, SQLAlchemy, SQLite, Pydantic  
**Auth:** JWT, Passlib (password hashing)  
**Deployment:** Vercel (frontend), Render (backend)

## Project Structure

TaskForge_API/
├── app/
│   ├── routers/        # users, projects, tasks route handlers
│   ├── auth.py          # JWT logic, password hashing
│   ├── database.py       # DB session + engine setup
│   ├── models.py         # SQLAlchemy models
│   └── schemas.py        # Pydantic request/response models
├── frontend/
└── requirements.txt

## Running Locally

**Backend**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Runs at `http://127.0.0.1:8000` — docs at `/docs`

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:5173`

## Environment Variables

```env
DATABASE_URL=sqlite:///./taskforge.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

**Auth:** `POST /register` · `POST /login` · `GET /me`  
**Projects:** `GET/POST /projects` · `GET/PUT/DELETE /projects/{id}`  
**Tasks:** `GET/POST /projects/{id}/tasks` · `GET/PUT/DELETE /projects/{id}/tasks/{task_id}`

## Next Steps

- Move from SQLite to PostgreSQL for production
- Add task filtering and search
- Password reset flow

## Author

Shardul Kadam  
[LinkedIn] www.linkedin.com/in/shardul-kadam-924a75349 · [GitHub]github.com/shardul778
