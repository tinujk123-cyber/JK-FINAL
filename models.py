"""
Data models for JK TRINETRA application.

This module defines data classes and enums for type-safe data handling.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TradingSignal(Enum):
    """Enumeration for trading signals."""
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


class MarketTrend(Enum):
    """Enumeration for market trends."""
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


class SmartMoneyConceptType(Enum):
    """Enumeration for Smart Money Concept (SMC) types."""
    LONG_BUILDUP = "LONG BUILDUP"
    SHORT_BUILDUP = "SHORT BUILDUP"
    SHORT_COVERING = "SHORT COVERING"
    LONG_UNWINDING = "LONG UNWINDING"
    NEUTRAL = "NEUTRAL"


class ADXStatus(Enum):
    """Enumeration for ADX trend status."""
    TRENDING = "TRENDING"
    WEAK = "WEAK"
    SIDEWAYS = "SIDEWAYS"


class RSIStatus(Enum):
    """Enumeration for RSI status."""
    OVERBOUGHT = "OVERBOUGHT (Risk)"
    OVERSOLD = "OVERSOLD (Bounce)"
    NEUTRAL = "NEUTRAL"


@dataclass
class PivotPoints:
    """Data class for pivot point calculations."""
    pivot: float
    resistance_1: float
    resistance_2: float
    support_1: float
    support_2: float


@dataclass
class MovingAverages:
    """Data class for moving average values."""
    sma_10: float
    sma_20: float
    sma_50: float
    sma_100: float
    sma_200: float

    def to_list(self) -> List[float]:
        """Convert to list for backward compatibility."""
        return [self.sma_10, self.sma_20, self.sma_50, self.sma_100, self.sma_200]


@dataclass
class TechnicalIndicators:
    """Data class for technical indicators."""
    rsi: float
    adx: float
    smc: SmartMoneyConceptType
    moving_averages: MovingAverages
    pivot_points: PivotPoints
    vwap: float


@dataclass
class PriceData:
    """Data class for price information."""
    ltp: float
    today_high: float
    today_low: float
    prev_high: float
    prev_low: float


@dataclass
class TradingPlan:
    """Data class for trading plan with entry, stop loss, and targets."""
    signal: TradingSignal
    entry: float
    stop_loss: float
    targets: List[float]


@dataclass
class StockAnalysis:
    """Complete stock analysis data."""
    symbol: str
    price_data: PriceData
    technical_indicators: TechnicalIndicators
    trading_plan: TradingPlan
    trend: MarketTrend

    def to_dict(self) -> dict:
        """
        Convert to dictionary for backward compatibility.
        
        Returns:
            Dictionary representation of the analysis
        """
        return {
            "Symbol": self.symbol,
            "LTP": self.price_data.ltp,
            "Signal": self.trading_plan.signal.value,
            "SMC": self.technical_indicators.smc.value,
            "Trend": self.trend.value,
            "VWAP": self.technical_indicators.vwap,
            "Entry": self.trading_plan.entry,
            "SL": self.trading_plan.stop_loss,
            "Tgts": self.trading_plan.targets,
            "S1": self.technical_indicators.pivot_points.support_1,
            "S2": self.technical_indicators.pivot_points.support_2,
            "R1": self.technical_indicators.pivot_points.resistance_1,
            "R2": self.technical_indicators.pivot_points.resistance_2,
            "DP": self.technical_indicators.pivot_points.pivot,
            "SMA": self.technical_indicators.moving_averages.to_list(),
            "TodayHigh": self.price_data.today_high,
            "TodayLow": self.price_data.today_low,
            "PrevHigh": self.price_data.prev_high,
            "PrevLow": self.price_data.prev_low,
            "RSI": self.technical_indicators.rsi,
            "ADX": self.technical_indicators.adx,
        }


@dataclass
class ReversalSignal:
    """Data class for reversal scan results."""
    symbol: str
    ltp: float
    reversal_type: str  # "TOP (SELL)" or "BOTTOM (BUY)"
