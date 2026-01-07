import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import json
import os
import random
import yfinance as yf
from datetime import datetime
import pytz
from tvDatafeed import TvDatafeed, Interval
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. MÜHİMMATLAR VE AYARLAR
# ==========================================

# TELEGRAM BİLGİLERİN
TELEGRAM_TOKEN = "7977796977:AAHNn1m3WbzfRTHOocfYTpQuhN6OWMRdwXg"
TELEGRAM_GROUP_ID = "-1003588305277" 

# ÇİFT SESSION ID (ANA VE YEDEK)
SESSION_IDS = [
    "v86ido9xj2o78ync4lz4q3ylpytwofne",  # 1. Anahtar
    "8kmfkpq73eqmpnzfwv3vpbi28hp1zktv"   # 2. Anahtar
]

# 511 HİSSELİK LİSTE (Word Dosyasından Temizlenmiş)
ACTIVE_WHITELIST = [
    'AVOD', 'A1CAP', 'A1YEN', 'ACSEL', 'ADEL', 'ADESE', 'AFYON', 'AHSGY', 'AKENR', 'AKSUE', 
    'ALCAR', 'ALCTL', 'ALKIM', 'ALKA', 'ALKLC', 'AYCES', 'ALVES', 'ASUZU', 'ANGEN', 'ANELE', 
    'ARENA', 'ARFYE', 'ARSAN', 'ARTMS', 'ARZUM', 'AVGYO', 'AVHOL', 'AYEN', 'AZTEK', 'BAGFS', 
    'BAHKM', 'BAKAB', 'BNTAS', 'BANVT', 'BARMA', 'BEGYO', 'BAYRK', 'BEYAZ', 'BIGTK', 'BLCYT', 
    'BRKVY', 'BRLSM', 'BIZIM', 'BLUME', 'BMSTL', 'BMSCH', 'BORSK', 'BOSSA', 'BULGS', 'BURCE', 
    'BVSAN', 'BIGCH', 'CRFSA', 'CEOEM', 'CONSE', 'CGCAM', 'CATES', 'CELHA', 'CEMAS', 'CEMTS', 
    'CMBTN', 'CUSAN', 'DAGI', 'DARDL', 'DGATE', 'DCTTR', 'DMSAS', 'DENGE', 'DZGYO', 'DERIM', 
    'DERHL', 'DESA', 'DESPC', 'DNISI', 'DITAS', 'DMRGD', 'DOCO', 'DOFER', 'DGNMO', 'DOKTA', 
    'DURDO', 'DURKN', 'DUNYH', 'DYOBY', 'ECOGR', 'EDATA', 'EDIP', 'EPLAS', 'EGPRO', 'EGSER', 
    'EGEGY', 'EKOS', 'EKSUN', 'ELITE', 'EMKEL', 'ENSRI', 'ERBOS', 'KIMMR', 'ESCOM', 'ETILR', 
    'EYGYO', 'FADE', 'FMIZP', 'FONET', 'FORMT', 'FORTE', 'FRIGO', 'GARFA', 'GEDIK', 'GEDZA', 
    'GEREL', 'GZNMI', 'GMTAS', 'GOODY', 'GSDDE', 'GSDHO', 'GLRYH', 'GUNDG', 'HATEK', 'HDFGS', 
    'HEDEF', 'HKTM', 'HOROZ', 'HUNER', 'HURGZ', 'ICBCT', 'ICUGS', 'INGRM', 'IHLGM', 'IHGZT', 
    'IHAAS', 'IHYAY', 'IMASM', 'INFO', 'INTEM', 'ISSEN', 'ISGSY', 'ISYAT', 'IZMDC', 'IZFAS', 
    'JANTS', 'KFEIN', 'KAPLM', 'KRDMB', 'KRTEK', 'KARTN', 'KRVGD', 'KLMSN', 'KLSYN', 'KNFRT', 
    'KONKA', 'KGYO', 'KRPLS', 'KRGYO', 'KRSTL', 'KRONT', 'KBORU', 'KZGYO', 'KUTPO', 'KTSKR', 
    'LIDFA', 'LKMNH', 'LRSHO', 'LUKSK', 'LYDYE', 'MACKO', 'MAKIM', 'MAKTK', 'MANAS', 'MARKA', 
    'MARMR', 'MAALT', 'MRSHL', 'MRGYO', 'MARTI', 'MTRKS', 'MEDTR', 'MEKAG', 'MNDRS', 'MERCN', 
    'MERIT', 'MERKO', 'METRO', 'MHRGY', 'MSGYO', 'MOGAN', 'MNDTR', 'EGEPO', 'NTGAZ', 'NETAS', 
    'NIBAS', 'NUGYO', 'OBASE', 'OFSYM', 'ONCSM', 'ONRYT', 'OSMEN', 'OSTIM', 'OTTO', 'OYYAT', 
    'OZGYO', 'OZSUB', 'OZYSR', 'PAMEL', 'PNLSN', 'PAGYO', 'PRDGS', 'PRKME', 'PCILT', 'PEKGY', 
    'PENGD', 'PENTA', 'PKENT', 'PETUN', 'PINSU', 'PNSUT', 'PKART', 'RAYSG', 'RTALB', 'RUBNS', 
    'RUZYE', 'SAFKR', 'SNICA', 'SANFM', 'SANKO', 'SAYAS', 'SEGMN', 'SELVA', 'SERNT', 'SMART', 
    'SOKE', 'SKTAS', 'SMRVA', 'SEGYO', 'SKYMD', 'TARKM', 'TATGD', 'TEKTU', 'TKNSA', 'TMPOL', 
    'TERA', 'TEHOL', 'TGSAS', 'TLMAN', 'TSGYO', 'TUCLK', 'MARBL', 'TRILC', 'TURGG', 'PRKAB', 
    'TBORG', 'UFUK', 'ULUFA', 'ULUSE', 'ULUUN', 'UNLU', 'VKGYO', 'VBTYZ', 'VRGYO', 'VERUS', 
    'VERTU', 'VKING', 'VSNMD', 'YATAS', 'YAYLA', 'YYAPI', 'YESIL', 'YIGIT', 'YKSLN', 'YUNSA', 
    'ZEDUR', 'BINHO', 'ADGYO', 'AGHOL', 'AGESA', 'AGROT', 'AHGAZ', 'AKBNK', 'AKCNS', 'AKFGY', 
    'AKFIS', 'AKFYE', 'AKSGY', 'AKSA', 'AKSEN', 'AKGRT', 'ALGYO', 'ALARK', 'ALBRK', 'ALFAS', 
    'ALTNY', 'ANSGR', 'AEFES', 'ANHYT', 'ARCLK', 'ARDYZ', 'ARMGD', 'ASGYO', 'ASELS', 'ASTOR', 
    'ATAKP', 'ATATP', 'AVPGY', 'AYDEM', 'AYGAZ', 'BALSU', 'BASGZ', 'BTCIM', 'BSOKE', 'BERA', 
    'BESLR', 'BJKAS', 'BIENY', 'BIMAS', 'BINBN', 'BIOEN', 'BIGEN', 'BOBET', 'BORLS', 'BRSAN', 
    'BRYAT', 'BFREN', 'BRISA', 'BUCIM', 'CEMZY', 'CCOLA', 'CVKMD', 'CWENE', 'CANTE', 'CLEBI', 
    'CIMSA', 'DAPGM', 'DSTKF', 'DEVA', 'DOFRB', 'DOHOL', 'ARASE', 'DOAS', 'EBEBK', 'ECZYT', 
    'EFOR', 'EGEEN', 'EGGUB', 'ECILC', 'EKGYO', 'ENDAE', 'ENJSA', 'ENERY', 'ENKAI', 'ERCB', 
    'EREGL', 'ESCAR', 'ESEN', 'TEZOL', 'EUREN', 'EUPWR', 'FENER', 'FROTO', 'FZLGY', 'GSRAY', 
    'GWIND', 'GLCVY', 'GENIL', 'GENTS', 'GIPTA', 'GESAN', 'GLYHO', 'GOKNR', 'GOLTS', 'GOZDE', 
    'GRTHO', 'GUBRF', 'GLRMK', 'GRSEL', 'SAHOL', 'HLGYO', 'HRKET', 'HATSN', 'HEKTS', 'HTTBT', 
    'ENTRA', 'INVEO', 'INVES', 'IEYHO', 'ISKPL', 'IHLAS', 'INDES', 'ISDMR', 'ISFIN', 'ISGYO', 
    'ISMEN', 'IZENR', 'KLKIM', 'KLSER', 'KLYPV', 'KRDMA', 'KRDMD', 'KAREL', 'KARSN', 'KTLEV', 
    'KATMR', 'KAYSE', 'TCKRC', 'KZBGY', 'KLGYO', 'KLRHO', 'KMPUR', 'KCAER', 'KCHOL', 'KOCMT', 
    'KONTR', 'KONYA', 'KORDS', 'KOTON', 'KOPOL', 'KUYAS', 'LIDER', 'LILAK', 'LMKDC', 'LINK', 
    'LOGO', 'LYDHO', 'MAGEN', 'MAVI', 'MEGMT', 'MIATK', 'MGROS', 'MPARK', 'MOBTL', 'MOPAS', 
    'NATEN', 'NTHOL', 'NUHCM', 'OBAMS', 'ODAS', 'ODINE', 'ORGE', 'OTKAR', 'OYAKC', 'OZKGY', 
    'OZATD', 'PAPIL', 'PARSN', 'PASEU', 'PSGYO', 'PAHOL', 'PATEK', 'PGSUS', 'PETKM', 'PLTUR', 
    'POLHO', 'POLTK', 'QUAGR', 'RALYH', 'REEDR', 'RYGYO', 'RYSAS', 'RGYAS', 'SARKY', 'SASA', 
    'SDTTR', 'SELEC', 'SRVGY', 'SNGYO', 'SMRTG', 'SUNTK', 'SURGY', 'SUWEN', 'SKBNK', 'SOKM', 
    'TABGD', 'TNZTP', 'TATEN', 'TAVHL', 'TKFEN', 'TOASO', 'TRGYO', 'TSPOR', 'TRMET', 'TRENJ', 
    'TUKAS', 'TRCAS', 'TUREX', 'TCELL', 'TMSN', 'TUPRS', 'TRALT', 'THYAO', 'GARAN', 'HALKB', 
    'ISCTR', 'TSKB', 'TURSG', 'SISE', 'VAKBN', 'TTKOM', 'TTRAK', 'USAK', 'ULKER', 'VAKFA', 
    'VAKFN', 'VAKKO', 'VESBE', 'VESTL', 'YKBNK', 'YAPRK', 'YYLGD', 'YGGYO', 'YEOTK', 'ZERGY', 
    'ZRGYO', 'ZOREN'
]

