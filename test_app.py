"""
Unit tests for JK TRINETRA application.

Run tests with: python -m pytest test_app.py -v
"""

import pytest
import pandas as pd
import math

from config import STOCK_SYMBOLS, GANN_STEP_SIZE
from models import TradingSignal, MarketTrend, SmartMoneyConceptType
from technical_analysis import (
    calculate_rsi,
    calculate_moving_averages,
    calculate_pivot_points,
    determine_market_trend,
)
from trading_strategy import calculate_gann_levels, generate_trading_signal


class TestConfiguration:
    """Test configuration and constants."""
    
    def test_stock_symbols_not_empty(self):
        """Test that stock symbols dictionary is populated."""
        assert len(STOCK_SYMBOLS) > 0
    
    def test_stock_symbols_have_valid_format(self):
        """Test that stock symbols have valid format."""
        for name, symbol in STOCK_SYMBOLS.items():
            assert isinstance(name, str)
            assert isinstance(symbol, str)
            assert len(symbol) > 0


class TestTechnicalAnalysis:
    """Test technical analysis calculations."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLC data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=250, freq='D')
        data = pd.DataFrame({
            'Open': [100 + i * 0.5 for i in range(250)],
            'High': [102 + i * 0.5 for i in range(250)],
            'Low': [98 + i * 0.5 for i in range(250)],
            'Close': [101 + i * 0.5 for i in range(250)],
            'Volume': [1000000 + i * 1000 for i in range(250)]
        }, index=dates)
        return data
    
    def test_calculate_moving_averages(self, sample_data):
        """Test moving average calculation."""
        ma = calculate_moving_averages(sample_data)
        
        assert ma.sma_10 > 0
        assert ma.sma_20 > 0
        assert ma.sma_50 > 0
        assert ma.sma_100 > 0
        assert ma.sma_200 > 0
        
        # In uptrend, longer MAs should be lower
        assert ma.sma_10 > ma.sma_20
        assert ma.sma_20 > ma.sma_50
    
    def test_calculate_pivot_points(self, sample_data):
        """Test pivot point calculation."""
        prev_day = sample_data.iloc[-2]
        pivots = calculate_pivot_points(prev_day)
        
        assert pivots.pivot > 0
        assert pivots.resistance_1 > pivots.pivot
        assert pivots.resistance_2 > pivots.resistance_1
        assert pivots.support_1 < pivots.pivot
        assert pivots.support_2 < pivots.support_1
    
    def test_determine_market_trend(self):
        """Test market trend determination."""
        # Bullish trend
        trend = determine_market_trend(ltp=150, sma_50=140)
        assert trend == MarketTrend.BULLISH
        
        # Bearish trend
        trend = determine_market_trend(ltp=130, sma_50=140)
        assert trend == MarketTrend.BEARISH
        
        # Sideways
        trend = determine_market_trend(ltp=140, sma_50=140)
        assert trend == MarketTrend.SIDEWAYS


class TestTradingStrategy:
    """Test trading strategy and signal generation."""
    
    def test_calculate_gann_levels_buy(self):
        """Test Gann level calculation for buy side."""
        pivot = 100
        entry, targets = calculate_gann_levels(pivot, is_buy=True)
        
        assert entry > pivot
        assert len(targets) == 5
        
        # Targets should be increasing
        for i in range(len(targets) - 1):
            assert targets[i + 1] > targets[i]
    
    def test_calculate_gann_levels_sell(self):
        """Test Gann level calculation for sell side."""
        pivot = 100
        entry, targets = calculate_gann_levels(pivot, is_buy=False)
        
        assert entry < pivot
        assert len(targets) == 5
        
        # Targets should be decreasing
        for i in range(len(targets) - 1):
            assert targets[i + 1] < targets[i]
    
    def test_generate_trading_signal_buy(self):
        """Test buy signal generation."""
        signal = generate_trading_signal(
            ltp=105,
            pivot=100,
            vwap=102,
            prev_high=104,
            prev_low=98
        )
        assert signal == TradingSignal.BUY
    
    def test_generate_trading_signal_sell(self):
        """Test sell signal generation."""
        signal = generate_trading_signal(
            ltp=95,
            pivot=100,
            vwap=98,
            prev_high=102,
            prev_low=96
        )
        assert signal == TradingSignal.SELL
    
    def test_generate_trading_signal_wait(self):
        """Test wait signal generation."""
        signal = generate_trading_signal(
            ltp=100,
            pivot=100,
            vwap=100,
            prev_high=102,
            prev_low=98
        )
        assert signal == TradingSignal.WAIT


class TestModels:
    """Test data models."""
    
    def test_trading_signal_enum(self):
        """Test TradingSignal enum values."""
        assert TradingSignal.BUY.value == "BUY"
        assert TradingSignal.SELL.value == "SELL"
        assert TradingSignal.WAIT.value == "WAIT"
    
    def test_market_trend_enum(self):
        """Test MarketTrend enum values."""
        assert MarketTrend.BULLISH.value == "BULLISH"
        assert MarketTrend.BEARISH.value == "BEARISH"
        assert MarketTrend.SIDEWAYS.value == "SIDEWAYS"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
