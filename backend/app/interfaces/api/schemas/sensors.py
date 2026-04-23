from datetime import datetime
from pydantic import BaseModel


class SensorCreate(BaseModel):
    zona_id: int
    tipo: str
    codigo: str
    umbral_min: float
    umbral_max: float
    estado: str
    fecha_instalacion: datetime


class SensorUpdate(BaseModel):
    zona_id: int | None = None
    tipo: str | None = None
    umbral_min: float | None = None
    umbral_max: float | None = None
    estado: str | None = None


class SensorResponse(BaseModel):
    id: int
    zona_id: int
    tipo: str
    codigo: str
    umbral_min: float
    umbral_max: float
    estado: str
    fecha_instalacion: datetime
    created_at: datetime

    class Config:
        from_attributes = True
