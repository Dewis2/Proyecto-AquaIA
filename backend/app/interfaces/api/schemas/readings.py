from datetime import datetime
from pydantic import BaseModel


class ReadingCreate(BaseModel):
    sensor_id: int
    valor: float
    unidad: str = "m3/h"
    timestamp: datetime | None = None


class ReadingResponse(BaseModel):
    id: int
    sensor_id: int
    zona_id: int
    timestamp: datetime
    valor: float
    unidad: str
    score_anomalia: float
    es_anomalia: bool

    class Config:
        from_attributes = True
