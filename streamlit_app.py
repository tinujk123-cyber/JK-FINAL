"""
JK TRINETRA - Stock Analysis Dashboard

A professional stock analysis application using technical indicators,
Gann Square of Nine, and Smart Money Concepts.

Author: Refactored by Senior Python Engineer
Version: 2.1 (Mobile Optimized)
"""

import logging

import streamlit as st

from analyzer import analyze_stock_legacy
from config import (
    ACCESS_PASSWORD,
    APP_STYLES,
    APP_TITLE,
    PAGE_LAYOUT,
    STOCK_SYMBOLS,
    SYMBOL_TO_NAME,
)
from data_fetcher import clear_cache, get_stock_symbol
from scanner import scan_for_buy_signals, scan_for_reversals, scan_for_sell_signals
from trading_strategy import calculate_gann_levels
from ui_components import (
    render_disclaimer,
    render_gann_levels,
    render_high_low_grid,
    render_indicators,
    render_key_metrics,
    render_moving_averages,
    render_pivot_points,
    render_scan_results_buttons,
    render_signal_banner,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def hide_streamlit_menu():
    """
    Hide Streamlit menu, GitHub link, and deploy button using CSS.
    Optimized for mobile devices with proper viewport settings.
    """
    # Combined CSS and meta tag in one clean block
    hide_style = """
    <style>
        /* Hide Streamlit branding and menu */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        
        /* Hide toolbar and deploy button */
        [data-testid="stToolbar"] {display: none !important;}
        .stDeployButton {display: none !important;}
        button[kind="header"] {display: none !important;}
        
        /* Hide GitHub/source links */
        [data-testid="stAppViewBlockContainer"] > div:first-child {display: none !important;}
        
        /* Ensure proper mobile rendering */
        .stApp {
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
        
        /* Mobile optimizations */
        @media (max-width: 768px) {
            .stApp {
                padding: 0 !important;
            }
            
            div.block-container {
                padding: 0.5rem !important;
                max-width: 100% !important;
            }
            
            [data-testid="stSidebar"] {
                min-width: 280px !important;
            }
            
            /* Ensure columns stack properly */
            .row-widget.stHorizontal {
                flex-wrap: wrap !important;
            }
            
            div[data-testid="column"] {
                min-width: 100% !important;
                flex: 1 1 100% !important;
            }
        }
    </style>
    """
    st.markdown(hide_style, unsafe_allow_html=True)


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'selected_stock' not in st.session_state:
        st.session_state.selected_stock = "NIFTY 50"
    
    if 'scan_buy_list' not in st.session_state:
        st.session_state.scan_buy_list = []
    
    if 'scan_sell_list' not in st.session_state:
        st.session_state.scan_sell_list = []
    
    if 'scan_rev_list' not in st.session_state:
        st.session_state.scan_rev_list = []


def authenticate_user() -> bool:
    """
    Handle user authentication.
    
    Returns:
        True if authenticated, False otherwise
    """
    st.sidebar.title(APP_TITLE)
    
    if st.session_state.authenticated:
        return True
    
    user_password = st.sidebar.text_input("PASSWORD:", type="password")
    
    if user_password == ACCESS_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
        return True
    elif user_password:
        st.sidebar.error("WRONG PASSWORD")
    
    return False


def render_sidebar_controls() -> None:
    """Render sidebar controls for stock selection and scanning."""
    st.sidebar.header("CONTROLS")
    
    # Stock selection dropdown
    current_index = (
        list(STOCK_SYMBOLS.keys()).index(st.session_state.selected_stock)
        if st.session_state.selected_stock in STOCK_SYMBOLS
        else 0
    )
    
    selected_name = st.sidebar.selectbox(
        "SELECT FROM LIST:",
        list(STOCK_SYMBOLS.keys()),
        index=current_index
    )
    
    # Manual symbol input
    manual_search = st.sidebar.text_input("OR TYPE SYMBOL (Ex: TRENT):")
    
    if manual_search:
        st.session_state.selected_stock = manual_search.upper()
    else:
        st.session_state.selected_stock = selected_name
    
    # Refresh button
    if st.sidebar.button("REFRESH DATA"):
        clear_cache()
        st.rerun()
    
    # Scanner controls
    st.sidebar.subheader("MANUAL SCANNER")
    col_scan1, col_scan2 = st.sidebar.columns(2)
    
    if col_scan1.button("BUY SCAN"):
        logger.info("Starting buy scan...")
        st.session_state.scan_buy_list = scan_for_buy_signals()
        st.session_state.scan_sell_list = []
        st.session_state.scan_rev_list = []
        st.rerun()
    
    if col_scan2.button("SELL SCAN"):
        logger.info("Starting sell scan...")
        st.session_state.scan_sell_list = scan_for_sell_signals()
        st.session_state.scan_buy_list = []
        st.session_state.scan_rev_list = []
        st.rerun()
    
    if st.sidebar.button("REVERSAL SCAN"):
        logger.info("Starting reversal scan...")
        st.session_state.scan_rev_list = scan_for_reversals()
        st.session_state.scan_buy_list = []
        st.session_state.scan_sell_list = []
        st.rerun()
    
    # Display scan results
    if st.session_state.scan_buy_list:
        st.sidebar.success(f"Found {len(st.session_state.scan_buy_list)} BUY")
        render_scan_results_buttons(
            st.session_state.scan_buy_list,
            "btn_buy",
            "selected_stock"
        )
    
    if st.session_state.scan_sell_list:
        st.sidebar.error(f"Found {len(st.session_state.scan_sell_list)} SELL")
        render_scan_results_buttons(
            st.session_state.scan_sell_list,
            "btn_sell",
            "selected_stock"
        )
    
    if st.session_state.scan_rev_list:
        st.sidebar.warning(f"Found {len(st.session_state.scan_rev_list)} REVERSAL")
        render_scan_results_buttons(
            st.session_state.scan_rev_list,
            "btn_rev",
            "selected_stock"
        )


def render_dashboard(ticker: str, stock_name: str) -> None:
    """
    Render the main dashboard for a selected stock.
    
    Args:
        ticker: Stock ticker symbol
        stock_name: Display name of the stock
    """
    # Analyze stock
    analysis = analyze_stock_legacy(ticker)
    
    if analysis is None:
        st.error(
            f"Could not load data for {stock_name}. "
            "If this persists, please try 'REFRESH DATA' button."
        )
        return
    
    # Display title with price
    ltp = analysis['LTP']
    st.title(f"{stock_name} | Rs. {round(ltp, 2)}")
    
    # Render signal banner
    render_signal_banner(analysis['Signal'])
    
    # Render key metrics
    trend_text = (
        f"UPTREND (Above 50 SMA)" if analysis['Trend'] == "BULLISH"
        else f"DOWNTREND (Below 50 SMA)" if analysis['Trend'] == "BEARISH"
        else "SIDEWAYS"
    )
    
    render_key_metrics(
        ltp=ltp,
        smc=analysis['SMC'],
        vwap=analysis['VWAP'],
        trend_text=trend_text
    )
    
    # Render high/low grid
    render_high_low_grid(
        today_high=analysis['TodayHigh'],
        today_low=analysis['TodayLow'],
        prev_high=analysis['PrevHigh'],
        prev_low=analysis['PrevLow']
    )
    
    # Render pivot points
    render_pivot_points(
        s2=analysis['S2'],
        s1=analysis['S1'],
        pivot=analysis['DP'],
        r1=analysis['R1'],
        r2=analysis['R2']
    )
    
    # Render moving averages
    render_moving_averages(ltp=ltp, sma_values=analysis['SMA'])
    
    # Calculate and render Gann levels
    buy_entry, buy_targets = calculate_gann_levels(analysis['DP'], is_buy=True)
    sell_entry, sell_targets = calculate_gann_levels(analysis['DP'], is_buy=False)
    
    render_gann_levels(
        ltp=ltp,
        pivot=analysis['DP'],
        buy_targets=buy_targets,
        sell_targets=sell_targets
    )
    
    # Render indicators
    render_indicators(rsi=analysis['RSI'], adx=analysis['ADX'])
    
    # Render disclaimer
    render_disclaimer()


def main() -> None:
    """Main application entry point."""
    # Configure page with mobile optimization
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="auto",  # Auto-collapse on mobile
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom CSS
    st.markdown(APP_STYLES, unsafe_allow_html=True)
    
    # Hide Streamlit menu and GitHub link
    hide_streamlit_menu()
    
    # Authenticate user
    if not authenticate_user():
        st.stop()
    
    # Render sidebar controls
    render_sidebar_controls()
    
    # Get ticker symbol for selected stock
    ticker = get_stock_symbol(st.session_state.selected_stock, STOCK_SYMBOLS)
    
    # Render main dashboard
    render_dashboard(ticker, st.session_state.selected_stock)


if __name__ == "__main__":
    main()
