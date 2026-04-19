"""Seed inicial para PMV1."""
from datetime import datetime
from app.infrastructure.auth.security import hash_password
from app.infrastructure.db.base import Base
from app.infrastructure.db.models import SensorModel, UserModel, ZoneModel
from app.infrastructure.db.session import SessionLocal, engine

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if not db.query(UserModel).first():
    admin = UserModel(nombre="Admin AquaIA", email="admin@aquaia.local", password_hash=hash_password("Admin123!"), rol="administrador")
    operador = UserModel(nombre="Operador AquaIA", email="operador@aquaia.local", password_hash=hash_password("Operador123!"), rol="operador")
    zone = ZoneModel(nombre="Zona Centro", descripcion="Zona piloto", latitud=-11.1586, longitud=-75.9926, tipo="urbana", activo=True)
    db.add_all([admin, operador, zone])
    db.flush()
    sensor = SensorModel(zona_id=zone.id, tipo="flujo", codigo="SEN-001", umbral_min=20, umbral_max=50, estado="activo", fecha_instalacion=datetime.utcnow())
    db.add(sensor)
    db.commit()
    print("Seed completado")
else:
    print("Seed omitido: ya existen datos")

db.close()
