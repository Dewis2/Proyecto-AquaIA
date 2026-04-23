# AquaIA — PMV1

Entrega académica enfocada **solo en PMV1**: monitoreo de consumo por zona, alertas automáticas, CRUD de zonas/sensores/usuarios, dashboard básico, autenticación JWT y trazabilidad de alertas.

## Estructura
- `backend/`: FastAPI + SQLAlchemy con separación por capas (domain/application/infrastructure/interfaces).
- `frontend/`: Next.js (App Router), módulos por dominio (`dashboard`, `alerts`, `zones`, `sensors`, `auth`).
- `docs/pmv1/`: alcance, backlog, trazabilidad y decisiones técnicas.

## Levantar entorno

## Guía de instalación detallada
- Revisa `docs/guia-instalacion.md` para setup completo de backend, frontend y PostgreSQL.


### Backend (Windows PowerShell)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

### Backend (Linux/macOS)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## PMV1 cubre
- HU-01, HU-02, HU-03, HU-09, HU-10, HU-12, HU-14.
- RF-01, RF-04, RF-05, RF-06, RF-07, RF-08, RF-09, RF-12.

## PMV1 NO cubre
Predicción de demanda (LSTM/Prophet/XGBoost), optimización de rutas VRP, simulación avanzada, reportes PDF/Excel, reentrenamiento automático.
