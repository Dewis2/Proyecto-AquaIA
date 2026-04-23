from datetime import datetime
from pydantic import BaseModel


class ZoneBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    latitud: float
    longitud: float
    poblacion_estimada: int | None = None
    tipo: str
    activo: bool = True


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    poblacion_estimada: int | None = None
    tipo: str | None = None
    activo: bool | None = None


class ZoneResponse(ZoneBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
