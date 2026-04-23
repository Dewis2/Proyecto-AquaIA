"""Generación simple de lecturas PMV1."""
from datetime import datetime
from app.domain.services.anomaly_service import anomaly_score, classify_level
from app.infrastructure.db.models import AlertModel, ReadingModel, SensorModel
from app.infrastructure.db.session import SessionLocal


def run() -> None:
    db = SessionLocal()
    sensors = db.query(SensorModel).all()
    generated = 0
    for sensor in sensors:
        value = float(sensor.umbral_max) * 1.2
        score = anomaly_score(value, float(sensor.umbral_min), float(sensor.umbral_max))
        reading = ReadingModel(sensor_id=sensor.id, zona_id=sensor.zona_id, valor=value, unidad="m3/h", timestamp=datetime.utcnow(), score_anomalia=score, es_anomalia=score > 0)
        db.add(reading)
        if score > 0:
            db.add(AlertModel(sensor_id=sensor.id, zona_id=sensor.zona_id, tipo="umbral_fuera_rango", nivel=classify_level(score).value, valor_detectado=value, descripcion="Lectura simulada fuera de rango", estado="activa"))
        generated += 1
    db.commit()
    db.close()
    print(f"Lecturas generadas: {generated}")


if __name__ == "__main__":
    run()
