"""Seed inicial para PMV1.

Soporta ejecución de estas dos formas:
- python scripts/seed_data.py
- python -m scripts.seed_data
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

# Permite import absoluto `app.*` cuando se ejecuta como script en Windows/Linux
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.infrastructure.auth.security import hash_password
from app.infrastructure.db.base import Base
from app.infrastructure.db.models import SensorModel, UserModel, ZoneModel
from app.infrastructure.db.session import SessionLocal, engine


def run_seed() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not db.query(UserModel).first():
            admin = UserModel(
                nombre="Admin AquaIA",
                email="admin@aquaia.local",
                password_hash=hash_password("Admin123!"),
                rol="administrador",
            )
            operador = UserModel(
                nombre="Operador AquaIA",
                email="operador@aquaia.local",
                password_hash=hash_password("Operador123!"),
                rol="operador",
            )
            analista = UserModel(
                nombre="Analista AquaIA",
                email="analista@aquaia.local",
                password_hash=hash_password("Analista123!"),
                rol="analista",
            )
            zone = ZoneModel(
                nombre="Zona Centro",
                descripcion="Zona piloto",
                latitud=-11.1586,
                longitud=-75.9926,
                tipo="urbana",
                activo=True,
            )
            db.add_all([admin, operador, analista, zone])
            db.flush()

            sensor = SensorModel(
                zona_id=zone.id,
                tipo="flujo",
                codigo="SEN-001",
                umbral_min=20,
                umbral_max=50,
                estado="activo",
                fecha_instalacion=datetime.utcnow(),
            )
            db.add(sensor)
            db.commit()
            print("Seed completado: admin, operador, analista, 1 zona y 1 sensor.")
        else:
            print("Seed omitido: ya existen datos.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
