from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.infrastructure.settings.config import get_settings
from app.interfaces.api.router import api_router, root_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)
    app.include_router(root_router)
    app.include_router(api_router)
    return app
