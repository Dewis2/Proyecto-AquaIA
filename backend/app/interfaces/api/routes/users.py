from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.auth.security import hash_password
from app.infrastructure.db.models import AuditLogModel, UserModel
from app.interfaces.api.dependencies.auth import require_roles
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.users import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(_: UserModel = Depends(require_roles("administrador")), db: Session = Depends(get_db)):
    return db.query(UserModel).order_by(UserModel.id.desc()).all()


@router.post("", response_model=UserResponse)
def create_user(payload: UserCreate, _: UserModel = Depends(require_roles("administrador")), db: Session = Depends(get_db)):
    exists = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email ya existe")
    user = UserModel(
        nombre=payload.nombre,
        email=payload.email,
        password_hash=hash_password(payload.password),
        rol=payload.rol,
    )
    db.add(user)
    db.flush()
    db.add(AuditLogModel(usuario_id=user.id, accion="CREATE", entidad="usuario", detalle_json=f'{{"id": {user.id}}}'))
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, _: UserModel = Depends(require_roles("administrador")), db: Session = Depends(get_db)):
    user = db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(user, field, value)
    db.add(AuditLogModel(usuario_id=user_id, accion="UPDATE", entidad="usuario", detalle_json=payload.model_dump_json()))
    db.commit()
    db.refresh(user)
    return user
