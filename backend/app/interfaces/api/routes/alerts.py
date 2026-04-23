from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case
from sqlalchemy.orm import Session
from app.infrastructure.db.models import AlertModel, UserModel
from app.interfaces.api.dependencies.auth import get_current_user, require_roles
from app.interfaces.api.dependencies.db import get_db
from app.interfaces.api.schemas.alerts import AlertResolveRequest, AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
def list_alerts(
    zone_id: int | None = Query(default=None),
    alert_type: str | None = Query(default=None),
    estado: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_roles("operador", "analista", "administrador")),
):
    # Orden de criticidad para priorizar atención en dashboard.
    severity_order = case(
        (AlertModel.nivel == "critica", 4),
        (AlertModel.nivel == "alta", 3),
        (AlertModel.nivel == "media", 2),
        else_=1,
    )
    query = db.query(AlertModel)
    if zone_id:
        query = query.filter(AlertModel.zona_id == zone_id)
    if alert_type:
        query = query.filter(AlertModel.tipo == alert_type)
    if estado:
        query = query.filter(AlertModel.estado == estado)
    return query.order_by(severity_order.desc(), AlertModel.created_at.desc()).all()


@router.post("/{alert_id}/resolve", response_model=AlertResponse)
def resolve_alert(alert_id: int, payload: AlertResolveRequest, db: Session = Depends(get_db), user: UserModel = Depends(get_current_user)):
    # Cierra alerta activa y deja trazabilidad (usuario + timestamp + notas).
    alert = db.get(AlertModel, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    if alert.estado == "resuelta":
        raise HTTPException(status_code=400, detail="Alerta ya resuelta")
    alert.estado = "resuelta"
    alert.resolucion_notas = payload.resolucion_notas
    alert.resuelto_por = user.id
    alert.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert
