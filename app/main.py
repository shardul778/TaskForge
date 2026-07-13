from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import app.models  # noqa: F401 — creates DB tables on startup

_root = Path(__file__).resolve().parent.parent

from app.routers import users, projects, task

app = FastAPI(title="TaskForge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://task-forge-ashy-mu.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["Users"])
app.include_router(projects.router, tags=["Projects"])
app.include_router(task.router, tags=["Tasks"])

_dist_dir = _root / "frontend" / "dist"
_assets_dir = _dist_dir / "assets"

if _dist_dir.is_dir() and (_dist_dir / "index.html").is_file():
    if _assets_dir.is_dir():
        app.mount(
            "/assets",
            StaticFiles(directory=str(_assets_dir)),
            name="frontend_assets",
        )

    @app.get("/")
    def serve_frontend_root():
        return FileResponse(str(_dist_dir / "index.html"))

    @app.get("/{full_path:path}")
    def serve_frontend_routes(full_path: str):
        file_path = _dist_dir / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(_dist_dir / "index.html"))
