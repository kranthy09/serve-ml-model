"""
APIRouter for /ping route.
"""

from fastapi import APIRouter, Depends

from app.config import get_settings, Settings

router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    """Simple ping endpoint for testing"""
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
