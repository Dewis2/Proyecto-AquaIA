from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.settings.config import get_settings
from app.interfaces.api.router import api_router, root_router


def create_app() -> FastAPI:
    # Carga configuración centralizada (env, JWT, CORS, etc.)
    settings = get_settings()
    # Inicializa la app FastAPI para PMV1
    app = FastAPI(title=settings.app_name, version="1.0.0")

    # Política CORS para permitir que el frontend consuma la API en desarrollo
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # En PMV1 creamos tablas automáticamente si no existen.
    # (En producción se recomienda migraciones formales con Alembic.)
    Base.metadata.create_all(bind=engine)
    # Rutas base (/health) y rutas versionadas (/api/v1/...)
    app.include_router(root_router)
    app.include_router(api_router)
    return app
