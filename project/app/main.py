"""
App Entry Point
"""

from fastapi import FastAPI, Depends
from app.config import get_settings, Settings

app = FastAPI()


@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    """simple endpoint for testing"""
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
