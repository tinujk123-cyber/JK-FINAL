"""
Configuration module for JK TRINETRA application.

This module contains all configuration constants, stock symbols,
and application settings.
"""

from typing import Dict

# Application Configuration
APP_TITLE = "JK TRINETRA"
PAGE_LAYOUT = "wide"
ACCESS_PASSWORD = "JK2026"

# Cache Configuration
CACHE_TTL_SECONDS = 60

# Technical Analysis Parameters
RSI_PERIOD = 14
ADX_PERIOD = 14
VOLUME_AVERAGE_PERIOD = 10
SMA_PERIODS = [10, 20, 50, 100, 200]

# ADX Thresholds
ADX_TRENDING_THRESHOLD = 25
ADX_SIDEWAYS_THRESHOLD = 20

# RSI Thresholds
RSI_OVERBOUGHT_THRESHOLD = 70
RSI_OVERSOLD_THRESHOLD = 30

# Gann Square of Nine Parameters
GANN_BUY_MULTIPLIER = 1.001
GANN_SELL_MULTIPLIER = 0.999
GANN_STEP_SIZE = 0.125
GANN_TARGET_COUNT = 5

# Stock Dictionary - Maps display names to Yahoo Finance symbols
STOCK_SYMBOLS: Dict[str, str] = {
    # Indices
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "FIN NIFTY": "NIFTY_FIN_SERVICE.NS",
    
    # Large Cap Stocks
    "Reliance": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Infosys": "INFY.NS",
    "TCS": "TCS.NS",
    "ITC": "ITC.NS",
    "L&T": "LT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Kotak Bank": "KOTAKBANK.NS",
    "SBI": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Maruti": "MARUTI.NS",
    "HCL Tech": "HCLTECH.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Titan": "TITAN.NS",
    "M&M": "M&M.NS",
    "UltraTech": "ULTRACEMCO.NS",
    "Tata Steel": "TATASTEEL.NS",
    "NTPC": "NTPC.NS",
    "Power Grid": "POWERGRID.NS",
    "Wipro": "WIPRO.NS",
    "Adani Ent": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Coal India": "COALINDIA.NS",
    "Hindalco": "HINDALCO.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Dr Reddy": "DRREDDY.NS",
    "BPCL": "BPCL.NS",
    "Nestle": "NESTLEIND.NS",
    "Grasim": "GRASIM.NS",
    "Hero Moto": "HEROMOTOCO.NS",
    "Tech M": "TECHM.NS",
    "Cipla": "CIPLA.NS",
    "Apollo Hosp": "APOLLOHOSP.NS",
    "Tata Cons": "TATACONSUM.NS",
    "Divis Lab": "DIVISLAB.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Jio Finance": "JIOFIN.NS",
    "Trent": "TRENT.NS",
    "BEL": "BEL.NS",
    "HAL": "HAL.NS",
    "Zomato": "ZOMATO.NS",
    "DLF": "DLF.NS",
    "Varun Bev": "VBL.NS",
    "Siemens": "SIEMENS.NS",
    "ABB": "ABB.NS",
    "Indigo": "INDIGO.NS",
    "Polycab": "POLYCAB.NS",
    
    # PSU Banks
    "REC": "REC.NS",
    "PFC": "PFC.NS",
    "Canara Bank": "CANBK.NS",
    "PNB": "PNB.NS",
    "Union Bank": "UNIONBANK.NS",
    "Bank Baroda": "BANKBARODA.NS",
    
    # Infrastructure & Defense
    "IRFC": "IRFC.NS",
    "RVNL": "RVNL.NS",
    "Mazagon": "MAZDOCK.NS",
    "Cochin Ship": "COCHINSHIP.NS",
    "BHEL": "BHEL.NS",
    
    # Metals & Mining
    "SAIL": "SAIL.NS",
    "NMDC": "NMDC.NS",
    "Vedanta": "VEDL.NS",
    "Hind Zinc": "HINDZINC.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Jindal Steel": "JINDALSTEL.NS",
    
    # Energy
    "Tata Power": "TATAPOWER.NS",
    "Adani Power": "ADANIPOWER.NS",
    "GAIL": "GAIL.NS",
    "ONGC": "ONGC.NS",
    "Oil India": "OIL.NS",
    
    # Auto Components
    "Motherson": "MOTHERSON.NS",
    "Bosch": "BOSCHLTD.NS",
    "TVS Motor": "TVSMOTOR.NS",
    "MRF": "MRF.NS",
    "Samvardhana": "MOTHERSON.NS",
}

# Reverse mapping for quick lookup
SYMBOL_TO_NAME: Dict[str, str] = {v: k for k, v in STOCK_SYMBOLS.items()}

# CSS Styling
APP_STYLES = """
<style>
    .stApp { 
        background-color: #ffffff; 
        color: #000000; 
        font-size: 12px !important; 
    }
    h1 { 
        font-size: 22px !important; 
        margin: 0px !important; 
        padding-bottom: 5px !important; 
    }
    div.block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 1rem !important; 
    }
    .mini-box { 
        background-color: #f0f2f6; 
        border: 1px solid #dce1e6; 
        padding: 5px; 
        border-radius: 6px; 
        text-align: center; 
        font-size: 12px; 
        margin-bottom: 4px; 
    }
    .mini-box b { 
        font-size: 16px; 
        color: #000; 
        font-weight: 700; 
    }
    .pivot-box { 
        background-color: #fff3e0; 
        border: 1px solid #ffe0b2; 
        padding: 4px; 
        border-radius: 4px; 
        text-align: center; 
        font-size: 11px; 
        margin-bottom: 3px; 
    }
    .pivot-box b { 
        font-size: 14px; 
    }
    .buy-signal { 
        background-color: #d4edda; 
        color: #155724; 
        padding: 5px; 
        border-radius: 5px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold; 
        border: 1px solid #28a745; 
        margin: 5px 0; 
    }
    .sell-signal { 
        background-color: #f8d7da; 
        color: #721c24; 
        padding: 5px; 
        border-radius: 5px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold; 
        border: 1px solid #dc3545; 
        margin: 5px 0; 
    }
    .wait-signal { 
        background-color: #e2e3e5; 
        color: #383d41; 
        padding: 5px; 
        border-radius: 5px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold; 
        border: 1px solid #d6d8db; 
        margin: 5px 0; 
    }
    .plan-box-buy { 
        border: 1px solid #28a745; 
        padding: 6px; 
        border-radius: 6px; 
        background-color: #f0fff4; 
        color: #000; 
        font-size: 13px; 
    }
    .plan-box-sell { 
        border: 1px solid #dc3545; 
        padding: 6px; 
        border-radius: 6px; 
        background-color: #fff5f5; 
        color: #000; 
        font-size: 13px; 
    }
    .reverse-warn { 
        color: #ffffff; 
        background-color: #ff0000; 
        font-weight: bold; 
        text-align: center; 
        padding: 2px; 
        border-radius: 3px; 
        font-size: 11px; 
        margin-top: 3px; 
    }
    .sma-box { 
        border: 1px solid #ddd; 
        padding: 3px; 
        border-radius: 4px; 
        text-align: center; 
        font-size: 11px; 
    }
    .sma-box b { 
        font-size: 13px; 
    }
    hr { 
        margin: 3px 0px !important; 
    }
    div[data-testid="column"] button { 
        padding: 2px 8px !important; 
        min-height: 28px !important; 
        font-size: 12px !important; 
    }
</style>
"""
