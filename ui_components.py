"""
UI components for the Streamlit dashboard.

This module contains reusable UI components for rendering
various parts of the dashboard.
"""

import streamlit as st
from typing import List, Tuple

from config import SYMBOL_TO_NAME
from models import StockAnalysis
from technical_analysis import get_adx_status, get_rsi_status


def render_signal_banner(signal: str) -> None:
    """
    Render the trading signal banner.
    
    Args:
        signal: Trading signal (BUY/SELL/WAIT)
    """
    if signal == "BUY":
        css_class = "buy-signal"
        text = "BUY CONFIRMED"
    elif signal == "SELL":
        css_class = "sell-signal"
        text = "SELL CONFIRMED"
    else:
        css_class = "wait-signal"
        text = "WAIT MODE"
    
    st.markdown(f"<div class='{css_class}'>{text}</div>", unsafe_allow_html=True)


def render_key_metrics(ltp: float, smc: str, vwap: float, trend_text: str) -> None:
    """
    Render the key metrics grid.
    
    Args:
        ltp: Last traded price
        smc: Smart Money Concept type
        vwap: Volume Weighted Average Price
        trend_text: Trend description text
    """
    col1, col2, col3, col4 = st.columns(4)
    
    # LTP
    html_ltp = f"<div class='mini-box'>LTP<br><b>Rs. {round(ltp, 2)}</b></div>"
    col1.markdown(html_ltp, unsafe_allow_html=True)
    
    # Smart Money Concept
    smc_color = "green" if "BUILDUP" in smc else ("red" if "UNWINDING" in smc else "orange")
    if "SHORT BUILDUP" in smc:
        smc_color = "red"
    html_smc = f"<div class='mini-box'>SMART MONEY<br><b style='color:{smc_color}'>{smc}</b></div>"
    col2.markdown(html_smc, unsafe_allow_html=True)
    
    # VWAP
    html_vwap = f"<div class='mini-box'>VWAP<br><b>{round(vwap, 2)}</b></div>"
    col3.markdown(html_vwap, unsafe_allow_html=True)
    
    # Trend
    html_trend = f"<div class='mini-box'>TREND (50 SMA)<br><b>{trend_text}</b></div>"
    col4.markdown(html_trend, unsafe_allow_html=True)


def render_high_low_grid(today_high: float, today_low: float, prev_high: float, prev_low: float) -> None:
    """
    Render the high/low price grid.
    
    Args:
        today_high: Today's high price
        today_low: Today's low price
        prev_high: Previous day's high price
        prev_low: Previous day's low price
    """
    col1, col2, col3, col4 = st.columns(4)
    
    col1.markdown(f"<div class='mini-box'>TODAY HIGH<br><b>{round(today_high, 2)}</b></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='mini-box'>TODAY LOW<br><b>{round(today_low, 2)}</b></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='mini-box'>PREV HIGH<br><b>{round(prev_high, 2)}</b></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='mini-box'>PREV LOW<br><b>{round(prev_low, 2)}</b></div>", unsafe_allow_html=True)


