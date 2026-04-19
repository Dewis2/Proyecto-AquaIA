from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.infrastructure.db.models import AlertModel, ReadingModel, SensorModel, ZoneModel, UserModel
from app.interfaces.api.dependencies.auth import require_roles
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db), _: UserModel = Depends(require_roles("operador", "analista", "administrador"))):
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    return DashboardSummary(
        active_alerts=db.query(func.count(AlertModel.id)).filter(AlertModel.estado == "activa").scalar() or 0,
        critical_alerts=db.query(func.count(AlertModel.id)).filter(AlertModel.estado == "activa", AlertModel.nivel == "critica").scalar() or 0,
        total_sensors=db.query(func.count(SensorModel.id)).scalar() or 0,
        active_sensors=db.query(func.count(SensorModel.id)).filter(SensorModel.estado == "activo").scalar() or 0,
        zones_count=db.query(func.count(ZoneModel.id)).scalar() or 0,
        last_hour_readings=db.query(func.count(ReadingModel.id)).filter(ReadingModel.timestamp >= one_hour_ago).scalar() or 0,
    )
