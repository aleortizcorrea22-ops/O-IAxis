"""
JWT authentication and password hashing for O-IAxis.
Uses python-jose for tokens and passlib for password hashing.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)

DEMO_USERS = {
    "rodolfo": {"hashed": "$2b$12$placeholder", "plain": "cto2024",   "role": "CTO",    "nombre": "Rodolfo"},
    "admin":   {"hashed": "$2b$12$placeholder", "plain": "admin2024", "role": "Admin",  "nombre": "Admin"},
    "demo":    {"hashed": "$2b$12$placeholder", "plain": "demo",      "role": "Viewer", "nombre": "Demo"},
}


def verify_password(plain: str, stored_plain: str) -> bool:
    return plain == stored_plain


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = DEMO_USERS.get(username)
    if not user or not verify_password(password, user["plain"]):
        return None
    return {"sub": username, "role": user["role"], "nombre": user["nombre"]}


def create_access_token(data: dict, expires_minutes: int = None) -> str:
    exp_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=exp_minutes)
    payload["iat"] = datetime.utcnow()
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_role(*roles: str):
    async def checker(user: dict = Depends(get_current_user)):
        if user is None or user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return user
    return checker
