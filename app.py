import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import json
import os
from datetime import datetime
import pytz
from tvDatafeed import TvDatafeed, Interval
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. AYARLAR & KİMLİK
# ==========================================

TELEGRAM_TOKEN = "7977796977:AAHNn1m3WbzfRTHOocfYTpQuhN6OWMRdwXg"
TELEGRAM_GROUP_ID = "-1003588305277" 

TV_USER = "hakanozalp1192"
TV_PASS = "192013Eg.//+"

PERIYOT = Interval.in_1_hour 

# LİSTE (Senin 327 Hissen)
FULL_UNIVERSE = ['BMSTL','EMKEL','FORMT','GARAN','HKTM','MAGEN','MNDTR','ODINE','RYGYO','SAFKR','SELGD','SKTAS','SNKRN','TCELL','TGSAS','TRGYO','ULUUN','SAMAT','YESIL','KFEIN','TAVHL','TEZOL','SRVGY','HURGZ','ANELE','KLSYN','ICBCT','CRDFA','KIMMR','MSGYO','AVGYO','SOKM','FZLGY','BRKVY','LOGO','TDGYO','IEYHO','KRONT','PATEK','VERUS','ETYAT','BASGZ','ESEN','IHAAS','RYSAS','VANGD','MACKO','PENTA','INTEM','GEDZA','GLCVY','BIENY','NUGYO','SEGMN','TLMAN','USAK','ONCSM','PRKME','ALBRK','ESCOM','ICUGS','KOPOL','PRDGS','DMRGD','HATEK','DGNMO','SEGYO','EUYO','OBASE','PSGYO','BNTAS','CVKMD','FORTE','SUNTK','ULUFA','BLCYT','DURDO','GEREL','PNLSN','GRSEL','VAKFN','KLMSN','MOGAN','KORDS','ANSGR','SMRTG','TKFEN','IZMDC','AKSA','FROTO','MNDRS','METRO','YEOTK','CEMTS','CRFSA','DARDL','ARASE','BIOEN','PNSUT','ALKIM','DGATE','YKSLN','OSTIM','MAKIM','ISGSY','CEMAS','DERHL','EKGYO','ISGYO','SKBNK','HUBVC','AKSUE','GENTS','EDATA','BIGCH','TOASO','CLEBI','CIMSA','PSDTC','EMNIS','SAHOL','VBTYZ','ALGYO','BORLS','FONET','KONKA','ASGYO','ENKAI','GWIND','KRDMD','BAKAB','OZKGY','FRIGO','POLHO','NTGAZ','TEKTU','ASTOR','VKGYO','KOZAL','KARTN','TMPOL','TKNSA','DAPGM','PINSU','MTRYO','KRDMB','MMCAS','ESCAR','AFYON','BORSK','KZGYO','BEYAZ','LILAK','KRVGD','AGROT','BRLSM','SMART','REEDR','JANTS','VESTL','MIATK','MARKA','CANTE','INGRM','BINHO','BJKAS','BANVT','DIRIT','DOAS','CWENE','VAKKO','NETAS','YONGA','SANKO','EGEPO','ISSEN','PAPIL','PAMEL','KRTEK','IHLGM','FADE','DNISI','EGSER','KNFRT','MEKAG','BRISA','INDES','MERCN','KARYE','IHYAY','MERKO','SARKY','GESAN','NUHCM','BOSSA','ECZYT','ALKA','KERVT','KAPLM','TSPOR','OYAYO','TURGG','ZEDUR','OZGYO','AKENR','IMASM','KATMR','KARSN','KTSKR','SELEC','ARZUM','CELHA','HTTBT','GOLTS','TUKAS','PRZMA','GSDDE','PKART','POLTK','OYLUM','TURSG','CEOEM','EGGUB','ELITE','MEPET','GARFA','SONME','COSMO','KRPLS','GRNYO','EDIP','PGSUS','SDTTR','BEGYO','BVSAN','KLRHO','LUKSK','TMSN','AKGRT','BERA','KLGYO','TRILC','KUTPO','KUYAS','OZSUB','OFSYM','ARTMS','ATLAS','TUCLK','FMIZP','SASA','BMSCH','HATSN','HEKTS','KAYSE','GEDIK','SUWEN','ATEKS','BARMA','SANEL','HLGYO','MAALT','ARCLK','ASUZU','SISE','BRKSN','AEFES','PLTUR','MANAS','BRSAN','AKCNS','YAYLA','AKMGY','BFREN','SNICA','TSGYO','DOHOL','DOKTA','MARTI','EUKYO','GLBMD','ERSU','DCTTR','NATEN','KRGYO','GSRAY','BIMAS','ISFIN','CATES','MZHLD','PENGD','RODRG','CONSE','LMKDC','DERIM','MEDTR','TATGD','ETILR','PRKAB','RNPOL','BAGFS','KRSTL','YYLGD','ERCB','ENJSA','MERIT','BIZIM','OTKAR','ISDMR','ONRYT','NIBAS','PKENT','QUAGR','THYAO','OSMEN','DITAS','MAKTK','DOGUB','RAYSG','ARSAN','DAGI','BURCE','KERVN','HUNER','KONTR','DEVA']
BLACKLIST = ['AHGAZ','TTRAK','AKYHO','MEGAP','TBORG','CMENT','OZRDN','SNPAM','OYAKC','SANFM','ALARK','AKFGY','BALAT','AKSEN']
ACTIVE_WHITELIST = [h for h in FULL_UNIVERSE if h not in BLACKLIST]

