# Backend AquaIA (PMV1)

API FastAPI para gestión de zonas, sensores, lecturas, alertas y usuarios con JWT.

> Guía completa (incluye PostgreSQL): `../docs/guia-instalacion.md`
> Compatibilidad: Python 3.10+ (incluido 3.14) con dependencias actualizadas.

## 1) Configurar entorno (Windows PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
# Si usas Python 3.14 y falla PyO3/pydantic-core:
$env:PYO3_USE_ABI3_FORWARD_COMPATIBILITY="1"
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
python -m pip install --upgrade pip
# Si usas Python 3.14 y falla PyO3/pydantic-core:
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1
python -m pip install -r requirements.txt
cp .env.example .env
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

> Nota: usar `python -m uvicorn` evita el error de comando no reconocido cuando `uvicorn` no está en PATH.
> Si cambiaste versión de Python, elimina el entorno `.venv` y créalo de nuevo antes de instalar dependencias.
> Si prefieres evitar conflictos de Python local, usa `docker compose up -d db backend` desde la raíz del repo.

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

## Pruebas (paso a paso)

### Paso 0 — activar entorno
Windows:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```
Linux/macOS:
```bash
cd backend
source .venv/bin/activate
```

### Paso 1 — correr todas las pruebas
```bash
python -m pytest app/tests -q
```

### Paso 2 — correr solo pruebas unitarias de reglas
```bash
python -m pytest app/tests/unit/test_anomaly_rules.py -q
```

### Paso 3 — correr integración de alertas (crear + resolver + roles)
```bash
python -m pytest app/tests/integration/test_alert_flow.py -q
```

### Paso 4 — correr integración nueva: 10 alertas distribuidas en el mapa
```bash
python -m pytest app/tests/integration/test_map_alert_distribution.py -q
```

### Paso 5 — correr solo el caso específico de 10 alertas
```bash
python -m pytest app/tests/integration/test_map_alert_distribution.py::test_generate_10_alerts_distributed_across_map_zones -q
```

### ¿Qué valida esta prueba nueva?
1. Crea 5 zonas con coordenadas.
2. Crea 10 sensores distribuidos entre esas zonas.
3. Registra 10 lecturas fuera de umbral.
4. Verifica que se generen exactamente 10 alertas activas.
5. Verifica que esas alertas correspondan a zonas existentes en `/zones` (fuente del mapa).