# Hafıza Dosyası
HAFIZA_DOSYASI = "sinyal_hafizasi.json"

# ==========================================
# 2. BAĞLANTI & VERİ MOTORU (YENİ SİSTEM)
# ==========================================

def init_tv_failover():
    """ÇİFT MOTOR + YFINANCE DESTEKLİ BAĞLANTI"""
    # 1. VIP Anahtarları Dene
    for index, sess_id in enumerate(SESSION_IDS):
        try:
            temp_tv = TvDatafeed()
            session_obj = None
            for attr in dir(temp_tv):
                try:
                    val = getattr(temp_tv, attr)
                    if isinstance(val, requests.Session):
                        session_obj = val
                        break
                except: continue
            
            if session_obj:
                session_obj.cookies.update({'sessionid': sess_id})
                session_obj.headers.update({'User-Agent': 'Mozilla/5.0'})
            else:
                temp_tv.session = requests.Session()
                temp_tv.session.cookies.update({'sessionid': sess_id})

            test = temp_tv.get_hist('THYAO', 'BIST', Interval.in_daily, n_bars=2)
            if test is not None and not test.empty:
                return temp_tv, "TV"
        except: continue
    
    # 2. Misafir Modu Dene
    try:
        temp_tv = TvDatafeed()
        test = temp_tv.get_hist('THYAO', 'BIST', Interval.in_daily, n_bars=2)
        if test is not None and not test.empty:
            return temp_tv, "TV"
    except: pass

    # 3. YFinance (C Planı)
    try:
        test = yf.download("THYAO.IS", period="2d", progress=False)
        if not test.empty:
            return None, "YF"
    except: pass

    return None, "FAIL"

