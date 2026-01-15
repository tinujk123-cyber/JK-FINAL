import streamlit as st
import yfinance as yf
import pandas as pd
import math

# 1. APP SETUP
st.set_page_config(page_title="JK TRINETRA", layout="wide")
ACCESS_PASSWORD = "JK2026"

# 2. SESSION STATE
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'selected_stock' not in st.session_state: st.session_state.selected_stock = "NIFTY 50"
# Initialize scanner lists to prevent errors if scanner buttons are clicked
if 'scan_buy_list' not in st.session_state: st.session_state.scan_buy_list = []
if 'scan_sell_list' not in st.session_state: st.session_state.scan_sell_list = []
if 'scan_rev_list' not in st.session_state: st.session_state.scan_rev_list = []

# 3. AUTHENTICATION
st.sidebar.title("JK TRINETRA")
if not st.session_state.authenticated:
    user_pass = st.sidebar.text_input("PASSWORD:", type="password")
    if user_pass == ACCESS_PASSWORD:
        st.session_state.authenticated = True; st.rerun()
    elif user_pass: st.sidebar.error("WRONG PASSWORD")
    st.stop()

# 4. CSS STYLING
st.markdown("""<style>
    .stApp { background-color: #ffffff; color: #000000; font-size: 14px !important; }
    h1 { font-size: 28px !important; margin: 0px !important; padding-bottom: 10px !important; }
    .mini-box { background-color: #f0f2f6; border: 1px solid #dce1e6; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; }
    .mini-box b { font-size: 20px; color: #000; }
    .pivot-box { background-color: #fff3e0; border: 1px solid #ffe0b2; padding: 8px; border-radius: 5px; text-align: center; margin-bottom: 5px; }
    .buy-signal { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #28a745; margin: 10px 0; }
    .sell-signal { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #dc3545; margin: 10px 0; }
    .wait-signal { background-color: #e2e3e5; color: #383d41; padding: 10px; border-radius: 5px; text-align: center; font-size: 22px; font-weight: bold; border: 2px solid #d6d8db; margin: 10px 0; }
    .plan-box-buy { border: 2px solid #28a745; padding: 10px; border-radius: 8px; background-color: #f0fff4; color: #000; }
    .plan-box-sell { border: 2px solid #dc3545; padding: 10px; border-radius: 8px; background-color: #fff5f5; color: #000; }
    .reverse-warn { color: #ffffff; background-color: #ff0000; font-weight: bold; text-align: center; padding: 5px; border-radius: 4px; margin-top: 5px; }
    .sma-box { border: 1px solid #ddd; padding: 5px; border-radius: 5px; text-align: center; font-size: 12px; }
    div[data-testid="column"] button { padding: 5px 10px !important; min-height: 35px !important; }
</style>""", unsafe_allow_html=True)

# 5. DATA FUNCTIONS
STOCK_DICT = {"NIFTY 50":"^NSEI","BANK NIFTY":"^NSEBANK","FIN NIFTY":"NIFTY_FIN_SERVICE.NS","Reliance":"RELIANCE.NS","HDFC Bank":"HDFCBANK.NS","ICICI Bank":"ICICIBANK.NS","Infosys":"INFY.NS","TCS":"TCS.NS","ITC":"ITC.NS","L&T":"LT.NS","Axis Bank":"AXISBANK.NS","Kotak Bank":"KOTAKBANK.NS","SBI":"SBIN.NS","Bharti Airtel":"BHARTIARTL.NS","Bajaj Finance":"BAJFINANCE.NS","Asian Paints":"ASIANPAINT.NS","Maruti":"MARUTI.NS","HCL Tech":"HCLTECH.NS","Sun Pharma":"SUNPHARMA.NS","Titan":"TITAN.NS","M&M":"M&M.NS","UltraTech":"ULTRACEMCO.NS","Tata Steel":"TATASTEEL.NS","NTPC":"NTPC.NS","Power Grid":"POWERGRID.NS","Wipro":"WIPRO.NS","Adani Ent":"ADANIENT.NS","Adani Ports":"ADANIPORTS.NS","Tata Motors":"TATAMOTORS.NS","Coal India":"COALINDIA.NS","Hindalco":"HINDALCO.NS","Eicher Motors":"EICHERMOT.NS","Dr Reddy":"DRREDDY.NS","BPCL":"BPCL.NS","Nestle":"NESTLEIND.NS","Grasim":"GRASIM.NS","Hero Moto":"HEROMOTOCO.NS","Tech M":"TECHM.NS","Cipla":"CIPLA.NS","Apollo Hosp":"APOLLOHOSP.NS","Tata Cons":"TATACONSUM.NS","Divis Lab":"DIVISLAB.NS","Bajaj Auto":"BAJAJ-AUTO.NS","Jio Finance":"JIOFIN.NS","Trent":"TRENT.NS","BEL":"BEL.NS","HAL":"HAL.NS","Zomato":"ZOMATO.NS","DLF":"DLF.NS","Varun Bev":"VBL.NS","Siemens":"SIEMENS.NS","ABB":"ABB.NS","Indigo":"INDIGO.NS","Polycab":"POLYCAB.NS","REC":"REC.NS","PFC":"PFC.NS","Canara Bank":"CANBK.NS","PNB":"PNB.NS","Union Bank":"UNIONBANK.NS","Bank Baroda":"BANKBARODA.NS","IRFC":"IRFC.NS","RVNL":"RVNL.NS","Mazagon":"MAZDOCK.NS","Cochin Ship":"COCHINSHIP.NS","BHEL":"BHEL.NS","SAIL":"SAIL.NS","NMDC":"NMDC.NS","Vedanta":"VEDL.NS","Hind Zinc":"HINDZINC.NS","JSW Steel":"JSWSTEEL.NS","Jindal Steel":"JINDALSTEL.NS","Tata Power":"TATAPOWER.NS","Adani Power":"ADANIPOWER.NS","GAIL":"GAIL.NS","ONGC":"ONGC.NS","Oil India":"OIL.NS","Motherson":"MOTHERSON.NS","Bosch":"BOSCHLTD.NS","TVS Motor":"TVSMOTOR.NS","MRF":"MRF.NS","Samvardhana":"MOTHERSON.NS"}
SYMBOL_TO_NAME = {v: k for k, v in STOCK_DICT.items()}

@st.cache_data(ttl=60)
def get_data(t):
    try:
        s=yf.Ticker(t); h=s.history(period="1y")
        if h.empty: return None, None
        return h['Close'].iloc[-1], h
    except: return None,None

def get_techs(h):
    if len(h)<200: return 50,0,"Neutral",0,0,0,0,0,0,0,0,0,0,0,0,0
    
    d=h['Close'].diff(); g=(d.where(d>0,0)).rolling(14).mean(); l=(-d.where(d<0,0)).rolling(14).mean()
    h
