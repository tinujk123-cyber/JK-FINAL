import streamlit as st
import yfinance as yf
import pandas as pd
import math
import urllib.parse
import urllib.request
import time
import smtplib
from email.mime.text import MIMEText

# ---------------------------------------------------------
# 1. APP CONFIGURATION & CSS
# ---------------------------------------------------------
st.set_page_config(page_title="JK TRINETRA", layout="wide")
ACCESS_PASSWORD = "JK2026"

# Session State
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'watchlist' not in st.session_state: st.session_state.watchlist = []

# Styling (THE OLD DASHBOARD STYLE)
st.markdown("""<style>
    .mini-box { background-color: #f0f2f6; border: 1px solid #dce1e6; padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 8px; }
    .mini-box b { font-size: 20px; color: #000; }
    .pivot-box { background-color: #fff3e0; border: 1px solid #ffe0b2; padding: 8px; border-radius: 5px; text-align: center; margin-bottom: 5px; }
    .buy-signal { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; font-size: 22px; border: 2px solid #28a745; margin: 10px 0px; }
    .sell-signal { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; font-size: 22px; border: 2px solid #dc3545; margin: 10px 0px; }
    .wait-signal { background-color: #e2e3e5; color: #383d41; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; font-size: 22px; border: 2px solid #d6d8db; margin: 10px 0px; }
    .plan-box-buy { border: 2px solid #28a745; padding: 10px; border-radius: 8px; background-color: #f0fff4; color: #000; font-size: 15px; }
    .plan-box-sell { border: 2px solid #dc3545; padding: 10px; border-radius: 8px; background-color: #fff5f5; color: #000; font-size: 15px; }
    .reverse-warn { color: #ffffff; background-color: #ff0000; font-weight: bold; text-align: center; padding: 5px; border-radius: 4px; margin-top: 5px; }
    .sma-box { border: 1px solid #ddd; padding: 5px; border-radius: 5px; text-align: center; font-size: 12px; }
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

def send_email(sender_email, app_password, receiver_email, subject, body):
    if not sender_email or not app_password or not receiver_email: return
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        # Connect to Gmail Server (Change if using Yahoo/Outlook)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, app_password)
            smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Email Failed: {e}")

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
    m_res = h['High'].iloc[-30:].max(); m_sup = h['Low'].iloc[-30:].min()
    pd = h.iloc[-2]; p_dp = (pd['High']+pd['Low']+pd['Close'])/3
    r1 = (2*p_dp)-pd['Low']; s1 = (2*p_dp)-pd['High']
    r2 = p_dp + (pd['High']-pd['Low']); s2 = p_dp - (pd['High']-pd['Low'])
    sma10 = h['Close'].rolling(10).mean().iloc[-1]; sma20 = h['Close'].rolling(20).mean().iloc[-1]
    sma50 = h['Close'].rolling(50).mean().iloc[-1]; sma100 = h['Close'].rolling(100).mean().iloc[-1]
    sma200 = h['Close'].rolling(200).mean().iloc[-1]
    return h['RSI'].iloc[-1], h['Close'].rolling(20).mean().iloc[-1], smc, adx, m_res, m_sup, r1, s1, r2, s2, sma10, sma20, sma50, sma100, sma200

def analyze(t):
    l,h=get_data(t)
    if l is None: return None
    pd_=h.iloc[-2]; td=h.iloc[-1]; dp=(pd_['High']+pd_['Low']+pd_['Close'])/3; vw=(td['High']+td['Low']+td['Close'])/3
    rsi,sma,smc,adx,m_res,m_sup,r1,s1,r2,s2,sma10,sma20,sma50,sma100,sma200 = get_techs(h)
    
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
# 3. AUTH & NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("JK TRINETRA 🔱")

if not st.session_state.authenticated:
    pwd = st.sidebar.text_input("ENTER PASSWORD:", type="password")
    if pwd == ACCESS_PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    elif pwd: st.sidebar.error("ACCESS DENIED")
    st.stop()

page = st.sidebar.radio("CHOOSE MODE:", ["📊 DASHBOARD (Charts)", "🚨 LIVE SCANNER (Alerts)"])

# ---------------------------------------------------------
# PAGE 1: THE OLD DASHBOARD STYLE (Restored)
# ---------------------------------------------------------
if page == "📊 DASHBOARD (Charts)":
    
    # Stock Selection
    c1, c2 = st.columns([1, 2])
    with c1: sel_stock = st.selectbox("SELECT STOCK:", list(STOCK_DICT.keys()))
    with c2: man_stock = st.text_input("OR TYPE SYMBOL (Ex: TRENT):")
    final_stock = man_stock.upper() if man_stock else sel_stock
    ticker = STOCK_DICT.get(final_stock, final_stock + ".NS")
    
    # Get Data
    r = analyze(ticker)
    
    if r:
        st.title(f"{final_stock} | Rs. {round(r['LTP'],2)}")
        
        # Signal Banner
        sc = "wait-signal"; txt = "WAIT MODE"
        if r['Signal']=="BUY": sc="buy-signal"; txt="BUY CONFIRMED"
        elif r['Signal']=="SELL": sc="sell-signal"; txt="SELL CONFIRMED"
        st.markdown(f"<div class='{sc}'>{txt}</div>", unsafe_allow_html=True)

        # ROW 1: Basic Info
        k1,k2,k3,k4 = st.columns(4)
        k1.markdown(f"<div class='mini-box'>LTP<br><b>{round(r['LTP'],2)}</b></div>", unsafe_allow_html=True)
        smc_color = "green" if "BUILDUP" in r['SMC'] else "red"
        k2.markdown(f"<div class='mini-box'>SMART MONEY<br><b style='color:{smc_color}'>{r['SMC']}</b></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='mini-box'>VWAP<br><b>{round(r['VWAP'],2)}</b></div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='mini-box'>TREND (50 SMA)<br><b>{r['Trend']}</b></div>", unsafe_allow_html=True)

        # ROW 2: High/Low
        h1,h2,h3,h4 = st.columns(4)
        h1.markdown(f"<div class='mini-box'>TODAY HIGH<br><b>{round(r['TodayHigh'],2)}</b></div>", unsafe_allow_html=True)
        h2.markdown(f"<div class='mini-box'>TODAY LOW<br><b>{round(r['TodayLow'],2)}</b></div>", unsafe_allow_html=True)
        h3.markdown(f"<div class='mini-box'>PREV HIGH<br><b>{round(r['PrevHigh'],2)}</b></div>", unsafe_allow_html=True)
        h4.markdown(f"<div class='mini-box'>PREV LOW<br><b>{round(r['PrevLow'],2)}</b></div>", unsafe_allow_html=True)

        # ROW 3: Pivots
        p1,p2,p3,p4,p5 = st.columns(5)
        p1.markdown(f"<div class='pivot-box'>S2<br><b>{round(r['S2'],2)}</b></div>", unsafe_allow_html=True)
        p2.markdown(f"<div class='pivot-box'>S1<br><b>{round(r['S1'],2)}</b></div>", unsafe_allow_html=True)
        p3.markdown(f"<div class='pivot-box' style='background-color:#fff;'>PIVOT<br><b>{round(r['DP'],2)}</b></div>", unsafe_allow_html=True)
        p4.markdown(f"<div class='pivot-box'>R1<br><b>{round(r['R1'],2)}</b></div>", unsafe_allow_html=True)
        p5.markdown(f"<div class='pivot-box'>R2<br><b>{round(r['R2'],2)}</b></div>", unsafe_allow_html=True)
        
        # ROW 4: Moving Averages
        st.markdown("<b>KEY MOVING AVERAGES</b>", unsafe_allow_html=True)
        s_col1, s_col2, s_col3, s_col4, s_col5 = st.columns(5)
        sma = r['SMA']
        def sma_clr(val): return "green" if r['LTP'] > val else "red"
        s_col1.markdown(f"<div class='sma-box'>10 SMA<br><b style='color:{sma_clr(sma[0])}'>{round(sma[0],2)}</b></div>", unsafe_allow_html=True)
        s_col2.markdown(f"<div class='sma-box'>20 SMA<br><b style='color:{sma_clr(sma[1])}'>{round(sma[1],2)}</b></div>", unsafe_allow_html=True)
        s_col3.markdown(f"<div class='sma-box'>50 SMA<br><b style='color:{sma_clr(sma[2])}'>{round(sma[2],2)}</b></div>", unsafe_allow_html=True)
        s_col4.markdown(f"<div class='sma-box'>100 SMA<br><b style='color:{sma_clr(sma[3])}'>{round(sma[3],2)}</b></div>", unsafe_allow_html=True)
        s_col5.markdown(f"<div class='sma-box'>200 SMA<br><b style='color:{sma_clr(sma[4])}'>{round(sma[4],2)}</b></div>", unsafe_allow_html=True)

        # GANN LEVELS
        tg = r['Tgts']
        cb,cs = st.columns(2)
        with cb:
            st.markdown(f"<div class='plan-box-buy'><b>BUY ENTRY: {r['Entry']}</b> | SL: {r['SL']}<hr>T1: {tg[0]} | T2: {tg[1]}<br>T3: {tg[2]} | T4: {tg[3]}<br><b>FINAL TARGET: {tg[4]}</b></div>", unsafe_allow_html=True)
        with cs:
            st.markdown(f"<div class='plan-box-sell'><b>SELL ENTRY: {r['Entry']}</b> | SL: {r['SL']}<hr>T1: {tg[0]} | T2: {tg[1]}<br>T3: {tg[2]} | T4: {tg[3]}<br><b>FINAL TARGET: {tg[4]}</b></div>", unsafe_allow_html=True)

    else:
        st.error("STOCK NOT FOUND")

# ---------------------------------------------------------
# PAGE 2: LIVE SCANNER (Auto-Refresh + Email)
# ---------------------------------------------------------
elif page == "🚨 LIVE SCANNER (Alerts)":
    st.title("🚨 LIVE WATCHLIST SCANNER")
    st.info("THIS PAGE AUTO-REFRESHES. OPEN THIS IN A SEPARATE TAB.")
    
    # Watchlist
    new_w = st.multiselect("EDIT WATCHLIST:", list(STOCK_DICT.keys()), default=st.session_state.watchlist)
    st.session_state.watchlist = new_w
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📱 WhatsApp Config")
        wa_phone = st.text_input("Your Phone (Optional):", value="91")
        wa_api = st.text_input("CallMeBot API (Optional):")
    with c2:
        st.subheader("📧 Email Config")
        st.warning("Needs 'App Password' from Gmail settings.")
        sender = st.text_input("Your Email (Gmail):")
        app_pass = st.text_input("App Password:", type="password")
        receiver = st.text_input("Receiver Email:")

    if st.button("🚀 START AUTO-SCAN"):
        if not new_w: st.error("WATCHLIST EMPTY")
        else:
            status = st.empty(); result = st.empty()
            while True:
                status.markdown(f"### ⏳ SCANNING... ({time.strftime('%H:%M:%S')})")
                
                scan_res = []
                alert_msg = ""
                
                for s_name in new_w:
                    tk = STOCK_DICT.get(s_name, s_name+".NS")
                    d = analyze(tk)
                    if d:
                        rev = ""
                        ba = d['DP'] * 1.001; t5_b = (math.sqrt(ba) + (5 * 0.125))**2
                        sb = d['DP'] * 0.999; t5_s = (math.sqrt(sb) - (5 * 0.125))**2
                        if d['LTP'] >= t5_b: rev = "TOP REVERSAL"
                        elif d['LTP'] <= t5_s: rev = "BOTTOM REVERSAL"
                        
                        sig_type = d['Signal']
                        if rev: sig_type += f" | {rev}"
                        
                        scan_res.append({"STOCK": s_name, "LTP": round(d['LTP'],2), "SIGNAL": sig_type})
                        
                        if d['Signal'] != "WAIT" or rev:
                            alert_msg += f"{s_name}: {sig_type} @ {d['LTP']}\n"
                
                # Show Table
                df = pd.DataFrame(scan_res)
                result.dataframe(df, use_container_width=True)
                
                # Send Alerts
                if alert_msg:
                    # WhatsApp
                    if wa_phone and wa_api:
                        send_whatsapp(wa_phone, wa_api, f"JK ALERT:\n{alert_msg}")
                    # Email
                    if sender and app_pass and receiver:
                        send_email(sender, app_pass, receiver, "JK TRINETRA ALERT", alert_msg)
                        st.toast("Email Sent!", icon="📧")

                time.sleep(900) # 15 Mins
