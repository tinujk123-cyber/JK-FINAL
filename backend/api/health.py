"""
Health Check API Endpoints.

Provides health and status endpoints for monitoring.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns current service status and configuration.
    """
    return {
        "status": "healthy",
        "service": "jk-trinetra-backend",
        "version": "1.0.0",
        "environment": settings.environment,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with dependency status.
    """
    # Check Convex connectivity
    convex_status = "unknown"
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(settings.convex_url)
            convex_status = "healthy" if response.status_code < 500 else "unhealthy"
    except Exception as e:
        convex_status = f"error: {str(e)[:50]}"
    
    return {
        "status": "healthy",
        "service": "jk-trinetra-backend",
        "version": "1.0.0",
        "environment": settings.environment,
        "timestamp": datetime.now().isoformat(),
        "dependencies": {
            "convex": convex_status,
            "yahoo_finance": "available",  # Always available, may be rate limited
        },
        "config": {
            "convex_url": settings.convex_url,
            "cache_ttl": settings.yahoo_cache_ttl_seconds,
        }
    }