def get_data(symbol, tv_object, source_type):
    """VERİ ÇEKME MOTORU (TV ve YF UYUMLU)"""
    try:
        if source_type == "TV":
            return tv_object.get_hist(symbol=symbol, exchange='BIST', interval=Interval.in_1_hour, n_bars=100)
        elif source_type == "YF":
            yf_sym = symbol + ".IS"
            df = yf.download(yf_sym, period="1mo", interval="1h", progress=False)
            if not df.empty:
                df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                    df.columns = [c.lower() for c in df.columns]
                return df
    except: pass
    return None

# ==========================================
# 3. ANALİZ MOTORU & HAFIZA
# ==========================================

def tr_saat():
    tz = pytz.timezone('Europe/Istanbul')
    return datetime.now(tz)

def hafiza_yukle():
    if os.path.exists(HAFIZA_DOSYASI):
        try:
            with open(HAFIZA_DOSYASI, 'r') as f: return json.load(f)
        except: return {}
    return {}

def hafiza_kaydet(data):
    try:
        with open(HAFIZA_DOSYASI, 'w') as f: json.dump(data, f)
    except: pass

def send_telegram(message):
    simdi = tr_saat()
    # 09:00 - 18:30 arası mesaj izni
    if (simdi.hour >= 9) and (simdi.hour <= 18):
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
            df.columns = [c.capitalize() for c in df.columns] 
            df['Volatility'] = df['High'] - df['Low']
            df['Body'] = abs(df['Close'] - df['Open'])
            data = df.tail(50).copy()
            X = data[['Volatility', 'Body']].values[:-1]
            y = data['Low'].values[1:]
            self.model.fit(X, y)
            curr = [[df['Volatility'].iloc[-1], df['Body'].iloc[-1]]]
            pred = self.model.predict(curr)[0]
            return round(min(pred, df['Close'].iloc[-1] * 0.997), 2)
        except: return round(df['Close'].iloc[-1], 2)

    def calculate_atr(self, df, period=14):
        try:
            df.columns = [c.capitalize() for c in df.columns]
            high_low = df['High'] - df['Low']
            high_close = (df['High'] - df['Close'].shift()).abs()
            low_close = (df['Low'] - df['Close'].shift()).abs()
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            return np.max(ranges, axis=1).rolling(period).mean().iloc[-1]
        except: return df['Close'].iloc[-1] * 0.03

