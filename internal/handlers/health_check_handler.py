from internal.domain.user import HealthCheck
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/health", response_model = HealthCheck)
async def health_check():
    """Health check endpoint"""
    import datetime
    health = HealthCheck(
        status="ok",
        timestamp=datetime.datetime.utcnow().isoformat() + "Z"
    )

    try:
        health.database = "healthly"
    except Exception:
        health.database = "unhealthly"
        health.status = "degreaded"

    return health

@router.get("/ready")
async def readness_check():
    """readiness probe"""

@router.get("/live")
async def liveness_check():
    """liveness probe"""