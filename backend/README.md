# Backend AquaIA (PMV1)

API FastAPI para gestión de zonas, sensores, lecturas, alertas y usuarios con JWT.

## 1) Configurar entorno (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

## 2) Configurar entorno (Linux/macOS)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

> Nota: usar `python -m uvicorn` evita el error de comando no reconocido cuando `uvicorn` no está en PATH.

## Usuarios seed por defecto
- Administrador: `admin@aquaia.local` / `Admin123!`
- Operador: `operador@aquaia.local` / `Operador123!`
- Analista: `analista@aquaia.local` / `Analista123!`

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
- `python -m scripts.simulate_readings`
- o `POST /api/v1/readings/simulate` (admin)

## Pruebas
```bash
pytest app/tests -q
```
