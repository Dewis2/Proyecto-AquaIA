from datetime import datetime
from pydantic import BaseModel, Field


class AlertResolveRequest(BaseModel):
    resolucion_notas: str = Field(min_length=5)


class AlertResponse(BaseModel):
    id: int
    sensor_id: int
    zona_id: int
    tipo: str
    nivel: str
    valor_detectado: float
    descripcion: str
    estado: str
    resolucion_notas: str | None = None
    resuelto_por: int | None = None
    created_at: datetime
    resolved_at: datetime | None = None

    class Config:
        from_attributes = True
