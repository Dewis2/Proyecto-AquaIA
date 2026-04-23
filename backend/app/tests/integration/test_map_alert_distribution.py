from __future__ import annotations

from datetime import datetime

from fastapi.testclient import TestClient

from app.infrastructure.auth.security import create_access_token
from app.infrastructure.db.base import Base
from app.infrastructure.db.models import SensorModel, UserModel, ZoneModel
from app.infrastructure.db.session import SessionLocal, engine
from app.main import create_app

app = create_app()
client = TestClient(app)


def setup_module() -> None:
    """Prepara una base limpia con zonas/sensores distribuidos."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = UserModel(
            nombre="Admin",
            email="admin-map@test.com",
            password_hash="not-used-in-this-test",
            rol="administrador",
        )
        operador = UserModel(
            nombre="Operador",
            email="operador-map@test.com",
            password_hash="not-used-in-this-test",
            rol="operador",
        )
        db.add_all([admin, operador])
        db.flush()

        zones: list[ZoneModel] = []
        for i in range(1, 6):
            zone = ZoneModel(
                nombre=f"Zona Mapa {i}",
                descripcion="Zona para prueba de distribución",
                latitud=-11.10 - (i * 0.01),
                longitud=-75.90 - (i * 0.01),
                tipo="urbana",
                activo=True,
            )
            zones.append(zone)
        db.add_all(zones)
        db.flush()

        sensors: list[SensorModel] = []
        for i in range(10):
            zone = zones[i % len(zones)]
            sensors.append(
                SensorModel(
                    zona_id=zone.id,
                    tipo="flujo",
                    codigo=f"MAP-SEN-{i+1:03d}",
                    umbral_min=10,
                    umbral_max=20,
                    estado="activo",
                    fecha_instalacion=datetime.utcnow(),
                )
            )
        db.add_all(sensors)
        db.commit()
    finally:
        db.close()


def test_generate_10_alerts_distributed_across_map_zones() -> None:
    # Creamos token de operador sin pasar por login para aislar la prueba
    # de dependencias de hashing del entorno.
    db = SessionLocal()
    try:
        sensors = db.query(SensorModel).order_by(SensorModel.id.asc()).all()
        assert len(sensors) == 10
        sensor_zone_ids = [s.zona_id for s in sensors]
        operador = db.query(UserModel).filter(UserModel.email == "operador-map@test.com").first()
        assert operador is not None
        token = create_access_token(str(operador.id), operador.rol)
    finally:
        db.close()

    headers = {"Authorization": f"Bearer {token}"}

    # Genera 10 lecturas fuera de umbral -> 10 alertas activas.
    for sensor in sensors:
        response = client.post(
            "/api/v1/readings",
            json={"sensor_id": sensor.id, "valor": 35},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["es_anomalia"] is True

    alerts_response = client.get("/api/v1/alerts?estado=activa", headers=headers)
    assert alerts_response.status_code == 200
    alerts = alerts_response.json()
    assert len(alerts) == 10

    # Verifica distribución en zonas (mapa consume /zones + /alerts).
    alert_zone_ids = {a["zona_id"] for a in alerts}
    assert len(alert_zone_ids) >= 5  # una por cada zona creada
    assert set(sensor_zone_ids).issubset(alert_zone_ids)

    zones_response = client.get("/api/v1/zones", headers=headers)
    assert zones_response.status_code == 200
    zones = zones_response.json()
    zone_ids = {z["id"] for z in zones}

    # Todas las alertas corresponden a zonas visibles para el frontend.
    assert alert_zone_ids.issubset(zone_ids)
