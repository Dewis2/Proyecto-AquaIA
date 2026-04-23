from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db.base import Base


class UserModel(Base):
    """Usuario del sistema con rol para control de acceso."""
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(30), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class ZoneModel(Base):
    """Zona geográfica monitoreada (visible en mapa)."""
    __tablename__ = "zona"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitud: Mapped[float] = mapped_column(Float, nullable=False)
    longitud: Mapped[float] = mapped_column(Float, nullable=False)
    poblacion_estimada: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    sensores = relationship("SensorModel", back_populates="zona")


class SensorModel(Base):
    """Sensor IoT asociado a una zona y con umbrales de operación."""
    __tablename__ = "sensor"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    zona_id: Mapped[int] = mapped_column(ForeignKey("zona.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    codigo: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    umbral_min: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    umbral_max: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False)
    fecha_instalacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    zona = relationship("ZoneModel", back_populates="sensores")


class ReadingModel(Base):
    """Lectura temporal de un sensor (serie histórica PMV1)."""
    __tablename__ = "lectura_sensor"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"), nullable=False)
    zona_id: Mapped[int] = mapped_column(ForeignKey("zona.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True)
    valor: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    unidad: Mapped[str] = mapped_column(String(20), nullable=False, default="m3/h")
    score_anomalia: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    es_anomalia: Mapped[bool] = mapped_column(Boolean, default=False)


class AlertModel(Base):
    """Alerta operacional generada por lectura anómala."""
    __tablename__ = "alerta"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"), nullable=False)
    zona_id: Mapped[int] = mapped_column(ForeignKey("zona.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    nivel: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    valor_detectado: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, index=True, default="activa")
    resolucion_notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    resuelto_por: Mapped[int | None] = mapped_column(ForeignKey("usuario.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AuditLogModel(Base):
    """Bitácora mínima de acciones relevantes para trazabilidad."""
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuario.id"), nullable=True)
    accion: Mapped[str] = mapped_column(String(80), nullable=False)
    entidad: Mapped[str] = mapped_column(String(80), nullable=False)
    detalle_json: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
