"""
Stock Scanner API Endpoints.

Provides endpoints for batch scanning stocks for signals.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel

from core.logging import get_logger
from services.analysis_service import (
    scan_for_signals,
    get_tradeable_tickers,
)

logger = get_logger(__name__)

router = APIRouter(prefix="/v1/scan", tags=["Scanner"])


class SignalResult(BaseModel):
    """Schema for a single signal result."""
    
    ticker: str
    ltp: float
    signal: str
    entry: Optional[float] = None
    stopLoss: Optional[float] = None
    targets: Optional[List[float]] = None
    rsi: Optional[float] = None
    adx: Optional[float] = None
    smc: Optional[str] = None
    trend: Optional[str] = None


class ReversalResult(BaseModel):
    """Schema for a reversal result."""
    
    ticker: str
    ltp: float
    reversal_type: str


class ScanResponse(BaseModel):
    """Response schema for scan endpoints."""
    
    scan_type: str
    stocks_scanned: int
    signals: List[SignalResult]
    scan_duration_ms: float
    scanned_at: str


class FullScanResponse(BaseModel):
    """Response schema for full scan."""
    
    scan_type: str
    stocks_scanned: int
    buy_signals: List[SignalResult]
    sell_signals: List[SignalResult]
    reversals: List[ReversalResult]
    failed_count: int
    scan_duration_ms: float
    scanned_at: str


@router.get("/buy", response_model=ScanResponse)
async def scan_buy_signals(
    tickers: Optional[List[str]] = Query(None, description="Specific tickers to scan"),
    update_convex: bool = Query(True, description="Update Convex with results")
) -> Dict[str, Any]:
    """
    Scan stocks for BUY signals.
    
    Scans all tradeable stocks (or specified tickers) and returns
    those with active BUY signals based on:
    - Price above pivot point
    - Price above VWAP
    - Price above previous day low
    
    Returns:
        List of stocks with BUY signals
    """
    logger.info("Starting BUY signal scan")
    
    try:
        results = await scan_for_signals(
            scan_type="BUY",
            tickers=tickers,
            update_convex=update_convex
        )
        
        return {
            "scan_type": "BUY",
            "stocks_scanned": results["stocks_scanned"],
            "signals": results["buy_signals"],
            "scan_duration_ms": results["scan_duration_ms"],
            "scanned_at": results["scanned_at"],
        }
        
    except Exception as e:
        logger.error(f"BUY scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sell", response_model=ScanResponse)
async def scan_sell_signals(
    tickers: Optional[List[str]] = Query(None, description="Specific tickers to scan"),
    update_convex: bool = Query(True, description="Update Convex with results")
) -> Dict[str, Any]:
    """
    Scan stocks for SELL signals.
    
    Scans all tradeable stocks (or specified tickers) and returns
    those with active SELL signals based on:
    - Price below pivot point
    - Price below VWAP
    - Price below previous day high
    
    Returns:
        List of stocks with SELL signals
    """
    logger.info("Starting SELL signal scan")
    
    try:
        results = await scan_for_signals(
            scan_type="SELL",
            tickers=tickers,
            update_convex=update_convex
        )
        
        return {
            "scan_type": "SELL",
            "stocks_scanned": results["stocks_scanned"],
            "signals": results["sell_signals"],
            "scan_duration_ms": results["scan_duration_ms"],
            "scanned_at": results["scanned_at"],
        }
        
    except Exception as e:
        logger.error(f"SELL scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reversals")
async def scan_reversals(
    tickers: Optional[List[str]] = Query(None, description="Specific tickers to scan"),
    update_convex: bool = Query(True, description="Update Convex with results")
) -> Dict[str, Any]:
    """
    Scan stocks for reversal zones.
    
    Identifies stocks where price has reached the 5th Gann target,
    indicating potential trend reversal:
    - TOP (SELL): Price reached 5th buy target - potential downside
    - BOTTOM (BUY): Price reached 5th sell target - potential upside
    
    Returns:
        List of stocks in reversal zones
    """
    logger.info("Starting reversal scan")
    
    try:
        results = await scan_for_signals(
            scan_type="REVERSAL",
            tickers=tickers,
            update_convex=update_convex
        )
        
        return {
            "scan_type": "REVERSAL",
            "stocks_scanned": results["stocks_scanned"],
            "reversals": results["reversals"],
            "scan_duration_ms": results["scan_duration_ms"],
            "scanned_at": results["scanned_at"],
        }
        
    except Exception as e:
        logger.error(f"Reversal scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/all", response_model=FullScanResponse)
async def run_full_scan(
    tickers: Optional[List[str]] = Query(None, description="Specific tickers to scan"),
    update_convex: bool = Query(True, description="Update Convex with results")
) -> Dict[str, Any]:
    """
    Run complete scan for all signal types.
    
    This is the main endpoint triggered by Convex scheduled functions.
    Scans all stocks and returns:
    - BUY signals
    - SELL signals
    - Reversal zones
    
    Returns:
        Complete scan results
    """
    logger.info("Starting full market scan")
    
    try:
        results = await scan_for_signals(
            scan_type="ALL",
            tickers=tickers,
            update_convex=update_convex
        )
        
        return results
        
    except Exception as e:
        logger.error(f"Full scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger")
async def trigger_background_scan(
    background_tasks: BackgroundTasks,
    update_convex: bool = Query(True)
) -> Dict[str, str]:
    """
    Trigger a background scan without waiting for results.
    
    Useful for webhook triggers from Convex scheduled functions.
    Results will be pushed to Convex when complete.
    
    Returns:
        Acknowledgment that scan started
    """
    async def run_scan():
        try:
            await scan_for_signals(
                scan_type="ALL",
                update_convex=update_convex
            )
            logger.info("Background scan completed")
        except Exception as e:
            logger.error(f"Background scan failed: {e}")
    
    background_tasks.add_task(run_scan)
    
    return {
        "status": "accepted",
        "message": "Scan started in background"
    }


@router.get("/tickers")
async def get_scannable_tickers() -> Dict[str, Any]:
    """
    Get list of tickers that will be scanned.
    
    Returns tradeable stocks (excluding indices like NIFTY).
    
    Returns:
        List of ticker symbols
    """
    tickers = get_tradeable_tickers()
    return {
        "count": len(tickers),
        "tickers": tickers
    }
