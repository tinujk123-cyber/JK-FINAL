"""
Market data fetching and caching utilities.

This module handles all interactions with the yfinance API
and implements caching strategies.
"""

import logging
from typing import Optional, Tuple

import pandas as pd
import streamlit as st
import yfinance as yf

from config import CACHE_TTL_SECONDS

# Configure logging
logger = logging.getLogger(__name__)


@st.cache_data(ttl=CACHE_TTL_SECONDS)
def fetch_stock_data(ticker: str) -> Tuple[Optional[float], Optional[pd.DataFrame]]:
    """
    Fetch stock data from Yahoo Finance with caching.
    
    Args:
        ticker: Stock ticker symbol (e.g., "RELIANCE.NS")
    
    Returns:
        Tuple of (last_traded_price, historical_data)
        Returns (None, None) if data fetch fails
    
    Raises:
        Exception: Logs exception but returns None values instead of raising
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y")
        
        if history.empty:
            logger.warning(f"No data available for ticker: {ticker}")
            return None, None
        
        last_price = history['Close'].iloc[-1]
        return last_price, history
        
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return None, None


def clear_cache() -> None:
    """Clear all cached data."""
    st.cache_data.clear()
    logger.info("Cache cleared successfully")


def validate_ticker(ticker: str) -> bool:
    """
    Validate if a ticker symbol is properly formatted.
    
    Args:
        ticker: Ticker symbol to validate
    
    Returns:
        True if ticker appears valid, False otherwise
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    # Basic validation - ticker should be alphanumeric with possible special chars
    return len(ticker) > 0 and len(ticker) < 50


def get_stock_symbol(stock_name: str, stock_dict: dict) -> str:
    """
    Get Yahoo Finance symbol from stock display name.
    
    Args:
        stock_name: Display name of the stock
        stock_dict: Dictionary mapping display names to symbols
    
    Returns:
        Yahoo Finance ticker symbol
    """
    if stock_name in stock_dict:
        return stock_dict[stock_name]
    else:
        # Assume it's a custom symbol, append .NS if not already present
        return stock_name if ".NS" in stock_name else f"{stock_name}.NS"
