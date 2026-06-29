"""
Auth endpoints — /api/v1/auth/token (login) and /api/v1/auth/me
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.security import authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    nombre: str


@router.post("/token", response_model=TokenResponse)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token(user)
    return TokenResponse(
        access_token=token,
        role=user["role"],
        nombre=user["nombre"],
    )


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="No autenticado")
    return current_user
