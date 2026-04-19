from datetime import datetime
from fastapi import APIRouter
from app.interfaces.api.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", service="aquaia-pmv1-backend", timestamp=datetime.utcnow())
