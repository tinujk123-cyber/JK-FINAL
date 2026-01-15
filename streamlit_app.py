import streamlit as st
import yfinance as yf
import pandas as pd
import math

# ---------------------------------------------------------
# 1. APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="JK TRINETRA", layout="wide")
ACCESS_PASSWORD = "JK2026"

# 2. SESSION STATE
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'selected_stock' not in st.session_state: st.session_state.selected_stock = "NIFTY 50"
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

# 4. COMPACT CSS STYLING (SMALLER & TIGHTER)
st.markdown("""<style>
    .stApp { background-color: #ffffff; color: #000000; font-size: 12px !important; }
    h1 { font-size: 22px !important; margin: 0px !important; padding-bottom: 5px !important; }
    div.block-container { padding-top: 2rem !important; padding-bottom: 1rem !important; }
    .mini-box { background-color: #f0f2f6; border: 1px solid #dce1e6; padding: 5px; border-radius: 6px; text-align: center; font-size: 12px; margin-bottom: 4px; }
    .mini-box b { font-size: 16px; color: #000; font-weight: 700; }
    .pivot-box { background-color: #fff3e0; border: 1px solid #ffe0b2; padding: 4px; border-radius: 4px; text-align: center; font-size: 11px; margin-bottom: 3px; }
    .pivot-box b { font-size: 14px; }
    .buy-signal { background-color: #d4edda; color: #155724; padding: 5px; border-radius: 5px; text-align: center; font-size: 18px; font-weight: bold; border: 1px solid #28a745; margin: 5px 0; }
    .sell-signal { background-color: #f8d7da; color: #721c24; padding: 5px; border-radius: 5px; text-align: center; font-size: 18px; font-weight: bold; border: 1px solid #dc3545; margin: 5px 0; }
    .wait-signal { background-color: #e2e3e5; color: #383d41; padding: 5px; border-radius: 5px; text-align: center; font-size: 18px; font-weight: bold; border: 1px solid #d6d8db; margin: 5px 0; }
    .plan-box-buy { border: 1px solid #28a745; padding: 6px; border-radius: 6px; background-color: #f0fff4; color: #000; font-size: 13px; }
    .plan-box-sell { border: 1px solid #dc3545; padding: 6px; border-radius: 6px; background-color: #fff5f5; color: #000; font-size: 13px; }
    .reverse-warn { color: #ffffff; background-color: #ff0000; font-weight: bold; text-align: center; padding: 2px; border-radius: 3px; font-size: 11px; margin-top: 3px; }
    .sma-box { border: 1px solid #ddd; padding: 3px; border-radius: 4px; text-align: center; font-size: 11px; }
    .sma-box b { font-size: 13px; }
    hr { margin: 3px 0px !important; }
    div[data-testid="column"] button { padding: 2px 8px !important; min-height: 28px !important; font-size: 12px !important; }
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
    h['RSI'] = 100-(100/(1+(g/l)))
    v_avg = h['Volume'].rolling(10).mean().iloc[-1]; v_now = h['Volume'].iloc[-1]
    pc = h['Close'].iloc[-1] - h['Close'].iloc[-2]
    
    if pc > 0 and v_now > v_avg: smc = "LONG BUILDUP"
    elif pc < 0 and v_now > v_avg: smc = "SHORT BUILDUP"
    elif pc > 0 and v_now < v_avg: smc = "SHORT COVERING"
    elif pc < 0 and v_now < v_avg: smc = "LONG UNWINDING"
    else: smc = "NEUTRAL"

    h['H-L']=h['High']-h['Low']; h['H-C']=abs(h['High']-h['Close'].shift(1)); h['L-C']=abs(h['Low']-h['Close'].shift(1))
    h['TR']=h[['H-L','H-C','L-C']].max(axis=1)
    h['UM']=h['High']-h['High'].shift(1); h['DM']=h['Low'].shift(1)-h['Low']; h['+DM']=0; h['-DM']=0
    h.loc[(h['UM']>h['DM'])&(h['UM']>0),'+DM']=h['UM']; h.loc[(h['DM']>h['UM'])&(h['DM']>0),'-DM']=h['DM']
    tr=h['TR'].rolling(14).mean(); pdi=100*(h['+DM'].rolling(14).mean()/tr); mdi=100*(h['-DM'].rolling(14).mean()/tr)
    dx=100*abs(pdi-mdi)/(pdi+mdi); adx=dx.rolling(14).mean().iloc[-1]

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

# 6. SIDEBAR CONTROLS
st.sidebar.header("CONTROLS")
selected_name = st.sidebar.selectbox("SELECT FROM LIST:", list(STOCK_DICT.keys()), index=list(STOCK_DICT.keys()).index(st.session_state.selected_stock) if st.session_state.selected_stock in STOCK_DICT else 0)

manual_search = st.sidebar.text_input("OR TYPE SYMBOL (Ex: TRENT):")
if manual_search: st.session_state.selected_stock = manual_search.upper()
else: st.session_state.selected_stock = selected_name

if st.sidebar.button("REFRESH DATA"): st.cache_data.clear(); st.rerun()

st.sidebar.subheader("MANUAL SCANNER")
c_s1, c_s2 = st.sidebar.columns(2)
f_list = [v for k,v in STOCK_DICT.items() if not k.endswith("NIFTY")]

if c_s1.button("BUY SCAN"):
    st.session_state.scan_buy_list = []; st.session_state.scan_sell_list = []; st.session_state.scan_rev_list = []
    for s in f_list:
        r=analyze(s)
        if r and r["Signal"]=="BUY": st.session_state.scan_buy_list.append(r)
    st.rerun()

if c_s2.button("SELL SCAN"):
    st.session_state.scan_buy_list = []; st.session_state.scan_sell_list = []; st.session_state.scan_rev_list = []
    for s in f_list:
        r=analyze(s)
        if r and r["Signal"]=="SELL": st.session_state.scan_sell_list.append(r)
    st.rerun()

if st.sidebar.button("REVERSAL SCAN"):
    st.session_state.scan_buy_list = []; st.session_state.scan_sell_list = []; st.session_state.scan_rev_list = []
    for s in f_list:
        l, h = get_data(s)
        if l is not None:
            pd = h.iloc[-2]; dp = (pd['High']+pd['Low']+pd['Close'])/3
            ba = dp * 1.001; sb = dp * 0.999
            t5_b = (math.sqrt(ba) + (5 * 0.125))**2
            t5_s = (math.sqrt(sb) - (5 * 0.125))**2
            if l >= t5_b: st.session_state.scan_rev_list.append({"Symbol":s, "LTP":l, "Type":"TOP (SELL)"})
            elif l <= t5_s: st.session_state.scan_rev_list.append({"Symbol":s, "LTP":l, "Type":"BOTTOM (BUY)"})
    st.rerun()

if st.session_state.scan_buy_list:
    st.sidebar.success(f"Found {len(st.session_state.scan_buy_list)} BUY")
    for i, item in enumerate(st.session_state.scan_buy_list):
        name = SYMBOL_TO_NAME.get(item['Symbol'], item['Symbol'])
        if st.sidebar.button(f"{name} ({round(item['LTP'],1)})", key=f"btn_buy_{i}"): 
            st.session_state.selected_stock = name; st.rerun()

if st.session_state.scan_sell_list:
    st.sidebar.error(f"Found {len(st.session_state.scan_sell_list)} SELL")
    for i, item in enumerate(st.session_state.scan_sell_list):
        name = SYMBOL_TO_NAME.get(item['Symbol'], item['Symbol'])
        if st.sidebar.button(f"{name} ({round(item['LTP'],1)})", key=f"btn_sell_{i}"): 
            st.session_state.selected_stock = name; st.rerun()

if st.session_state.scan_rev_list:
    st.sidebar.warning(f"Found {len(st.session_state.scan_rev_list)} REVERSAL")
    for i, item in enumerate(st.session_state.scan_rev_list):
        name = SYMBOL_TO_NAME.get(item['Symbol'], item['Symbol'])
        if st.sidebar.button(f"{name} [{item['Type']}]", key=f"btn_rev_{i}"): 
            st.session_state.selected_stock = name; st.rerun()

# 7. DASHBOARD DISPLAY
if st.session_state.selected_stock in STOCK_DICT: ticker = STOCK_DICT[st.session_state.selected_stock]
else: ticker = st.session_state.selected_stock + ".NS"

ltp = None
hist = None
ltp, hist = get_data(ticker)
price_txt = f"| Rs. {round(ltp,2)}" if ltp else ""
st.title(f"{st.session_state.selected_stock} {price_txt}")

if ltp is not None and hist is not None:
    pd_=hist.iloc[-2]; td=hist.iloc[-1]; dp=(pd_['High']+pd_['Low']+pd_['Close'])/3; vw=(td['High']+td['Low']+td['Close'])/3
    rsi,sma,smc,adx,r1,s1,r2,s2,sma10,sma20,sma50,sma100,sma200 = get_techs(hist)
    r = analyze(ticker) 
    
    # 1. SIGNAL BANNER
    sc = "wait-signal"; txt = "WAIT MODE"
    if r['Signal']=="BUY": sc="buy-signal"; txt="BUY CONFIRMED"
    elif r['Signal']=="SELL": sc="sell-signal"; txt="SELL CONFIRMED"
    st.markdown(f"<div class='{sc}'>{txt}</div>", unsafe_allow_html=True)

    # 2. DATA GRID
    k1,k2,k3,k4 = st.columns(4)
    
    html_ltp = f"<div class='mini-box'>LTP<br><b>Rs. {round(ltp,2)}</b></div>"
    k1.markdown(html_ltp, unsafe_allow_html=True)
    
    smc_color = "green" if "BUILDUP" in smc else ("red" if "UNWINDING" in smc else "orange")
    if "SHORT BUILDUP" in smc: smc_color = "red"
    html_smc = f"<div class='mini-box'>SMART MONEY<br><b style='color:{smc_color}'>{smc}</b></div>"
    k2.markdown(html_smc, unsafe_allow_html=True)
    
    html_vwap = f"<div class='mini-box'>VWAP<br><b>{round(vw,2)}</b></div>"
    k3.markdown(html_vwap, unsafe_allow_html=True)
    
    trend_txt = "UPTREND (Above 50 SMA)" if ltp > sma50 else "DOWNTREND (Below 50 SMA)"
    html_trend = f"<div class='mini-box'>TREND (50 SMA)<br><b>{trend_txt}</b></div>"
    k4.markdown(html_trend, unsafe_allow_html=True)

    # 3. HIGH / LOW GRID
    h1,h2,h3,h4 = st.columns(4)
    h1.markdown(f"<div class='mini-box'>TODAY HIGH<br><b>{round(td['High'],2)}</b></div>", unsafe_allow_html=True)
    h2.markdown(f"<div class='mini-box'>TODAY LOW<br><b>{round(td['Low'],2)}</b></div>", unsafe_allow_html=True)
    h3.markdown(f"<div class='mini-box'>PREV HIGH<br><b>{round(pd_['High'],2)}</b></div>", unsafe_allow_html=True)
    h4.markdown(f"<div class='mini-box'>PREV LOW<br><b>{round(pd_['Low'],2)}</b></div>", unsafe_allow_html=True)

    # 4. PIVOTS
    p1,p2,p3,p4,p5 = st.columns(5)
    p1.markdown(f"<div class='pivot-box'>S2<br><b>{round(s2,2)}</b></div>", unsafe_allow_html=True)
    p2.markdown(f"<div class='pivot-box'>S1<br><b>{round(s1,2)}</b></div>", unsafe_allow_html=True)
    p3.markdown(f"<div class='pivot-box' style='background-color:#fff;'>PIVOT<br><b>{round(dp,2)}</b></div>", unsafe_allow_html=True)
    p4.markdown(f"<div class='pivot-box'>R1<br><b>{round(r1,2)}</b></div>", unsafe_allow_html=True)
    p5.markdown(f"<div class='pivot-box'>R2<br><b>{round(r2,2)}</b></div>", unsafe_allow_html=True)
    
    # 5. MOVING AVERAGES
    st.markdown("<b>KEY MOVING AVERAGES (TREND SUPPORT)</b>", unsafe_allow_html=True)
    s_col1, s_col2, s_col3, s_col4, s_col5 = st.columns(5)
    def sma_clr(val): return "green" if ltp > val else "red"
    s_col1.markdown(f"<div class='sma-box'>10 SMA<br><b style='color:{sma_clr(sma10)}'>{round(sma10,2)}</b></div>", unsafe_allow_html=True)
    s_col2.markdown(f"<div class='sma-box'>20 SMA<br><b style='color:{sma_clr(sma20)}'>{round(sma20,2)}</b></div>", unsafe_allow_html=True)
    s_col3.markdown(f"<div class='sma-box'>50 SMA<br><b style='color:{sma_clr(sma50)}'>{round(sma50,2)}</b></div>", unsafe_allow_html=True)
    s_col4.markdown(f"<div class='sma-box'>100 SMA<br><b style='color:{sma_clr(sma100)}'>{round(sma100,2)}</b></div>", unsafe_allow_html=True)
    s_col5.markdown(f"<div class='sma-box'>200 SMA<br><b style='color:{sma_clr(sma200)}'>{round(sma200,2)}</b></div>", unsafe_allow_html=True)

    # 6. GANN LEVELS
    tg = r['Tgts']
    ba=round(dp*1.001,2); sb=round(dp*0.999,2); s_rt_b=math.sqrt(ba); s_rt_s=math.sqrt(sb)
    bt=[round((s_rt_b+(i*0.125))**2,2) for i in range(1,6)]; st_=[round((s_rt_s-(i*0.125))**2,2) for i in range(1,6)]
    
    cb,cs = st.columns(2)
    with cb:
        html_buy = f"<div class='plan-box-buy'><b>BUY ABOVE: {ba}</b> | SL: {round(dp,2)}<hr>T1: {bt[0]} | T2: {bt[1]}<br>T3: {bt[2]} | T4: {bt[3]}<br><b>TGT 5: {bt[4]}</b></div>"
        st.markdown(html_buy, unsafe_allow_html=True)
        if ltp >= bt[4]: st.markdown("<div class='reverse-warn'>REVERSAL ZONE</div>", unsafe_allow_html=True)
    with cs:
        html_sell = f"<div class='plan-box-sell'><b>SELL BELOW: {sb}</b> | SL: {round(dp,2)}<hr>T1: {st_[0]} | T2: {st_[1]}<br>T3: {st_[2]} | T4: {st_[3]}<br><b>TGT 5: {st_[4]}</b></div>"
        st.markdown(html_sell, unsafe_allow_html=True)
        if ltp <= st_[4]: st.markdown("<div class='reverse-warn'>REVERSAL ZONE</div>", unsafe_allow_html=True)
    
    # 7. RSI & ADX
    if adx > 25: adx_c="green"; adx_stat="TRENDING"; adx_rem="Strong Momentum."
    elif adx < 20: adx_c="red"; adx_stat="SIDEWAYS"; adx_rem="No Trade Zone."
    else: adx_c="orange"; adx_stat="WEAK"; adx_rem="Weak Trend."
    
    rsi_val = round(rsi, 2)
    rsi_stat = "OVERBOUGHT (Risk)" if rsi > 70 else ("OVERSOLD (Bounce)" if rsi < 30 else "NEUTRAL")
    rsi_c = "red" if rsi > 70 or rsi < 30 else "blue"

    st.markdown(f"""<div style='margin-top:5px; display:flex; gap:10px;'>
        <div style='flex:1; padding:5px; border-radius:5px; border:1px solid {adx_c}; text-align:center;'>
            <b style='color:{adx_c}!important;'>ADX: {round(adx,2)} ({adx_stat})</b><br><span style='font-size:10px;'>{adx_rem}</span>
        </div>
        <div style='flex:1; padding:5px; border-radius:5px; border:1px solid {rsi_c}; text-align:center;'>
            <b style='color:{rsi_c}!important;'>RSI: {rsi_val}</b><br><span style='font-size:11px;'>{rsi_stat}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class='disclaimer-box'>IT IS NOT A BUY/SELL RECOMMENDATION.<br>STRICTLY FOR STUDY PURPOSE.<br>CONSULT YOUR FINANCIAL ADVISOR.</div>""", unsafe_allow_html=True)
else:
    st.error(f"Could not load data for {st.session_state.selected_stock}. If this persists, please try 'REFRESH DATA' button.")
