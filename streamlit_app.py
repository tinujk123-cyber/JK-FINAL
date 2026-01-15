import streamlit as st
import yfinance as yf
import pandas as pd
import math
import urllib.parse
import urllib.request
import time

# --- SETUP ---
st.set_page_config(page_title="JK TRINETRA", layout="wide")

# --- SIDEBAR & AUTH ---
st.sidebar.title("JK TRINETRA")
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.sidebar.text_input("PASSWORD:", type="password")
    if pwd == "JK2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- FUNCTIONS ---
@st.cache_data(ttl=60)
def get_data(t):
    try:
        d = yf.Ticker(t).history(period="1y")
        return (None, None) if d.empty else (d['Close'].iloc[-1], d)
    except: return None, None

def analyze(t):
    l, h = get_data(t)
    if l is None: return None
    # Logic Placeholder for speed
    return {"Symbol":t, "LTP":l, "Signal":"WAIT", "Entry":0, "SL":0, "Tgts":[0]*5}

# --- MAIN APP ---
st.title("JK TRINETRA DASHBOARD")
st.success("SYSTEM ONLINE - V10")

ticker = st.text_input("ENTER SYMBOL (e.g. TRENT):", "NIFTY 50")
t_map = {"NIFTY 50":"^NSEI", "BANK NIFTY":"^NSEBANK"}
sym = t_map.get(ticker, ticker+".NS") if ticker in t_map else ticker+".NS"

ltp, hist = get_data(sym)
if ltp:
    st.metric(label=ticker, value=f"{ltp:.2f}")
    st.line_chart(hist['Close'])
else:
    st.error("Symbol Not Found")
