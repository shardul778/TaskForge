import os
from pathlib import Path

from dotenv import load_dotenv

_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskforge.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your_super_secret_key_here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
Redis_host = os.getenv("REDIS_HOST")
Redis_username = os.getenv("REDIS_USERNAME")
Redis_password = os.getenv("REDIS_PASSWORD")