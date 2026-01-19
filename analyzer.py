"""
Stock analysis orchestration module.

This module combines data fetching, technical analysis, and trading strategy
to provide complete stock analysis.
"""

import logging
from typing import Optional

import pandas as pd

from data_fetcher import fetch_stock_data
from models import StockAnalysis
from technical_analysis import calculate_all_indicators, determine_market_trend
from trading_strategy import (
    create_trading_plan,
    extract_price_data,
    generate_trading_signal,
)

logger = logging.getLogger(__name__)


def analyze_stock(ticker: str) -> Optional[StockAnalysis]:
    """
    Perform complete analysis on a stock.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        StockAnalysis object with complete analysis, or None if analysis fails
    """
    try:
        # Fetch data
        ltp, historical_data = fetch_stock_data(ticker)
        
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
        
        # Combine into complete analysis
        analysis = StockAnalysis(
            symbol=ticker,
            price_data=price_data,
            technical_indicators=technical_indicators,
            trading_plan=trading_plan,
            trend=trend
        )
        
        return analysis
        
    except ValueError as e:
        logger.warning(f"Insufficient data for {ticker}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {str(e)}")
        return None


def analyze_stock_legacy(ticker: str) -> Optional[dict]:
    """
    Perform stock analysis and return in legacy dictionary format.
    
    This function maintains backward compatibility with the old code.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        Dictionary with analysis results, or None if analysis fails
    """
    analysis = analyze_stock(ticker)
    
    if analysis is None:
        return None
    
    return analysis.to_dict()
