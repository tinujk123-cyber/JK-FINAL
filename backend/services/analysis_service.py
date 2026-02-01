"""
Analysis Service for JK TRINETRA.

Orchestrates stock analysis using existing technical analysis modules
and updates Convex with results.
"""

import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add parent directory to path to import existing modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd

from core.logging import get_logger
from services.convex_client import ConvexClient, get_convex_client

logger = get_logger(__name__)

# Import existing analysis modules from parent directory
try:
    from config import STOCK_SYMBOLS
    from models import (
        MarketTrend,
        MovingAverages,
        PivotPoints,
        PriceData,
        SmartMoneyConceptType,
        TechnicalIndicators,
        TradingPlan,
        TradingSignal,
    )
    from technical_analysis import (
        calculate_all_indicators,
        determine_market_trend,
    )
    from trading_strategy import (
        create_trading_plan,
        extract_price_data,
        generate_trading_signal,
        check_reversal_zone,
    )
except ImportError as e:
    logger.error(f"Failed to import analysis modules: {e}")
    raise


# Cache for Yahoo Finance data (in-memory, per-process)
_data_cache: Dict[str, Tuple[float, pd.DataFrame, float]] = {}
CACHE_TTL_SECONDS = 60


def _get_cached_data(ticker: str) -> Optional[Tuple[float, pd.DataFrame]]:
    """Get cached stock data if fresh."""
    if ticker in _data_cache:
        ltp, data, cached_at = _data_cache[ticker]
        if time.time() - cached_at < CACHE_TTL_SECONDS:
            return ltp, data
    return None


def _cache_data(ticker: str, ltp: float, data: pd.DataFrame) -> None:
    """Cache stock data."""
    _data_cache[ticker] = (ltp, data, time.time())


def fetch_stock_data(ticker: str) -> Tuple[Optional[float], Optional[pd.DataFrame]]:
    """
    Fetch stock data with caching.
    
    Uses the existing data_fetcher module but adds additional caching
    to prevent Yahoo Finance rate limiting.
    """
    # Check cache first
    cached = _get_cached_data(ticker)
    if cached:
        logger.debug(f"Cache hit for {ticker}")
        return cached
    
    # Fetch fresh data
    try:
        import yfinance as yf
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")
        
        if history.empty:
            logger.warning(f"No data available for {ticker}")
            return None, None
        
        ltp = history['Close'].iloc[-1]
        
        # Cache the result
        _cache_data(ticker, ltp, history)
        
        return ltp, history
        
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return None, None


async def analyze_stock(ticker: str, update_convex: bool = True) -> Optional[Dict[str, Any]]:
    """
    Perform complete stock analysis.
    
    Args:
        ticker: Stock ticker symbol (e.g., "RELIANCE.NS")
        update_convex: Whether to update Convex with results
    
    Returns:
        Analysis dictionary or None if analysis fails
    """
    start_time = time.time()
    
    try:
        # Fetch data (runs in thread pool to avoid blocking)
        loop = asyncio.get_event_loop()
        ltp, historical_data = await loop.run_in_executor(
            None, fetch_stock_data, ticker
        )
        
        if ltp is None or historical_data is None:
            logger.warning(f"Could not fetch data for {ticker}")
            return None
        
        # Extract price data
        price_data = extract_price_data(historical_data)
        
        # Calculate technical indicators
        technical_indicators = calculate_all_indicators(historical_data)
        
        # Determine market trend
        trend = determine_market_trend(
            ltp=price_data.ltp,
            sma_50=technical_indicators.moving_averages.sma_50
        )
        
        # Generate trading signal
        signal = generate_trading_signal(
            ltp=price_data.ltp,
            pivot=technical_indicators.pivot_points.pivot,
            vwap=technical_indicators.vwap,
            prev_high=price_data.prev_high,
            prev_low=price_data.prev_low
        )
        
        # Create trading plan
        trading_plan = create_trading_plan(
            signal=signal,
            pivot=technical_indicators.pivot_points.pivot,
            prev_high=price_data.prev_high,
            prev_low=price_data.prev_low
        )
        
        # Build response
        analysis = {
            "symbol": ticker,
            "price_data": {
                "ltp": round(price_data.ltp, 2),
                "today_high": round(price_data.today_high, 2),
                "today_low": round(price_data.today_low, 2),
                "prev_high": round(price_data.prev_high, 2),
                "prev_low": round(price_data.prev_low, 2),
            },
            "indicators": {
                "rsi": round(technical_indicators.rsi, 2),
                "adx": round(technical_indicators.adx, 2),
                "vwap": round(technical_indicators.vwap, 2),
                "smc": technical_indicators.smc.value,
                "pivot_points": {
                    "pivot": round(technical_indicators.pivot_points.pivot, 2),
                    "resistance_1": round(technical_indicators.pivot_points.resistance_1, 2),
                    "resistance_2": round(technical_indicators.pivot_points.resistance_2, 2),
                    "support_1": round(technical_indicators.pivot_points.support_1, 2),
                    "support_2": round(technical_indicators.pivot_points.support_2, 2),
                },
                "moving_averages": {
                    "sma_10": round(technical_indicators.moving_averages.sma_10, 2),
                    "sma_20": round(technical_indicators.moving_averages.sma_20, 2),
                    "sma_50": round(technical_indicators.moving_averages.sma_50, 2),
                    "sma_100": round(technical_indicators.moving_averages.sma_100, 2),
                    "sma_200": round(technical_indicators.moving_averages.sma_200, 2),
                }
            },
            "trading_plan": {
                "signal": trading_plan.signal.value,
                "entry": round(trading_plan.entry, 2),
                "stop_loss": round(trading_plan.stop_loss, 2),
                "targets": [round(t, 2) for t in trading_plan.targets],
            },
            "trend": trend.value,
            "computed_at": datetime.now().isoformat(),
            "computation_time_ms": round((time.time() - start_time) * 1000, 2)
        }
        
        # Update Convex if requested
        if update_convex:
            try:
                client = get_convex_client()
                await client.update_analysis(ticker, analysis)
                logger.info(f"Updated Convex with analysis for {ticker}")
            except Exception as e:
                logger.warning(f"Failed to update Convex for {ticker}: {e}")
                # Continue - analysis is still valid even if Convex update fails
        
        return analysis
        
    except ValueError as e:
        logger.warning(f"Insufficient data for {ticker}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {e}")
        return None


