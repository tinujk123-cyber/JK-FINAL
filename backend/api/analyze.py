"""
Stock Analysis API Endpoints.

Provides endpoints for analyzing individual stocks.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from core.logging import get_logger
from services.analysis_service import analyze_stock, get_all_tickers

logger = get_logger(__name__)

router = APIRouter(prefix="/v1/analyze", tags=["Analysis"])


class AnalysisResponse(BaseModel):
    """Response schema for stock analysis."""
    
    symbol: str
    price_data: Dict[str, float]
    indicators: Dict[str, Any]
    trading_plan: Dict[str, Any]
    trend: str
    computed_at: str
    computation_time_ms: float


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str
    detail: Optional[str] = None


@router.get(
    "/{ticker}",
    response_model=AnalysisResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Stock not found"},
        500: {"model": ErrorResponse, "description": "Analysis failed"},
    }
)
async def get_stock_analysis(
    ticker: str,
    force_refresh: bool = Query(
        False,
        description="Force refresh even if cached data exists"
    ),
    update_convex: bool = Query(
        True,
        description="Update Convex with analysis results"
    )
) -> Dict[str, Any]:
    """
    Analyze a single stock.
    
    Performs complete technical analysis including:
    - Price data (LTP, today's range, previous day range)
    - Technical indicators (RSI, ADX, VWAP, SMC)
    - Pivot points (S1, S2, R1, R2)
    - Moving averages (10, 20, 50, 100, 200 SMA)
    - Trading plan (signal, entry, stop loss, 5 targets)
    
    Args:
        ticker: Stock ticker symbol (e.g., "RELIANCE.NS")
        force_refresh: Force fresh data fetch from Yahoo Finance
        update_convex: Whether to store results in Convex
    
    Returns:
        Complete stock analysis
    
    Raises:
        404: If stock data not available
        500: If analysis fails
    """
    # Normalize ticker
    normalized_ticker = ticker.upper()
    
    # Add .NS suffix if not present (for NSE stocks)
    if not normalized_ticker.endswith(".NS") and not normalized_ticker.startswith("^"):
        normalized_ticker = f"{normalized_ticker}.NS"
    
    logger.info(f"Analyzing stock: {normalized_ticker}")
    
    try:
        analysis = await analyze_stock(
            ticker=normalized_ticker,
            update_convex=update_convex
        )
        
        if analysis is None:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {normalized_ticker}"
            )
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed for {normalized_ticker}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/tickers/all")
async def list_all_tickers() -> Dict[str, Any]:
    """
    List all available stock tickers.
    
    Returns:
        List of all configured stock ticker symbols
    """
    tickers = get_all_tickers()
    return {
        "count": len(tickers),
        "tickers": tickers
    }


@router.post("/batch")
async def batch_analyze(
    tickers: list[str],
    update_convex: bool = Query(True)
) -> Dict[str, Any]:
    """
    Analyze multiple stocks in batch.
    
    Args:
        tickers: List of ticker symbols to analyze
        update_convex: Whether to store results in Convex
    
    Returns:
        Analysis results for all stocks
    """
    if len(tickers) > 20:
        raise HTTPException(
            status_code=400,
            detail="Maximum 20 tickers per batch request"
        )
    
    results = {}
    failed = []
    
    for ticker in tickers:
        try:
            analysis = await analyze_stock(
                ticker=ticker.upper(),
                update_convex=update_convex
            )
            if analysis:
                results[ticker] = analysis
            else:
                failed.append(ticker)
        except Exception as e:
            logger.error(f"Batch analysis failed for {ticker}: {e}")
            failed.append(ticker)
    
    return {
        "success_count": len(results),
        "failed_count": len(failed),
        "failed_tickers": failed,
        "results": results
    }
