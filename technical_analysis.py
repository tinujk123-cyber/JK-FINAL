"""
Technical analysis calculations module.

This module contains all technical indicator calculations including
RSI, ADX, Moving Averages, Pivot Points, and Smart Money Concepts.
"""

import logging
from typing import Tuple

import pandas as pd

from config import (
    ADX_PERIOD,
    ADX_SIDEWAYS_THRESHOLD,
    ADX_TRENDING_THRESHOLD,
    RSI_OVERBOUGHT_THRESHOLD,
    RSI_OVERSOLD_THRESHOLD,
    RSI_PERIOD,
    SMA_PERIODS,
    VOLUME_AVERAGE_PERIOD,
)
from models import (
    ADXStatus,
    MarketTrend,
    MovingAverages,
    PivotPoints,
    RSIStatus,
    SmartMoneyConceptType,
    TechnicalIndicators,
)

logger = logging.getLogger(__name__)


def calculate_rsi(data: pd.DataFrame, period: int = RSI_PERIOD) -> pd.Series:
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        data: DataFrame with 'Close' column
        period: RSI period (default: 14)
    
    Returns:
        Series containing RSI values
    """
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_adx(data: pd.DataFrame, period: int = ADX_PERIOD) -> float:
    """
    Calculate Average Directional Index (ADX).
    
    Args:
        data: DataFrame with OHLC data
        period: ADX period (default: 14)
    
    Returns:
        Current ADX value
    """
    # Calculate True Range
    data['H-L'] = data['High'] - data['Low']
    data['H-C'] = abs(data['High'] - data['Close'].shift(1))
    data['L-C'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['H-L', 'H-C', 'L-C']].max(axis=1)
    
    # Calculate Directional Movement
    data['UM'] = data['High'] - data['High'].shift(1)
    data['DM'] = data['Low'].shift(1) - data['Low']
    data['+DM'] = 0
    data['-DM'] = 0
    
    data.loc[(data['UM'] > data['DM']) & (data['UM'] > 0), '+DM'] = data['UM']
    data.loc[(data['DM'] > data['UM']) & (data['DM'] > 0), '-DM'] = data['DM']
    
    # Calculate Directional Indicators
    tr_smooth = data['TR'].rolling(window=period).mean()
    plus_di = 100 * (data['+DM'].rolling(window=period).mean() / tr_smooth)
    minus_di = 100 * (data['-DM'].rolling(window=period).mean() / tr_smooth)
    
    # Calculate ADX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=period).mean().iloc[-1]
    
    return adx


def calculate_moving_averages(data: pd.DataFrame) -> MovingAverages:
    """
    Calculate multiple Simple Moving Averages (SMA).
    
    Args:
        data: DataFrame with 'Close' column
    
    Returns:
        MovingAverages object with all SMA values
    """
    sma_values = {}
    for period in SMA_PERIODS:
        sma_values[f'sma_{period}'] = data['Close'].rolling(window=period).mean().iloc[-1]
    
    return MovingAverages(
        sma_10=sma_values['sma_10'],
        sma_20=sma_values['sma_20'],
        sma_50=sma_values['sma_50'],
        sma_100=sma_values['sma_100'],
        sma_200=sma_values['sma_200']
    )


def calculate_pivot_points(prev_day: pd.Series) -> PivotPoints:
    """
    Calculate pivot points for support and resistance levels.
    
    Args:
        prev_day: Previous day's OHLC data
    
    Returns:
        PivotPoints object with all levels
    """
    pivot = (prev_day['High'] + prev_day['Low'] + prev_day['Close']) / 3
    
    resistance_1 = (2 * pivot) - prev_day['Low']
    support_1 = (2 * pivot) - prev_day['High']
    
    resistance_2 = pivot + (prev_day['High'] - prev_day['Low'])
    support_2 = pivot - (prev_day['High'] - prev_day['Low'])
    
    return PivotPoints(
        pivot=pivot,
        resistance_1=resistance_1,
        resistance_2=resistance_2,
        support_1=support_1,
        support_2=support_2
    )


def calculate_vwap(current_day: pd.Series) -> float:
    """
    Calculate Volume Weighted Average Price (VWAP) for current day.
    
    Args:
        current_day: Current day's OHLC data
    
    Returns:
        VWAP value
    """
    return (current_day['High'] + current_day['Low'] + current_day['Close']) / 3


def determine_smart_money_concept(data: pd.DataFrame) -> SmartMoneyConceptType:
    """
    Determine Smart Money Concept (SMC) based on price and volume changes.
    
    Args:
        data: DataFrame with price and volume data
    
    Returns:
        SmartMoneyConceptType enum value
    """
    volume_avg = data['Volume'].rolling(window=VOLUME_AVERAGE_PERIOD).mean().iloc[-1]
    current_volume = data['Volume'].iloc[-1]
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    
    if price_change > 0 and current_volume > volume_avg:
        return SmartMoneyConceptType.LONG_BUILDUP
    elif price_change < 0 and current_volume > volume_avg:
        return SmartMoneyConceptType.SHORT_BUILDUP
    elif price_change > 0 and current_volume < volume_avg:
        return SmartMoneyConceptType.SHORT_COVERING
    elif price_change < 0 and current_volume < volume_avg:
        return SmartMoneyConceptType.LONG_UNWINDING
    else:
        return SmartMoneyConceptType.NEUTRAL


def determine_market_trend(ltp: float, sma_50: float) -> MarketTrend:
    """
    Determine market trend based on price relative to 50 SMA.
    
    Args:
        ltp: Last traded price
        sma_50: 50-period Simple Moving Average
    
    Returns:
        MarketTrend enum value
    """
    if ltp > sma_50:
        return MarketTrend.BULLISH
    elif ltp < sma_50:
        return MarketTrend.BEARISH
    else:
        return MarketTrend.SIDEWAYS


def get_adx_status(adx: float) -> Tuple[ADXStatus, str, str]:
    """
    Get ADX status and interpretation.
    
    Args:
        adx: ADX value
    
    Returns:
        Tuple of (ADXStatus, color, remark)
    """
    if adx > ADX_TRENDING_THRESHOLD:
        return ADXStatus.TRENDING, "green", "Strong Momentum."
    elif adx < ADX_SIDEWAYS_THRESHOLD:
        return ADXStatus.SIDEWAYS, "red", "No Trade Zone."
    else:
        return ADXStatus.WEAK, "orange", "Weak Trend."


def get_rsi_status(rsi: float) -> Tuple[RSIStatus, str]:
    """
    Get RSI status and interpretation.
    
    Args:
        rsi: RSI value
    
    Returns:
        Tuple of (RSIStatus, color)
    """
    if rsi > RSI_OVERBOUGHT_THRESHOLD:
        return RSIStatus.OVERBOUGHT, "red"
    elif rsi < RSI_OVERSOLD_THRESHOLD:
        return RSIStatus.OVERSOLD, "red"
    else:
        return RSIStatus.NEUTRAL, "blue"


def calculate_all_indicators(data: pd.DataFrame) -> TechnicalIndicators:
    """
    Calculate all technical indicators for the given data.
    
    Args:
        data: Historical OHLC data
    
    Returns:
        TechnicalIndicators object with all calculated values
    
    Raises:
        ValueError: If insufficient data for calculations
    """
    if len(data) < 200:
        logger.warning("Insufficient data for full technical analysis")
        raise ValueError("Minimum 200 data points required for analysis")
    
    # Calculate indicators
    data['RSI'] = calculate_rsi(data)
    rsi_value = data['RSI'].iloc[-1]
    
    adx_value = calculate_adx(data)
    moving_averages = calculate_moving_averages(data)
    
    prev_day = data.iloc[-2]
    current_day = data.iloc[-1]
    
    pivot_points = calculate_pivot_points(prev_day)
    vwap = calculate_vwap(current_day)
    smc = determine_smart_money_concept(data)
    
    return TechnicalIndicators(
        rsi=rsi_value,
        adx=adx_value,
        smc=smc,
        moving_averages=moving_averages,
        pivot_points=pivot_points,
        vwap=vwap
    )
