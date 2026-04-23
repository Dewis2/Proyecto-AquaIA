from fastapi import APIRouter
from app.interfaces.api.routes import alerts, auth, dashboard, health, readings, sensors, users, zones

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(zones.router)
api_router.include_router(sensors.router)
api_router.include_router(readings.router)
api_router.include_router(alerts.router)
api_router.include_router(dashboard.router)

root_router = APIRouter()
root_router.include_router(health.router)
