# Guía de instalación completa (Backend + Frontend + Base de datos)

Esta guía está pensada para levantar AquaIA PMV1 desde cero.

---

## 0) Requisitos previos

- Python 3.10+ (incluye Python 3.14)
- Node.js 18+
- PostgreSQL 14+
- Git

Verifica versiones:

```bash
python --version
node --version
npm --version
psql --version
```

---

## 1) Clonar proyecto

```bash
git clone <URL_DEL_REPO>
cd Proyecto-AquaIA
```

---

## 2) Configurar base de datos PostgreSQL

### 2.1 Crear base de datos y usuario (desde psql)

```sql
CREATE DATABASE aquaia;
CREATE USER aquaia_user WITH PASSWORD 'aquaia_pass';
GRANT ALL PRIVILEGES ON DATABASE aquaia TO aquaia_user;
```

> Si usarás el usuario `postgres`, puedes omitir crear `aquaia_user`.

### 2.2 Cadena de conexión

Usa este formato para `DATABASE_URL`:

```txt
postgresql+psycopg://USUARIO:CLAVE@HOST:PUERTO/BASE
```

Ejemplo:

```txt
postgresql+psycopg://aquaia_user:aquaia_pass@localhost:5432/aquaia
```

---

## 3) Instalar y ejecutar backend

### Windows (PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

Edita `backend/.env` y define tu `DATABASE_URL` real.

Luego:

```powershell
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

Backend disponible en:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

### Linux/macOS

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
```

Edita `backend/.env` y define tu `DATABASE_URL` real.

Luego:

```bash
python -m scripts.seed_data
python -m uvicorn main:app --reload
```

---

## 4) Instalar y ejecutar frontend

En otra terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend disponible en:
- App: http://localhost:3000

---

## 5) Usuarios iniciales (seed)

Después de `python -m scripts.seed_data`:

- Administrador: `admin@aquaia.local` / `Admin123!`
- Operador: `operador@aquaia.local` / `Operador123!`
- Analista: `analista@aquaia.local` / `Analista123!`

---

## 6) Ejecutar pruebas

```bash
cd backend
python -m pytest app/tests -q
```

Pruebas puntuales:

```bash
python -m pytest app/tests/unit/test_anomaly_rules.py -q
python -m pytest app/tests/integration/test_alert_flow.py -q
python -m pytest app/tests/integration/test_map_alert_distribution.py -q
```

---

## 7) Solución rápida de problemas comunes

### Error: `No module named 'app'`
Ejecuta scripts como módulo:

```bash
python -m scripts.seed_data
```

### Error: `uvicorn no se reconoce`
Usa:

```bash
python -m uvicorn main:app --reload
```

### Error PyO3 / binario incompatible en Python 3.14
- Borra y recrea el entorno virtual (no reutilices `.venv` de otra versión de Python).
- Ejecuta `python -m pip install --upgrade pip` antes de instalar requerimientos.
- Reinstala dependencias con `python -m pip install -r requirements.txt`.
- En este proyecto se usa `pbkdf2_sha256` (passlib) para evitar dependencia nativa `bcrypt`.

### Error de conexión a PostgreSQL
- Verifica que el servicio PostgreSQL esté encendido.
- Verifica `DATABASE_URL` en `backend/.env`.
- Prueba conexión con `psql` manualmente.