def wavetrend_check(df):
    try:
        df.columns = [c.capitalize() for c in df.columns]
        hlc3 = (df['High'] + df['Low'] + df['Close']) / 3
        esa = hlc3.ewm(span=10, adjust=False).mean()
        d = (hlc3 - esa).abs().ewm(span=10, adjust=False).mean()
        ci = (hlc3 - esa) / (0.015 * d)
        wt1 = ci.ewm(span=21, adjust=False).mean()
        wt2 = wt1.rolling(window=4).mean()
        
        wt1_now = wt1.iloc[-1]
        wt2_now = wt2.iloc[-1]
        wt1_prev = wt1.iloc[-2]
        wt2_prev = wt2.iloc[-2]
        
        buy = (wt1_prev < wt2_prev) and (wt1_now > wt2_now) and (wt1_prev < -40)
        sell = (wt1_prev > wt2_prev) and (wt1_now < wt2_now) and (wt1_prev > 40)
        
        return buy, sell, wt1_now, wt2_now
    except: return False, False, 0, 0

# ==========================================
# 4. ANA DÖNGÜ (SAVAŞ KOMUTA MERKEZİ)
# ==========================================

st.set_page_config(page_title="Hedge Fund Panel V2", page_icon="🦁", layout="wide")
st.title("🦁 SNIPER AI - HYBRID SİSTEM")

