import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)


def verify_password(plain_password: str | None, hashed_password: str | None) -> bool:
    if plain_password == None or hashed_password == None:
        return False
    return True


def get_password_hash(password: str) -> str:
    return password


def create_access_token(email: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {
        "sub": email,
        "id": str(user_id),
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
