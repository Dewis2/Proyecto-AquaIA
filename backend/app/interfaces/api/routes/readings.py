from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.domain.services.anomaly_service import anomaly_score, classify_level
from app.infrastructure.db.models import AlertModel, ReadingModel, SensorModel, UserModel
from app.interfaces.api.dependencies.auth import require_roles
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.readings import ReadingCreate, ReadingResponse

router = APIRouter(prefix="/readings", tags=["readings"])


@router.get("", response_model=list[ReadingResponse])
def list_readings(
    zone_id: int | None = Query(default=None),
    sensor_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_roles("operador", "analista", "administrador")),
):
    query = db.query(ReadingModel).join(SensorModel, SensorModel.id == ReadingModel.sensor_id)
    if zone_id:
        query = query.filter(ReadingModel.zona_id == zone_id)
    if sensor_type:
        query = query.filter(SensorModel.tipo == sensor_type)
    return query.order_by(ReadingModel.timestamp.desc()).limit(200).all()


@router.post("", response_model=ReadingResponse)
def create_reading(payload: ReadingCreate, db: Session = Depends(get_db), _: UserModel = Depends(require_roles("operador", "analista", "administrador"))):
    sensor = db.get(SensorModel, payload.sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    score = anomaly_score(payload.valor, float(sensor.umbral_min), float(sensor.umbral_max))
    is_anomaly = score > 0
    reading = ReadingModel(
        sensor_id=sensor.id,
        zona_id=sensor.zona_id,
        valor=payload.valor,
        unidad=payload.unidad,
        timestamp=payload.timestamp or datetime.utcnow(),
        score_anomalia=score,
        es_anomalia=is_anomaly,
    )
    db.add(reading)
    db.flush()
    if is_anomaly:
        level = classify_level(score).value
        alert = AlertModel(
            sensor_id=sensor.id,
            zona_id=sensor.zona_id,
            tipo="umbral_fuera_rango",
            nivel=level,
            valor_detectado=payload.valor,
            descripcion=f"Valor fuera de umbral ({sensor.umbral_min}-{sensor.umbral_max})",
            estado="activa",
        )
        db.add(alert)
    db.commit()
    db.refresh(reading)
    return reading


@router.post("/simulate")
def simulate_readings(db: Session = Depends(get_db), _: UserModel = Depends(require_roles("administrador"))):
    sensors = db.query(SensorModel).all()
    if not sensors:
        raise HTTPException(status_code=400, detail="No hay sensores para simular")
    generated = 0
    now = datetime.utcnow()
    for sensor in sensors:
        base = (float(sensor.umbral_min) + float(sensor.umbral_max)) / 2
        for offset in range(3):
            value = base + ((-1) ** offset) * (offset * 0.2)
            if offset == 2:
                value = float(sensor.umbral_max) * 1.4
            create_payload = ReadingCreate(sensor_id=sensor.id, valor=value, timestamp=now - timedelta(seconds=offset * 20))
            create_reading(create_payload, db, _)
            generated += 1
    return {"generated_readings": generated}
