import datetime as dt
import jwt
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from .configs import settings

ALGORITHM = "HS256"

def create_token(payload: dict) -> str:
    exp = dt.datetime.utcnow() + dt.timedelta(hours=settings.JWT_EXPIRY_HOURS)
    data = {**payload, "exp": exp}
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

def hash_password(raw: str) -> str:
    return bcrypt.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return bcrypt.verify(raw, hashed)
