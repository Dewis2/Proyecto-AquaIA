from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.models import AuditLogModel, SensorModel, UserModel, ZoneModel
from app.interfaces.api.dependencies.auth import require_roles
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.sensors import SensorCreate, SensorResponse, SensorUpdate

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.get("", response_model=list[SensorResponse])
def list_sensors(db: Session = Depends(get_db), _: UserModel = Depends(require_roles("operador", "analista", "administrador"))):
    return db.query(SensorModel).order_by(SensorModel.id.desc()).all()


@router.post("", response_model=SensorResponse)
def create_sensor(payload: SensorCreate, db: Session = Depends(get_db), user: UserModel = Depends(require_roles("administrador"))):
    zone = db.get(ZoneModel, payload.zona_id)
    if not zone:
        raise HTTPException(status_code=400, detail="Zona no existe")
    sensor = SensorModel(**payload.model_dump())
    db.add(sensor)
    db.flush()
    db.add(AuditLogModel(usuario_id=user.id, accion="CREATE", entidad="sensor", detalle_json=payload.model_dump_json()))
    db.commit()
    db.refresh(sensor)
    return sensor


@router.patch("/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: int, payload: SensorUpdate, db: Session = Depends(get_db), user: UserModel = Depends(require_roles("administrador"))):
    sensor = db.get(SensorModel, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    if payload.zona_id:
        zone = db.get(ZoneModel, payload.zona_id)
        if not zone:
            raise HTTPException(status_code=400, detail="Zona no existe")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(sensor, field, value)
    db.add(AuditLogModel(usuario_id=user.id, accion="UPDATE", entidad="sensor", detalle_json=payload.model_dump_json()))
    db.commit()
    db.refresh(sensor)
    return sensor


@router.delete("/{sensor_id}")
def delete_sensor(sensor_id: int, db: Session = Depends(get_db), user: UserModel = Depends(require_roles("administrador"))):
    sensor = db.get(SensorModel, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    db.delete(sensor)
    db.add(AuditLogModel(usuario_id=user.id, accion="DELETE", entidad="sensor", detalle_json=f'{{"id": {sensor_id}}}'))
    db.commit()
    return {"message": "Sensor eliminado"}