# BAĞLANTIYI KUR
tv_obj, source_mode = init_tv_failover()

if source_mode == "FAIL":
    st.error("🚨 SİSTEM ÇÖKTÜ! HİÇBİR KAYNAKTAN VERİ ALINAMIYOR.")
else:
    st.success(f"✅ BAĞLANTI AKTİF | MOD: {source_mode}")
    
    ml = MLEngine()
    hafiza = hafiza_yukle()
    
    status = st.empty()
    bar = st.progress(0)
    sinyal_sayisi = 0
    
    simdi = tr_saat()
    
    # GECE MODU KONTROLÜ (09:00 - 18:30 arası çalış)
    if 9 <= simdi.hour <= 18:
        for i, hisse in enumerate(ACTIVE_WHITELIST):
            try:
                status.text(f"🔍 Taranıyor: {hisse} (Kaynak: {source_mode})")
                bar.progress((i+1)/len(ACTIVE_WHITELIST))
                
                # Anti-Ban (Sadece TV modunda bekle)
                if source_mode == "TV":
                    time.sleep(random.uniform(0.5, 1.2))
                
                # VERİYİ ÇEK
                df = get_data(hisse, tv_obj, source_mode)
                if df is None or df.empty: continue
                
                # ANALİZ
                buy, sell, wt1, wt2 = wavetrend_check(df)
                fiyat = df['close'].iloc[-1] if 'close' in df.columns else df['Close'].iloc[-1]
                su_an = time.time()
                
                # AL SİNYALİ
                if buy:
                    puan = 50 + (wt1 - wt2)*5
                    vol_col = 'Volume' if 'Volume' in df.columns else 'volume'
                    if df[vol_col].iloc[-1] > df[vol_col].iloc[-20:-1].mean(): puan += 15
                    if wt1 < -60: puan += 10
                    puan = min(100, int(puan))
                    
                    if puan >= 60:
                        giris = ml.optimal_giris(df)
                        atr = ml.calculate_atr(df)
                        stop_loss = giris - (atr * 1.5)
                        
                        msg = f"🟢 <b>YENİ FIRSAT! (#{hisse})</b>\n\n"
                        msg += f"🦁 <b>Hisse:</b> #{hisse}\n"
                        msg += f"⭐ <b>Kalite:</b> {puan}/100\n"
                        msg += f"💰 <b>Fiyat:</b> {fiyat} TL\n"
                        msg += f"🧠 <b>AI Giriş:</b> {giris} TL\n"
                        msg += f"🛑 <b>Stop:</b> {round(stop_loss, 2)} TL\n\n"
                        
                        send_telegram(msg)
                        sinyal_sayisi += 1
                        
                        hafiza[hisse] = su_an
                        hafiza_kaydet(hafiza)
                
                # SAT SİNYALİ
                elif sell:
                    if hisse in hafiza:
                        alim_zamani = hafiza[hisse]
                        if (su_an - alim_zamani) <= 86400: # 24 saat kuralı
                            msg = f"🔴 <b>ERKEN UYARI! (#{hisse})</b>\n\n"
                            msg += f"🦁 <b>Hisse:</b> #{hisse}\n"
                            msg += f"📉 <b>Durum:</b> Trend 24 saat dolmadan bozuldu!\n"
                            msg += f"💡 <b>Tavsiye:</b> Stop Ol / Satış Yap.\n\n"
                            send_telegram(msg)
                            sinyal_sayisi += 1
                        del hafiza[hisse]
                        hafiza_kaydet(hafiza)
                        
            except: continue
        
        status.success(f"Tur Bitti. {sinyal_sayisi} işlem bulundu. Yeniden başlatılıyor...")
        
    else:
        st.warning("🌙 Gece Modu. Piyasalar kapalı. Sistem uyku modunda.")

    # --- SONSUZ DÖNGÜ (AUTO-RESTART) ---
    time.sleep(60) # 1 Dakika bekle
    st.rerun()     # BAŞA SAR VE TEKRARLA!