async def scan_for_signals(
    scan_type: str = "ALL",
    tickers: Optional[List[str]] = None,
    update_convex: bool = True
) -> Dict[str, Any]:
    """
    Scan multiple stocks for trading signals.
    
    Args:
        scan_type: Type of scan (BUY, SELL, REVERSAL, ALL)
        tickers: Optional list of tickers to scan (defaults to all stocks)
        update_convex: Whether to update Convex with results
    
    Returns:
        Scan results with buy, sell, and reversal signals
    """
    start_time = time.time()
    
    # Get tickers to scan
    if tickers is None:
        tickers = [
            symbol for name, symbol in STOCK_SYMBOLS.items()
            if not name.endswith("NIFTY")  # Exclude indices
        ]
    
    logger.info(f"Starting {scan_type} scan for {len(tickers)} stocks")
    
    buy_signals = []
    sell_signals = []
    reversals = []
    failed = []
    
    # Process stocks with controlled concurrency
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent
    
    async def analyze_with_semaphore(ticker: str):
        async with semaphore:
            return await analyze_stock(ticker, update_convex=False)
    
    # Run analysis tasks
    tasks = [analyze_with_semaphore(ticker) for ticker in tickers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    for ticker, result in zip(tickers, results):
        if isinstance(result, Exception):
            logger.error(f"Error analyzing {ticker}: {result}")
            failed.append(ticker)
            continue
        
        if result is None:
            failed.append(ticker)
            continue
        
        signal = result["trading_plan"]["signal"]
        
        signal_data = {
            "ticker": ticker,
            "ltp": result["price_data"]["ltp"],
            "signal": signal,
            "entry": result["trading_plan"]["entry"],
            "stopLoss": result["trading_plan"]["stop_loss"],
            "targets": result["trading_plan"]["targets"],
            "rsi": result["indicators"]["rsi"],
            "adx": result["indicators"]["adx"],
            "smc": result["indicators"]["smc"],
            "trend": result["trend"],
        }
        
        if signal == "BUY":
            buy_signals.append(signal_data)
        elif signal == "SELL":
            sell_signals.append(signal_data)
        
        # Check for reversals
        try:
            loop = asyncio.get_event_loop()
            ltp, data = await loop.run_in_executor(None, fetch_stock_data, ticker)
            if ltp and data is not None:
                pivot = result["indicators"]["pivot_points"]["pivot"]
                is_reversal, reversal_type = check_reversal_zone(ltp, pivot)
                if is_reversal:
                    reversals.append({
                        "ticker": ticker,
                        "ltp": ltp,
                        "reversal_type": reversal_type,
                    })
        except Exception as e:
            logger.error(f"Error checking reversal for {ticker}: {e}")
    
    duration_ms = round((time.time() - start_time) * 1000, 2)
    
    scan_results = {
        "scan_type": scan_type,
        "stocks_scanned": len(tickers),
        "buy_signals": buy_signals,
        "sell_signals": sell_signals,
        "reversals": reversals,
        "failed_count": len(failed),
        "scan_duration_ms": duration_ms,
        "scanned_at": datetime.now().isoformat(),
    }
    
    logger.info(
        f"Scan complete: {len(buy_signals)} BUY, {len(sell_signals)} SELL, "
        f"{len(reversals)} reversals in {duration_ms}ms"
    )
    
    # Update Convex if requested
    if update_convex:
        try:
            client = get_convex_client()
            await client.update_scan_results(
                scan_type=scan_type,
                results=buy_signals + sell_signals,
                stocks_scanned=len(tickers),
                duration_ms=int(duration_ms)
            )
            logger.info("Updated Convex with scan results")
        except Exception as e:
            logger.warning(f"Failed to update Convex with scan results: {e}")
    
    return scan_results


def get_all_tickers() -> List[str]:
    """Get all available stock tickers."""
    return list(STOCK_SYMBOLS.values())


def get_tradeable_tickers() -> List[str]:
    """Get tradeable stock tickers (excluding indices)."""
    return [
        symbol for name, symbol in STOCK_SYMBOLS.items()
        if not name.endswith("NIFTY")
    ]
