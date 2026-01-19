"""
Stock scanner module for batch analysis.

This module provides scanning functionality to find stocks
matching specific criteria (buy signals, sell signals, reversals).
"""

import logging
from typing import List

from analyzer import analyze_stock_legacy
from config import STOCK_SYMBOLS
from data_fetcher import fetch_stock_data
from models import ReversalSignal
from trading_strategy import check_reversal_zone

logger = logging.getLogger(__name__)


def get_tradeable_stocks() -> List[str]:
    """
    Get list of tradeable stock symbols (excluding indices).
    
    Returns:
        List of stock ticker symbols
    """
    return [
        symbol for name, symbol in STOCK_SYMBOLS.items()
        if not name.endswith("NIFTY")
    ]


def scan_for_buy_signals() -> List[dict]:
    """
    Scan all stocks for buy signals.
    
    Returns:
        List of dictionaries containing stocks with buy signals
    """
    buy_signals = []
    tradeable_stocks = get_tradeable_stocks()
    
    logger.info(f"Scanning {len(tradeable_stocks)} stocks for buy signals...")
    
    for ticker in tradeable_stocks:
        try:
            analysis = analyze_stock_legacy(ticker)
            
            if analysis and analysis["Signal"] == "BUY":
                buy_signals.append(analysis)
                logger.debug(f"Buy signal found: {ticker}")
                
        except Exception as e:
            logger.error(f"Error scanning {ticker}: {str(e)}")
            continue
    
    logger.info(f"Found {len(buy_signals)} buy signals")
    return buy_signals


def scan_for_sell_signals() -> List[dict]:
    """
    Scan all stocks for sell signals.
    
    Returns:
        List of dictionaries containing stocks with sell signals
    """
    sell_signals = []
    tradeable_stocks = get_tradeable_stocks()
    
    logger.info(f"Scanning {len(tradeable_stocks)} stocks for sell signals...")
    
    for ticker in tradeable_stocks:
        try:
            analysis = analyze_stock_legacy(ticker)
            
            if analysis and analysis["Signal"] == "SELL":
                sell_signals.append(analysis)
                logger.debug(f"Sell signal found: {ticker}")
                
        except Exception as e:
            logger.error(f"Error scanning {ticker}: {str(e)}")
            continue
    
    logger.info(f"Found {len(sell_signals)} sell signals")
    return sell_signals


def scan_for_reversals() -> List[dict]:
    """
    Scan all stocks for reversal zones (price reached 5th target).
    
    Returns:
        List of dictionaries containing stocks in reversal zones
    """
    reversals = []
    tradeable_stocks = get_tradeable_stocks()
    
    logger.info(f"Scanning {len(tradeable_stocks)} stocks for reversals...")
    
    for ticker in tradeable_stocks:
        try:
            ltp, historical_data = fetch_stock_data(ticker)
            
            if ltp is None or historical_data is None:
                continue
            
            # Calculate pivot from previous day
            prev_day = historical_data.iloc[-2]
            pivot = (prev_day['High'] + prev_day['Low'] + prev_day['Close']) / 3
            
            # Check if in reversal zone
            is_reversal, reversal_type = check_reversal_zone(ltp, pivot)
            
            if is_reversal:
                reversals.append({
                    "Symbol": ticker,
                    "LTP": ltp,
                    "Type": reversal_type
                })
                logger.debug(f"Reversal found: {ticker} - {reversal_type}")
                
        except Exception as e:
            logger.error(f"Error scanning {ticker} for reversals: {str(e)}")
            continue
    
    logger.info(f"Found {len(reversals)} reversals")
    return reversals