def render_pivot_points(s2: float, s1: float, pivot: float, r1: float, r2: float) -> None:
    """
    Render pivot points grid.
    
    Args:
        s2: Support level 2
        s1: Support level 1
        pivot: Pivot point
        r1: Resistance level 1
        r2: Resistance level 2
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.markdown(f"<div class='pivot-box'>S2<br><b>{round(s2, 2)}</b></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='pivot-box'>S1<br><b>{round(s1, 2)}</b></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='pivot-box' style='background-color:#fff;'>PIVOT<br><b>{round(pivot, 2)}</b></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='pivot-box'>R1<br><b>{round(r1, 2)}</b></div>", unsafe_allow_html=True)
    col5.markdown(f"<div class='pivot-box'>R2<br><b>{round(r2, 2)}</b></div>", unsafe_allow_html=True)


def render_moving_averages(ltp: float, sma_values: List[float]) -> None:
    """
    Render moving averages grid.
    
    Args:
        ltp: Last traded price
        sma_values: List of SMA values [10, 20, 50, 100, 200]
    """
    st.markdown("<b>KEY MOVING AVERAGES (TREND SUPPORT)</b>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    periods = [10, 20, 50, 100, 200]
    
    for col, period, sma_value in zip(columns, periods, sma_values):
        color = "green" if ltp > sma_value else "red"
        html = f"<div class='sma-box'>{period} SMA<br><b style='color:{color}'>{round(sma_value, 2)}</b></div>"
        col.markdown(html, unsafe_allow_html=True)


def render_gann_levels(ltp: float, pivot: float, buy_targets: List[float], sell_targets: List[float]) -> None:
    """
    Render Gann Square of Nine levels.
    
    Args:
        ltp: Last traded price
        pivot: Pivot point
        buy_targets: List of buy targets
        sell_targets: List of sell targets
    """
    buy_entry = round(pivot * 1.001, 2)
    sell_entry = round(pivot * 0.999, 2)
    
    col_buy, col_sell = st.columns(2)
    
    # Buy plan
    with col_buy:
        html_buy = f"""<div class='plan-box-buy'>
            <b>BUY ABOVE: {buy_entry}</b> | SL: {round(pivot, 2)}<hr>
            T1: {buy_targets[0]} | T2: {buy_targets[1]}<br>
            T3: {buy_targets[2]} | T4: {buy_targets[3]}<br>
            <b>TGT 5: {buy_targets[4]}</b>
        </div>"""
        st.markdown(html_buy, unsafe_allow_html=True)
        
        if ltp >= buy_targets[4]:
            st.markdown("<div class='reverse-warn'>REVERSAL ZONE</div>", unsafe_allow_html=True)
    
    # Sell plan
    with col_sell:
        html_sell = f"""<div class='plan-box-sell'>
            <b>SELL BELOW: {sell_entry}</b> | SL: {round(pivot, 2)}<hr>
            T1: {sell_targets[0]} | T2: {sell_targets[1]}<br>
            T3: {sell_targets[2]} | T4: {sell_targets[3]}<br>
            <b>TGT 5: {sell_targets[4]}</b>
        </div>"""
        st.markdown(html_sell, unsafe_allow_html=True)
        
        if ltp <= sell_targets[4]:
            st.markdown("<div class='reverse-warn'>REVERSAL ZONE</div>", unsafe_allow_html=True)


def render_indicators(rsi: float, adx: float) -> None:
    """
    Render RSI and ADX indicators.
    
    Args:
        rsi: RSI value
        adx: ADX value
    """
    adx_status, adx_color, adx_remark = get_adx_status(adx)
    rsi_status, rsi_color = get_rsi_status(rsi)
    
    html = f"""<div style='margin-top:5px; display:flex; gap:10px;'>
        <div style='flex:1; padding:5px; border-radius:5px; border:1px solid {adx_color}; text-align:center;'>
            <b style='color:{adx_color}!important;'>ADX: {round(adx, 2)} ({adx_status.value})</b><br>
            <span style='font-size:10px;'>{adx_remark}</span>
        </div>
        <div style='flex:1; padding:5px; border-radius:5px; border:1px solid {rsi_color}; text-align:center;'>
            <b style='color:{rsi_color}!important;'>RSI: {round(rsi, 2)}</b><br>
            <span style='font-size:11px;'>{rsi_status.value}</span>
        </div>
    </div>"""
    
    st.markdown(html, unsafe_allow_html=True)


def render_disclaimer() -> None:
    """Render the disclaimer message."""
    st.markdown(
        """<div class='disclaimer-box'>IT IS NOT A BUY/SELL RECOMMENDATION.<br>
        STRICTLY FOR STUDY PURPOSE.<br>CONSULT YOUR FINANCIAL ADVISOR.</div>""",
        unsafe_allow_html=True
    )


def render_scan_results_buttons(scan_list: List[dict], button_prefix: str, session_state_key: str) -> None:
    """
    Render buttons for scan results in sidebar.
    
    Args:
        scan_list: List of scan results
        button_prefix: Prefix for button keys
        session_state_key: Key to update in session state when clicked
    """
    for i, item in enumerate(scan_list):
        name = SYMBOL_TO_NAME.get(item['Symbol'], item['Symbol'])
        
        if 'Type' in item:  # Reversal scan
            button_label = f"{name} [{item['Type']}]"
        else:  # Buy/Sell scan
            button_label = f"{name} ({round(item['LTP'], 1)})"
        
        if st.sidebar.button(button_label, key=f"{button_prefix}_{i}"):
            st.session_state.selected_stock = name
            st.rerun()
