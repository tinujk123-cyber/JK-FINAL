"""
Trading strategy and signal generation module.

This module implements the Gann Square of Nine strategy
and generates trading signals with entry, stop loss, and targets.
"""

import logging
import math
from typing import List, Tuple

import pandas as pd

from config import (
    GANN_BUY_MULTIPLIER,
    GANN_SELL_MULTIPLIER,
    GANN_STEP_SIZE,
    GANN_TARGET_COUNT,
)
from models import PriceData, TradingPlan, TradingSignal

logger = logging.getLogger(__name__)


def calculate_gann_levels(pivot: float, is_buy: bool) -> Tuple[float, List[float]]:
    """
    Calculate Gann Square of Nine levels for entry and targets.
    
    Args:
        pivot: Pivot point value
        is_buy: True for buy levels, False for sell levels
    
    Returns:
        Tuple of (entry_price, list_of_targets)
    """
    if is_buy:
        entry = pivot * GANN_BUY_MULTIPLIER
        sqrt_entry = math.sqrt(entry)
        targets = [
            round((sqrt_entry + (i * GANN_STEP_SIZE)) ** 2, 2)
            for i in range(1, GANN_TARGET_COUNT + 1)
        ]
    else:
        entry = pivot * GANN_SELL_MULTIPLIER
        sqrt_entry = math.sqrt(entry)
        targets = [
            round((sqrt_entry - (i * GANN_STEP_SIZE)) ** 2, 2)
            for i in range(1, GANN_TARGET_COUNT + 1)
        ]
    
    return round(entry, 2), targets


def generate_trading_signal(
    ltp: float,
    pivot: float,
    vwap: float,
    prev_high: float,
    prev_low: float
) -> TradingSignal:
    """
    Generate trading signal based on price action.
    
    Args:
        ltp: Last traded price
        pivot: Pivot point
        vwap: Volume Weighted Average Price
        prev_high: Previous day's high
        prev_low: Previous day's low
    
    Returns:
        TradingSignal enum value
    """
    # Buy signal conditions
    if ltp > pivot and ltp > vwap and ltp > prev_low:
        return TradingSignal.BUY
    
    # Sell signal conditions
    elif ltp < pivot and ltp < vwap and ltp < prev_high:
        return TradingSignal.SELL
    
    # Wait/neutral
    else:
        return TradingSignal.WAIT


def create_trading_plan(
    signal: TradingSignal,
    pivot: float,
    prev_high: float,
    prev_low: float
) -> TradingPlan:
    """
    Create a complete trading plan with entry, stop loss, and targets.
    
    Args:
        signal: Trading signal (BUY/SELL/WAIT)
        pivot: Pivot point value
        prev_high: Previous day's high
        prev_low: Previous day's low
    
    Returns:
        TradingPlan object
    """
    if signal == TradingSignal.BUY:
        entry, targets = calculate_gann_levels(pivot, is_buy=True)
        stop_loss = round(prev_low, 2)
        
    elif signal == TradingSignal.SELL:
        entry, targets = calculate_gann_levels(pivot, is_buy=False)
        stop_loss = round(prev_high, 2)
        
    else:  # WAIT
        entry = 0
        stop_loss = 0
        targets = [0] * GANN_TARGET_COUNT
    
    return TradingPlan(
        signal=signal,
        entry=entry,
        stop_loss=stop_loss,
        targets=targets
    )


def check_reversal_zone(ltp: float, pivot: float) -> Tuple[bool, str]:
    """
    Check if price is in reversal zone (reached 5th target).
    
    Args:
        ltp: Last traded price
        pivot: Pivot point
    
    Returns:
        Tuple of (is_reversal_zone, reversal_type)
    """
    # Calculate 5th targets for both buy and sell
    buy_entry, buy_targets = calculate_gann_levels(pivot, is_buy=True)
    sell_entry, sell_targets = calculate_gann_levels(pivot, is_buy=False)
    
    buy_target_5 = buy_targets[4]  # 5th target (index 4)
    sell_target_5 = sell_targets[4]
    
    if ltp >= buy_target_5:
        return True, "TOP (SELL)"
    elif ltp <= sell_target_5:
        return True, "BOTTOM (BUY)"
    else:
        return False, ""


def extract_price_data(data: pd.DataFrame) -> PriceData:
    """
    Extract price data from historical DataFrame.
    
    Args:
        data: Historical OHLC DataFrame
    
    Returns:
        PriceData object
    """
    current_day = data.iloc[-1]
    prev_day = data.iloc[-2]
    
    return PriceData(
        ltp=current_day['Close'],
        today_high=current_day['High'],
        today_low=current_day['Low'],
        prev_high=prev_day['High'],
        prev_low=prev_day['Low']
    )
