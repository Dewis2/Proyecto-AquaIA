from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.auth.security import create_access_token, verify_password
from app.infrastructure.db.models import UserModel
from app.interfaces.api.dependencies.auth import get_current_user
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.auth import LoginRequest, MeResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    user.ultimo_acceso = datetime.utcnow()
    db.commit()
    return TokenResponse(access_token=create_access_token(str(user.id), user.rol))


@router.get("/me", response_model=MeResponse)
def me(user: UserModel = Depends(get_current_user)):
    return user
