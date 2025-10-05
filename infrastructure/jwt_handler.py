from datetime import datetime, timedelta, UTC
from jose import  jwt, JWTError
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("API_SECRET_KEY", "fastkit-secretkey")
REFRESH_SECRET_KEY = os.getenv("API_REFRESH_SECRET_KEY", "astkit-refresh-secretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("API_ACCESS_TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("API_REFRESH_TOKEN_EXPIRE_DAYS", 7)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
