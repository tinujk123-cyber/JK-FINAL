import streamlit as st
import yfinance as yf
import pandas as pd
import math
import urllib.parse
import urllib.request
import time

# ---------------------------------------------------------
# 1. APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="JK TRINETRA", layout="wide")
ACCESS_PASSWORD = "JK2026"

# Session State
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'watchlist' not in st.session_state: st.session_state.watchlist = []

# CSS Styling
st.markdown("""<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .success-box { padding:15px; background-color:#d4edda; color:#155724; border-radius:10px; border:1px solid #c3e6cb; text-align:center; margin-bottom:10px; }
    .fail-box { padding:15px; background-color:#f8d7da; color:#721c24; border-radius:10px; border:1px solid #f5c6cb; text-align:center; margin-bottom:10px; }
    .info-box { padding:10px; background-color:#e2e3e5; color:#383d41; border-radius:10px; text-align:center; }
    div[data-testid="stSidebarNav"] {display: none;}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. FUNCTIONS (Logic)
# ---------------------------------------------------------
STOCK_DICT = {"NIFTY 50":"^NSEI","BANK NIFTY":"^NSEBANK","FIN NIFTY":"NIFTY_FIN_SERVICE.NS","Reliance":"RELIANCE.NS","HDFC Bank":"HDFCBANK.NS","ICICI Bank":"ICICIBANK.NS","Infosys":"INFY.NS","TCS":"TCS.NS","ITC":"ITC.NS","L&T":"LT.NS","Axis Bank":"AXISBANK.NS","Kotak Bank":"KOTAKBANK.NS","SBI":"SBIN.NS","Bharti Airtel":"BHARTIARTL.NS","Bajaj Finance":"BAJFINANCE.NS","Asian Paints":"ASIANPAINT.NS","Maruti":"MARUTI.NS","HCL Tech":"HCLTECH.NS","Sun Pharma":"SUNPHARMA.NS","Titan":"TITAN.NS","M&M":"M&M.NS","UltraTech":"ULTRACEMCO.NS","Tata Steel":"TATASTEEL.NS","NTPC":"NTPC.NS","Power Grid":"POWERGRID.NS","Wipro":"WIPRO.NS","Adani Ent":"ADANIENT.NS","Adani Ports":"ADANIPORTS.NS","Tata Motors":"TATAMOTORS.NS","Coal India":"COALINDIA.NS","Hindalco":"HINDALCO.NS","Eicher Motors":"EICHERMOT.NS","Dr Reddy":"DRREDDY.NS","BPCL":"BPCL.NS","Nestle":"NESTLEIND.NS","Grasim":"GRASIM.NS","Hero Moto":"HEROMOTOCO.NS","Tech M":"TECHM.NS","Cipla":"CIPLA.NS","Apollo Hosp":"APOLLOHOSP.NS","Tata Cons":"TATACONSUM.NS","Divis Lab":"DIVISLAB.NS","Bajaj Auto":"BAJAJ-AUTO.NS","Jio Finance":"JIOFIN.NS","Trent":"TRENT.NS","BEL":"BEL.NS","HAL":"HAL.NS","Zomato":"ZOMATO.NS","DLF":"DLF.NS","Varun Bev":"VBL.NS","Siemens":"SIEMENS.NS","ABB":"ABB.NS","Indigo":"INDIGO.NS","Polycab":"POLYCAB.NS","REC":"REC.NS","PFC":"PFC.NS","Canara Bank":"CANBK.NS","PNB":"PNB.NS","Union Bank":"UNIONBANK.NS","Bank Baroda":"BANKBARODA.NS","IRFC":"IRFC.NS","RVNL":"RVNL.NS","Mazagon":"MAZDOCK.NS","Cochin Ship":"COCHINSHIP.NS","BHEL":"BHEL.NS","SAIL":"SAIL.NS","NMDC":"NMDC.NS","Vedanta":"VEDL.NS","Hind Zinc":"HINDZINC.NS","JSW Steel":"JSWSTEEL.NS","Jindal Steel":"JINDALSTEL.NS","Tata Power":"TATAPOWER.NS","Adani Power":"ADANIPOWER.NS","GAIL":"GAIL.NS","ONGC":"ONGC.NS","Oil India":"OIL.NS","Motherson":"MOTHERSON.NS","Bosch":"BOSCHLTD.NS","TVS Motor":"TVSMOTOR.NS","MRF":"MRF.NS","Samvardhana":"MOTHERSON.NS"}
SYMBOL_TO_NAME = {v: k for k, v in STOCK_DICT.items()}

def send_whatsapp(phone, apikey, message):
    if not phone or not apikey: return
    try:
        encoded_msg = urllib.parse.quote(message)
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_msg}&apikey={apikey}"
        urllib.request.urlopen(url)
    except: pass

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
    h['RSI'] = 100-(100/(1+(g/l)))
    v_avg = h['Volume'].rolling(10).mean().iloc[-1]; v_now = h['Volume'].iloc[-1]
    pc = h['Close'].iloc[-1] - h['Close'].iloc[-2]
    if pc > 0 and v_now > v_avg: smc = "LONG BUILDUP"
    elif pc < 0 and v_now > v_avg: smc = "SHORT BUILDUP"
    elif pc > 0 and v_now < v_avg: smc = "SHORT COVERING"
    elif pc < 0 and v_now < v_avg: smc = "LONG UNWINDING"
    else: smc = "NEUTRAL"
    dx=100*abs((100*(h['High']-h['High'].shift(1)).rolling(14).mean()/h['Close'].rolling(14).mean())-(100*(h['Low'].shift(1)-h['Low']).rolling(14).mean()/h['Close'].rolling(14).mean()))/((100*(h['High']-h['High'].shift(1)).rolling(14).mean()/h['Close'].rolling(14).mean())+(100*(h['Low'].shift(1)-h['Low']).rolling(14).mean()/h['Close'].rolling(14).mean()))
    adx=dx.rolling(14).mean().iloc[-1]
    pd = h.iloc[-2]; p_dp = (pd['High']+pd['Low']+pd['Close'])/3
    r1 = (2*p_dp)-pd['Low']; s1 = (2*p_dp)-pd['High']
    r2 = p_dp + (pd['High']-pd['Low']); s2 = p_dp - (pd['High']-pd['Low'])
    sma10 = h['Close'].rolling(10).mean().iloc[-1]; sma20 = h['Close'].rolling(20).mean().iloc[-1]
    sma50 = h['Close'].rolling(50).mean().iloc[-1]; sma100 = h['Close'].rolling(100).mean().iloc[-1]
    sma200 = h['Close'].rolling(200).mean().iloc[-1]
    return h['RSI'].iloc[-1], h['Close'].rolling(20).mean().iloc[-1], smc, adx, r1, s1, r2, s2, sma10, sma20, sma50, sma100, sma200

def analyze(t):
    l,h=get_data(t)
    if l is None: return None
    pd_=h.iloc[-2]; td=h.iloc[-1]; dp=(pd_['High']+pd_['Low']+pd_['Close'])/3; vw=(td['High']+td['Low']+td['Close'])/3
    rsi,sma,smc,adx,r1,s1,r2,s2,sma10,sma20,sma50,sma100,sma200 = get_techs(h)
    
    sig="WAIT"; trend = "SIDEWAYS"
    if l > sma50: trend = "BULLISH"
    elif l < sma50: trend = "BEARISH"

    if l>dp and l>vw and l>pd_['Low']: sig="BUY"
    elif l<dp and l<vw and l<pd_['High']: sig="SELL"
    
    targets = []
    if sig == "BUY":
        entry = round(dp * 1.001, 2); sl = round(pd_['Low'], 2)
        for i in range(1,6): targets.append(round((math.sqrt(entry) + (i*0.125))**2, 2))
    elif sig == "SELL":
        entry = round(dp * 0.999, 2); sl = round(pd_['High'], 2)
        for i in range(1,6): targets.append(round((math.sqrt(entry) - (i*0.125))**2, 2))
    else: entry=0; sl=0; targets=[0]*5

    return {
        "Symbol":t, "LTP":l, "Signal":sig, "SMC":smc, "Trend":trend, "VWAP":vw,
        "Entry":entry, "SL":sl, "Tgts":targets, "S1":s1, "S2":s2, "R1":r1, "R2":r2, "DP":dp,
        "SMA": [sma10, sma20, sma50, sma100, sma200], "TodayHigh":td['High'], "TodayLow":td['Low'],
        "PrevHigh":pd_['High'], "PrevLow":pd_['Low'], "RSI":rsi, "ADX":adx
    }

# ---------------------------------------------------------
# 3. AUTHENTICATION & NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("JK TRINETRA 🔱")

if not st.session_state.authenticated:
    pwd = st.sidebar.text_input("ENTER PASSWORD:", type="password")
    if pwd == ACCESS_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    elif pwd:
        st.sidebar.error("ACCESS DENIED")
    st.title("🔒 SYSTEM LOCKED")
    st.info("Please enter the password in the sidebar.")
    st.stop()

# PAGE SELECTION
page = st.sidebar.radio("CHOOSE MODE:", ["📊 DASHBOARD", "🚨 LIVE SCANNER"])

# ---------------------------------------------------------
# PAGE 1: DASHBOARD (ANALYSIS)
# ---------------------------------------------------------
if page == "📊 DASHBOARD":
    st.title("📊 JK TRINETRA: DASHBOARD")
    
    # Selection
    c1, c2 = st.columns([1, 2])
    with c1:
        sel_stock = st.selectbox("SELECT STOCK:", list(STOCK_DICT.keys()))
    with c2:
        man_stock = st.text_input("OR TYPE SYMBOL (Ex: TRENT):")
    
    final_stock = man_stock.upper() if man_stock else sel_stock
    ticker = STOCK_DICT.get(final_stock, final_stock + ".NS")
    
    r = analyze(ticker)
    
    if r:
        # SIGNAL BANNER
        if r['Signal'] == "BUY":
            st.markdown(f"<div class='success-box'><h1 style='margin:0'>BUY CONFIRMED</h1>LTP: {round(r['LTP'],2)} | TREND: {r['Trend']}</div>", unsafe_allow_html=True)
        elif r['Signal'] == "SELL":
            st.markdown(f"<div class='fail-box'><h1 style='margin:0'>SELL CONFIRMED</h1>LTP: {round(r['LTP'],2)} | TREND: {r['Trend']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='info-box'><h1 style='margin:0'>WAIT / NO SIGNAL</h1>LTP: {round(r['LTP'],2)} | TREND: {r['Trend']}</div>", unsafe_allow_html=True)

        # DATA GRID
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("LTP", round(r['LTP'],2))
        k2.metric("VWAP", round(r['VWAP'],2))
        k3.metric("SMART MONEY", r['SMC'])
        k4.metric("ADX Strength", round(r['ADX'],2))

        # GANN LEVELS
        st.subheader("🎯 GANN PROJECTION & LEVELS")
        g1, g2 = st.columns(2)
        with g1:
            st.info(f"**🟢 BUY ZONE**\n\n**ENTRY:** {r['Entry']}\n\n**SL:** {r['SL']}\n\n**T1:** {r['Tgts'][0]} | **T2:** {r['Tgts'][1]}\n\n**FINAL:** {r['Tgts'][4]}")
        with g2:
            st.error(f"**🔴 SELL ZONE**\n\n**ENTRY:** {r['Entry']}\n\n**SL:** {r['SL']}\n\n**T1:** {r['Tgts'][0]} | **T2:** {r['Tgts'][1]}\n\n**FINAL:** {r['Tgts'][4]}")

    else:
        st.error("Data not found. Please check symbol.")

# ---------------------------------------------------------
# PAGE 2: LIVE SCANNER (AUTOMATION)
# ---------------------------------------------------------
elif page == "🚨 LIVE SCANNER":
    st.title("🚨 LIVE WATCHLIST SCANNER")
    st.info("This screen will AUTO-REFRESH every 15 mins to check for signals.")
    
    # Watchlist Manager
    default_w = st.session_state.watchlist
    new_w = st.multiselect("EDIT WATCHLIST:", list(STOCK_DICT.keys()), default=default_w)
    st.session_state.watchlist = new_w
    
    # WhatsApp Config
    c_w1, c_w2 = st.columns(2)
    phone = c_w1.text_input("WhatsApp Phone (Optional):", value="91")
    api = c_w2.text_input("CallMeBot API Key (Optional):")
    
    if st.button("🚀 START AUTO-SCAN"):
        if not new_w:
            st.error("WATCHLIST IS EMPTY!")
        else:
            status_box = st.empty()
            result_box = st.empty()
            
            # THE LOOP
            while True:
                status_box.markdown(f"### ⏳ SCANNING {len(new_w)} STOCKS... ({time.strftime('%H:%M:%S')})")
                
                scan_res = []
                wa_msg = ""
                
                for s_name in new_w:
                    tk = STOCK_DICT.get(s_name, s_name+".NS")
                    d = analyze(tk)
                    if d:
                        # Logic for Reversal
                        rev = ""
                        ba = d['DP'] * 1.001; t5_b = (math.sqrt(ba) + (5 * 0.125))**2
                        sb = d['DP'] * 0.999; t5_s = (math.sqrt(sb) - (5 * 0.125))**2
                        if d['LTP'] >= t5_b: rev = "TOP REVERSAL"
                        elif d['LTP'] <= t5_s: rev = "BOTTOM REVERSAL"
                        
                        sig_type = d['Signal']
                        if rev: sig_type += f" | {rev}"
                        
                        scan_res.append({
                            "STOCK": s_name,
                            "LTP": round(d['LTP'],2),
                            "SIGNAL": sig_type,
                            "TREND": d['Trend']
                        })
                        
                        if d['Signal'] != "WAIT" or rev:
                            wa_msg += f"*{s_name}*: {sig_type} @ {d['LTP']}\n"
                
                # Show Table
                df = pd.DataFrame(scan_res)
                result_box.dataframe(df, use_container_width=True)
                
                # Send WhatsApp
                if wa_msg and phone and api:
                    send_whatsapp(phone, api, f"JK ALERT:\n{wa_msg}")
                    st.toast("Alert Sent to WhatsApp!", icon="✅")
                
                time.sleep(900) # Wait 15 mins
