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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin = UserModel(
            nombre="Admin",
            email="admin@test.com",
            password_hash="not-used-in-this-test",
            rol="administrador",
        )
        operador = UserModel(
            nombre="Op",
            email="op@test.com",
            password_hash="not-used-in-this-test",
            rol="operador",
        )
        zone = ZoneModel(nombre="Zona Test", latitud=-11.1, longitud=-75.9, tipo="urbana", activo=True)
        db.add_all([admin, operador, zone])
        db.flush()
        sensor = SensorModel(
            zona_id=zone.id,
            tipo="flujo",
            codigo="S-T1",
            umbral_min=10,
            umbral_max=20,
            estado="activo",
            fecha_instalacion=datetime.utcnow(),
        )
        db.add(sensor)
        db.commit()
    finally:
        db.close()


def _token_for(email: str) -> str:
    db = SessionLocal()
    try:
        user = db.query(UserModel).filter(UserModel.email == email).first()
        assert user is not None
        return create_access_token(str(user.id), user.rol)
    finally:
        db.close()


def test_generate_alert_and_resolve_with_notes() -> None:
    token = _token_for("op@test.com")
    headers = {"Authorization": f"Bearer {token}"}

    read_res = client.post("/api/v1/readings", json={"sensor_id": 1, "valor": 35}, headers=headers)
    assert read_res.status_code == 200

    alerts = client.get("/api/v1/alerts?estado=activa", headers=headers)
    assert alerts.status_code == 200
    assert len(alerts.json()) >= 1
    alert_id = alerts.json()[0]["id"]

    bad_resolve = client.post(
        f"/api/v1/alerts/{alert_id}/resolve",
        json={"resolucion_notas": "ok"},
        headers=headers,
    )
    assert bad_resolve.status_code == 422

    good_resolve = client.post(
        f"/api/v1/alerts/{alert_id}/resolve",
        json={"resolucion_notas": "Se cerró válvula y se calibró sensor."},
        headers=headers,
    )
    assert good_resolve.status_code == 200
    assert good_resolve.json()["estado"] == "resuelta"


def test_role_protection_users_endpoint() -> None:
    token_op = _token_for("op@test.com")
    op_headers = {"Authorization": f"Bearer {token_op}"}
    forbidden = client.get("/api/v1/users", headers=op_headers)
    assert forbidden.status_code == 403
