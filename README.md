# TaskForge

A RESTful task and project management API built with FastAPI, featuring 
JWT authentication and Redis-backed performance and security layers — 
token blacklisting, response caching, and login rate limiting.

**Live:** https://task-forge-tech.vercel.app  
**API Docs:** https://taskforge-7mfj.onrender.com/docs

## Overview

Users register, log in, and manage projects containing tasks — all data 
scoped per user via JWT. On top of standard CRUD, this project adds three 
production-style Redis integrations: blacklisting tokens on logout so they 
can't be reused, caching frequently-requested project/task data, and 
rate-limiting login attempts to prevent brute-force attacks.

## Features

**Authentication** — JWT-based auth, registration, login, logout, 
password hashing (bcrypt), protected routes

**Projects & Tasks** — Full CRUD on both, with tasks scoped to their 
parent project and marked completed/incomplete

**Redis Layer**
- *Token blacklisting* — logout adds the JWT to Redis, so it's rejected 
  on any further use even before it naturally expires
- *Response caching* — project and task list responses are cached with 
  automatic expiration, and invalidated on any create/update/delete
- *Login rate limiting* — tracks failed login attempts per IP and 
  temporarily blocks further attempts after the threshold is hit

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, SQLite  
**Auth:** JWT, Passlib (bcrypt)  
**Caching/Security:** Redis  
**Validation:** Pydantic

## Project Structure
<img width="611" height="305" alt="image" src="https://github.com/user-attachments/assets/e170ae81-3a5e-48c9-85ff-94a1e058246d" />


## Running Locally

```bash
git clone <repo-url>
cd TaskForge
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Runs at `http://127.0.0.1:8000` — docs at `/docs`

## Environment Variables

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USERNAME=default
REDIS_PASSWORD=your_password
```

## API Endpoints

**Auth:** `POST /register` · `POST /login` · `POST /logout` · `GET /me`  
**Projects:** `GET/POST /projects` · `GET/PUT/DELETE /projects/{id}`  
**Tasks:** `GET/POST /projects/{id}/tasks` · `GET/PUT/DELETE /projects/{id}/tasks/{task_id}`

## Next Steps

- Move from SQLite to PostgreSQL for production
- Containerize with Docker + docker-compose (app, DB, Redis)
- Add CI/CD via GitHub Actions

## Author

Shardul Kadam  
[LinkedIn](https://www.linkedin.com/in/shardul-kadam-924a75349) · [GitHub](https://github.com/shardul778)
