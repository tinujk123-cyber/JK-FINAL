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

# CSS Styling with Mobile Optimization
APP_STYLES = """
<style>
    /* ========================================
       BASE STYLES
       ======================================== */
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
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* ========================================
       COMPONENT STYLES
       ======================================== */
    .mini-box { 
        background-color: #f0f2f6; 
        border: 1px solid #dce1e6; 
        padding: 8px; 
        border-radius: 6px; 
        text-align: center; 
        font-size: 12px; 
        margin-bottom: 8px;
        min-height: 60px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .mini-box b { 
        font-size: 16px; 
        color: #000; 
        font-weight: 700; 
    }
    
    .pivot-box { 
        background-color: #fff3e0; 
        border: 1px solid #ffe0b2; 
        padding: 6px; 
        border-radius: 4px; 
        text-align: center; 
        font-size: 11px; 
        margin-bottom: 6px;
        min-height: 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .pivot-box b { 
        font-size: 14px; 
    }
    
    .buy-signal { 
        background-color: #d4edda; 
        color: #155724; 
        padding: 10px; 
        border-radius: 5px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold; 
        border: 1px solid #28a745; 
        margin: 8px 0; 
    }
    
    .sell-signal { 
        background-color: #f8d7da; 
        color: #721c24; 
        padding: 10px; 
        border-radius: 5px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold; 
        border: 1px solid #dc3545; 
        margin: 8px 0; 
    }
    
    .wait-signal { 
        background-color: #e2e3e5; 
        color: #383d41; 
        padding: 10px; 
        border-radius: 5px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold; 
        border: 1px solid #d6d8db; 
        margin: 8px 0; 
    }
    
    .plan-box-buy { 
        border: 1px solid #28a745; 
        padding: 10px; 
        border-radius: 6px; 
        background-color: #f0fff4; 
        color: #000; 
        font-size: 13px; 
        margin-bottom: 10px;
    }
    
    .plan-box-sell { 
        border: 1px solid #dc3545; 
        padding: 10px; 
        border-radius: 6px; 
        background-color: #fff5f5; 
        color: #000; 
        font-size: 13px; 
        margin-bottom: 10px;
    }
    
    .reverse-warn { 
        color: #ffffff; 
        background-color: #ff0000; 
        font-weight: bold; 
        text-align: center; 
        padding: 4px; 
        border-radius: 3px; 
        font-size: 11px; 
        margin-top: 6px; 
    }
    
    .sma-box { 
        border: 1px solid #ddd; 
        padding: 6px; 
        border-radius: 4px; 
        text-align: center; 
        font-size: 11px;
        min-height: 50px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .sma-box b { 
        font-size: 13px; 
    }
    
    hr { 
        margin: 6px 0px !important; 
    }
    
    /* Touch-friendly buttons */
    div[data-testid="column"] button { 
        padding: 8px 12px !important; 
        min-height: 44px !important; 
        font-size: 14px !important;
        border-radius: 6px !important;
        cursor: pointer;
    }
    
    /* Sidebar buttons */
    .stButton button {
        min-height: 44px !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
    }
    
    /* Input fields */
    input, select, textarea {
        min-height: 44px !important;
        font-size: 16px !important; /* Prevents zoom on iOS */
        padding: 8px !important;
    }
    
    /* ========================================
       MOBILE RESPONSIVE STYLES
       ======================================== */
    
    /* Tablets and below (768px) */
    @media (max-width: 768px) {
        div.block-container { 
            padding-top: 1rem !important; 
            padding-bottom: 0.5rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        h1 { 
            font-size: 20px !important; 
            padding-bottom: 8px !important;
            text-align: center;
        }
        
        .mini-box { 
            padding: 10px; 
            font-size: 13px; 
            margin-bottom: 10px;
            min-height: 70px;
        }
        
        .mini-box b { 
            font-size: 18px; 
        }
        
        .pivot-box { 
            padding: 8px; 
            font-size: 12px; 
            margin-bottom: 8px;
            min-height: 60px;
        }
        
        .pivot-box b { 
            font-size: 16px; 
        }
        
        .buy-signal, .sell-signal, .wait-signal { 
            padding: 12px; 
            font-size: 20px; 
            margin: 10px 0; 
        }
        
        .plan-box-buy, .plan-box-sell { 
            padding: 12px; 
            font-size: 14px; 
            margin-bottom: 12px;
        }
        
        .sma-box { 
            padding: 8px; 
            font-size: 12px;
            min-height: 60px;
        }
        
        .sma-box b { 
            font-size: 15px; 
        }
        
        /* Larger touch targets */
        div[data-testid="column"] button { 
            padding: 12px 16px !important; 
            min-height: 48px !important; 
            font-size: 15px !important;
            width: 100%;
        }
        
        .stButton button {
            min-height: 48px !important;
            padding: 12px 20px !important;
            font-size: 15px !important;
            width: 100%;
        }
        
        /* Sidebar optimization */
        section[data-testid="stSidebar"] {
            min-width: 280px !important;
        }
        
        /* Column spacing */
        div[data-testid="column"] {
            padding: 0 4px !important;
        }
    }
    
    /* Mobile phones (480px and below) */
    @media (max-width: 480px) {
        div.block-container { 
            padding: 0.5rem !important;
        }
        
        h1 { 
            font-size: 18px !important; 
            padding-bottom: 10px !important;
        }
        
        .mini-box { 
            padding: 12px; 
            font-size: 14px; 
            margin-bottom: 12px;
            min-height: 75px;
        }
        
        .mini-box b { 
            font-size: 20px; 
        }
        
        .pivot-box { 
            padding: 10px; 
            font-size: 13px; 
            margin-bottom: 10px;
            min-height: 65px;
        }
        
        .pivot-box b { 
            font-size: 18px; 
        }
        
        .buy-signal, .sell-signal, .wait-signal { 
            padding: 14px; 
            font-size: 22px; 
            margin: 12px 0; 
        }
        
        .plan-box-buy, .plan-box-sell { 
            padding: 14px; 
            font-size: 15px; 
            margin-bottom: 14px;
            line-height: 1.6;
        }
        
        .sma-box { 
            padding: 10px; 
            font-size: 13px;
            min-height: 65px;
        }
        
        .sma-box b { 
            font-size: 16px; 
        }
        
        /* Extra large touch targets for mobile */
        div[data-testid="column"] button { 
            padding: 14px 18px !important; 
            min-height: 50px !important; 
            font-size: 16px !important;
            width: 100%;
            margin-bottom: 8px !important;
        }
        
        .stButton button {
            min-height: 50px !important;
            padding: 14px 22px !important;
            font-size: 16px !important;
            width: 100%;
            margin-bottom: 8px !important;
        }
        
        /* Stack columns on mobile */
        div[data-testid="column"] {
            min-width: 100% !important;
            padding: 4px 0 !important;
        }
        
        /* Sidebar full width on mobile */
        section[data-testid="stSidebar"] {
            width: 100% !important;
        }
        
        /* Prevent horizontal scroll */
        .stApp {
            overflow-x: hidden !important;
        }
        
        /* Optimize selectbox for mobile */
        div[data-baseweb="select"] {
            font-size: 16px !important;
        }
    }
    
    /* Small mobile devices (375px and below) */
    @media (max-width: 375px) {
        h1 { 
            font-size: 16px !important; 
        }
        
        .mini-box, .pivot-box, .sma-box { 
            font-size: 12px; 
        }
        
        .mini-box b { 
            font-size: 18px; 
        }
        
        .pivot-box b, .sma-box b { 
            font-size: 16px; 
        }
        
        .buy-signal, .sell-signal, .wait-signal { 
            font-size: 20px; 
        }
        
        .plan-box-buy, .plan-box-sell { 
            font-size: 14px; 
        }
    }
    
    /* ========================================
       ACCESSIBILITY & UX IMPROVEMENTS
       ======================================== */
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Focus states for accessibility */
    button:focus, input:focus, select:focus {
        outline: 2px solid #1f77b4 !important;
        outline-offset: 2px !important;
    }
    
    /* Prevent text selection on buttons */
    button {
        user-select: none;
        -webkit-user-select: none;
        -moz-user-select: none;
    }
    
    /* Improve tap highlighting on mobile */
    * {
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
    }
    
    /* Loading state */
    .stSpinner {
        text-align: center;
        padding: 20px;
    }
</style>
"""
