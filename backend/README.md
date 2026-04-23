# Backend AquaIA (PMV1)

API FastAPI para gestión de zonas, sensores, lecturas, alertas y usuarios con JWT.

## Ejecutar

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/seed_data.py
uvicorn main:app --reload
```

## Endpoints PMV1
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `CRUD /api/v1/users`
- `CRUD /api/v1/zones`
- `CRUD /api/v1/sensors`
- `GET|POST /api/v1/readings`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/{id}/resolve`
- `GET /api/v1/dashboard/summary`
- `GET /health`

## Simulación
- `python scripts/simulate_readings.py`
- o `POST /api/v1/readings/simulate` (admin)

## Pruebas
```bash
pytest app/tests -q
```