# Dosya Adı (Hafıza)
HAFIZA_DOSYASI = "sinyal_hafizasi.json"

# ==========================================
# 2. YARDIMCI FONKSİYONLAR (HAFIZA & ANALİZ)
# ==========================================

def tr_saat():
    tz = pytz.timezone('Europe/Istanbul')
    return datetime.now(tz)

def hafiza_yukle():
    """Geçmiş Alım Sinyallerini Yükler"""
    if os.path.exists(HAFIZA_DOSYASI):
        try:
            with open(HAFIZA_DOSYASI, 'r') as f:
                return json.load(f)
        except: return {}
    return {}

def hafiza_kaydet(data):
    """Yeni Sinyali Kaydeder"""
    try:
        with open(HAFIZA_DOSYASI, 'w') as f:
            json.dump(data, f)
    except: pass

def send_telegram(message):
    simdi = tr_saat()
    # 09:50 - 18:15 arası mesaj izni
    if (simdi.hour > 9 or (simdi.hour==9 and simdi.minute>=50)) and (simdi.hour < 18 or (simdi.hour==18 and simdi.minute<=15)):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {"chat_id": TELEGRAM_GROUP_ID, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data, timeout=5)
        except: pass

class MLEngine:
    def __init__(self):
        self.model = LinearRegression()
    
    def optimal_giris(self, df):
        try:
            df['Volatility'] = df['High'] - df['Low']
            df['Body'] = abs(df['Close'] - df['Open'])
            data = df.tail(50).copy()
            X = data[['Volatility', 'Body']].values[:-1]
            y = data['Low'].values[1:]
            self.model.fit(X, y)
            curr = [[df['Volatility'].iloc[-1], df['Body'].iloc[-1]]]
            pred = self.model.predict(curr)[0]
            return round(min(pred, df['Close'].iloc[-1] * 0.997), 2)
        except: return round(df['Low'].iloc[-1] * 1.003, 2)

    def calculate_atr(self, df, period=14):
        try:
            high_low = df['High'] - df['Low']
            high_close = (df['High'] - df['Close'].shift()).abs()
            low_close = (df['Low'] - df['Close'].shift()).abs()
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            return np.max(ranges, axis=1).rolling(period).mean().iloc[-1]
        except: return df['Close'].iloc[-1] * 0.03

def wavetrend_check(df):
    try:
        hlc3 = (df['High'] + df['Low'] + df['Close']) / 3
        esa = hlc3.ewm(span=10, adjust=False).mean()
        d = (hlc3 - esa).abs().ewm(span=10, adjust=False).mean()
        ci = (hlc3 - esa) / (0.015 * d)
        wt1 = ci.ewm(span=21, adjust=False).mean()
        wt2 = wt1.rolling(window=4).mean()
        
        # AL SİNYALİ: Dipte Kesişim (-40 Altı)
        buy_signal = (wt1_prev < wt2_prev) and (wt1_now > wt2_now) and (wt1_prev < -40)
        
        # SAT SİNYALİ: Tepede Kesişim (+40 Üstü)
        sell_signal = (wt1_prev > wt2_prev) and (wt1_now < wt2_now) and (wt1_prev > 40)
        
        return buy_signal, sell_signal, wt1_now, wt2_now
    except: return False, False, 0, 0

def get_tv():
    try: return TvDatafeed(TV_USER, TV_PASS)
    except: return TvDatafeed()

def market_regime(tv):
    try:
        xu100 = tv.get_hist(symbol='XU100', exchange='BIST', interval=Interval.in_daily, n_bars=200)
        if xu100 is not None:
            sma200 = xu100['close'].mean()
            guncel = xu100['close'].iloc[-1]
            if guncel < sma200: return "DEFANSIF"
            else: return "NORMAL"
    except: pass
    return "NORMAL"

# ==========================================
# 3. ANA DÖNGÜ (STREAMLIT)
# ==========================================

st.set_page_config(page_title="Hedge Fund Panel", page_icon="🦁", layout="wide")
st.title("🦁 Borsa Avcısı - Yönetim Paneli")

tv = get_tv()
ml = MLEngine()
piyasa_modu = market_regime(tv)
st.info(f"📊 Piyasa Modu: **{piyasa_modu}**")

# Hafızayı Yükle
hafiza = hafiza_yukle() # {'GARAN': 1709235000, 'THYAO': 1709240000} şeklinde zaman damgası tutar

status = st.empty()
bar = st.progress(0)
sinyal_sayisi = 0

saat = tr_saat().hour
if 9 <= saat <= 18:
    for i, hisse in enumerate(ACTIVE_WHITELIST):
        try:
            status.text(f"🔍 {hisse}")
            bar.progress((i+1)/len(ACTIVE_WHITELIST))
            
            df = tv.get_hist(symbol=hisse, exchange='BIST', interval=PERIYOT, n_bars=100)
