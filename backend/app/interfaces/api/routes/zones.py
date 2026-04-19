from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.models import AuditLogModel, ZoneModel, UserModel
from app.interfaces.api.dependencies.auth import require_roles
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.zones import ZoneCreate, ZoneResponse, ZoneUpdate

router = APIRouter(prefix="/zones", tags=["zones"])


@router.get("", response_model=list[ZoneResponse])
def list_zones(db: Session = Depends(get_db), _: UserModel = Depends(require_roles("operador", "analista", "administrador"))):
    return db.query(ZoneModel).order_by(ZoneModel.id.desc()).all()


@router.post("", response_model=ZoneResponse)
def create_zone(payload: ZoneCreate, db: Session = Depends(get_db), user: UserModel = Depends(require_roles("administrador"))):
    zone = ZoneModel(**payload.model_dump())
    db.add(zone)
    db.flush()
    db.add(AuditLogModel(usuario_id=user.id, accion="CREATE", entidad="zona", detalle_json=payload.model_dump_json()))
    db.commit()
    db.refresh(zone)
    return zone


@router.patch("/{zone_id}", response_model=ZoneResponse)
def update_zone(zone_id: int, payload: ZoneUpdate, db: Session = Depends(get_db), user: UserModel = Depends(require_roles("administrador"))):
    zone = db.get(ZoneModel, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(zone, field, value)
    db.add(AuditLogModel(usuario_id=user.id, accion="UPDATE", entidad="zona", detalle_json=payload.model_dump_json()))
    db.commit()
    db.refresh(zone)
    return zone


@router.delete("/{zone_id}")
def delete_zone(zone_id: int, db: Session = Depends(get_db), user: UserModel = Depends(require_roles("administrador"))):
    zone = db.get(ZoneModel, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zona no encontrada")
    db.delete(zone)
    db.add(AuditLogModel(usuario_id=user.id, accion="DELETE", entidad="zona", detalle_json=f'{{"id": {zone_id}}}'))
    db.commit()
    return {"message": "Zona eliminada"}
