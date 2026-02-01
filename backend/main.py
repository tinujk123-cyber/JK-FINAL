"""
JK TRINETRA FastAPI Backend.

Main application entry point that configures and runs the FastAPI server.
Provides stock analysis and scanning endpoints with Convex integration.
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path for importing existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.health import router as health_router
from api.analyze import router as analyze_router
from api.scan import router as scan_router
from core.config import settings
from core.logging import setup_logging, get_logger
from services.convex_client import close_convex_client

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting JK TRINETRA Backend", extra={
        "environment": settings.environment,
        "convex_url": settings.convex_url,
    })
    
    yield
    
    # Shutdown
    logger.info("Shutting down JK TRINETRA Backend")
    await close_convex_client()


# Create FastAPI application
app = FastAPI(
    title="JK TRINETRA Backend",
    description="""
    AI-Powered Stock Analysis Backend for Indian NSE Markets.
    
    ## Features
    
    * **Stock Analysis**: Complete technical analysis with RSI, ADX, SMA, Pivots, Gann levels
    * **Signal Generation**: BUY/SELL/WAIT signals based on price action
    * **Batch Scanning**: Scan 80+ stocks for trading opportunities
    * **Reversal Detection**: Identify stocks at potential reversal points
    * **Convex Integration**: Real-time updates to connected clients
    
    ## Endpoints
    
    * `/health` - Health check
    * `/v1/analyze/{ticker}` - Analyze single stock
    * `/v1/scan/buy` - Scan for BUY signals
    * `/v1/scan/sell` - Scan for SELL signals
    * `/v1/scan/reversals` - Scan for reversal zones
    * `/v1/scan/all` - Run complete market scan
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(scan_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "JK TRINETRA Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
