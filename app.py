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
# 1. AYARLAR
# ==========================================

TELEGRAM_TOKEN = "7977796977:AAHNn1m3WbzfRTHOocfYTpQuhN6OWMRdwXg"
TELEGRAM_GROUP_ID = "-1003588305277" 

SESSION_IDS = [
    "v86ido9xj2o78ync4lz4q3ylpytwofne",
    "8kmfkpq73eqmpnzfwv3vpbi28hp1zktv"
]

# 511 HİSSELİK LİSTE
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

HAFIZA_DOSYASI = "sinyal_hafizasi.json"

# ==========================================
# 2. MOTORLAR (MULTI-TIMEFRAME ENGINE)
# ==========================================

def init_tv_failover():
    for index, sess_id in enumerate(SESSION_IDS):
        try:
            temp_tv = TvDatafeed()
            s_obj = None
            for attr in dir(temp_tv):
                try:
                    if isinstance(getattr(temp_tv, attr), requests.Session):
                        s_obj = getattr(temp_tv, attr)
                        break
                except: continue
            
            if s_obj:
                s_obj.cookies.update({'sessionid': sess_id})
                s_obj.headers.update({'User-Agent': 'Mozilla/5.0'})
            else:
                temp_tv.session = requests.Session()
                temp_tv.session.cookies.update({'sessionid': sess_id})

            if not temp_tv.get_hist('THYAO', 'BIST', Interval.in_daily, n_bars=1).empty:
                return temp_tv, "TV"
        except: continue
    
    try:
        if not TvDatafeed().get_hist('THYAO', 'BIST', Interval.in_daily, n_bars=1).empty:
            return TvDatafeed(), "TV"
    except: pass
    
    try:
        if not yf.download("THYAO.IS", period="1d", progress=False).empty:
            return None, "YF"
    except: pass
    return None, "FAIL"

def get_data(symbol, tv_object, source_type, timeframe):
    try:
        if source_type == "TV":
            interval = Interval.in_daily if timeframe == 'DAILY' else Interval.in_1_hour
            return tv_object.get_hist(symbol=symbol, exchange='BIST', interval=interval, n_bars=100)
        elif source_type == "YF":
            yf_sym = symbol + ".IS"
            p = "6mo" if timeframe == 'DAILY' else "1mo"
            i = "1d" if timeframe == 'DAILY' else "1h"
            df = yf.download(yf_sym, period=p, interval=i, progress=False)
            if not df.empty:
                df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                    df.columns = [c.lower() for c in df.columns]
                return df
    except: pass
    return None

# ==========================================
# 3. ZEKA (ML & ANALİZ)
# ==========================================

class MLEngine:
    def __init__(self):
        self.model = LinearRegression()
    
    def bist_yuvarlama(self, fiyat):
        """
        BIST Fiyat Adımları Kuralı (Tick Size)
        """
        if fiyat < 20.00:
            tick = 0.01
        elif fiyat < 50.00:
            tick = 0.02
        elif fiyat < 100.00:
            tick = 0.05
        elif fiyat < 250.00:
            tick = 0.10
        elif fiyat < 500.00:
            tick = 0.25
        elif fiyat < 1000.00:
            tick = 0.50
        else:
            tick = 1.00
            
        # En yakın tick'e yuvarla
        return round(round(fiyat / tick) * tick, 2)

    def optimal_giris(self, df):
        """Saatlik veriyi kullanarak hassas ve BIST uyumlu giriş hesaplar"""
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
            
            # Ham AI Tahmini
            raw_price = min(pred, df['Close'].iloc[-1] * 0.998)
            
            # BIST Kuralına Göre Düzelt (Burası Yeni!)
            return self.bist_yuvarlama(raw_price)
            
        except: return round(df['Close'].iloc[-1], 2)

    def calculate_atr(self, df, period=14):
        try:
            df.columns = [c.capitalize() for c in df.columns]
            high_low = df['High'] - df['Low']
            high_close = (df['High'] - df['Close'].shift()).abs()
            low_close = (df['Low'] - df['Close'].shift()).abs()
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            raw_stop = np.max(ranges, axis=1).rolling(period).mean().iloc[-1]
            return raw_stop
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

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_GROUP_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=5)
    except: pass

def tr_saat():
    return datetime.now(pytz.timezone('Europe/Istanbul'))

def hafiza_islem(mode, data=None):
    if mode == "load":
        if os.path.exists(HAFIZA_DOSYASI):
            try: 
                with open(HAFIZA_DOSYASI, 'r') as f: return json.load(f)
            except: return {}
        return {}
    elif mode == "save":
        try: 
            with open(HAFIZA_DOSYASI, 'w') as f: json.dump(data, f)
        except: pass

# ==========================================
# 4. ANA DÖNGÜ (STRATEJİ MERKEZİ)
# ==========================================

st.set_page_config(page_title="Sniper V5 - BIST PRO", page_icon="🦁", layout="wide")
st.title("🦁 SNIPER AI - BIST UYUMLU PROFESYONEL SİSTEM")

tv_obj, source_mode = init_tv_failover()
ml = MLEngine()
hafiza = hafiza_islem("load")

if source_mode == "FAIL":
    st.error("🚨 SİSTEM ÇÖKTÜ!")
else:
    st.success(f"✅ SİSTEM AKTİF | MOD: {source_mode} | STRATEJİ: Günlük Trend + BIST Uyumlu Giriş")
    
    status = st.empty()
    bar = st.progress(0)
    simdi = tr_saat()
    sinyal_sayisi = 0

    if 9 <= simdi.hour <= 18:
        for i, hisse in enumerate(ACTIVE_WHITELIST):
            try:
                status.text(f"🔍 {hisse} Analiz Ediliyor...")
                bar.progress((i+1)/len(ACTIVE_WHITELIST))
                if source_mode == "TV": time.sleep(random.uniform(0.5, 1.2))
                
                # ADIM 1: GÜNLÜK VERİ (Trend)
                df_daily = get_data(hisse, tv_obj, source_mode, "DAILY")
                if df_daily is None or df_daily.empty: continue
                
                buy_daily, sell_daily, wt1, wt2 = wavetrend_check(df_daily)
                fiyat = df_daily['close'].iloc[-1] if 'close' in df_daily.columns else df_daily['Close'].iloc[-1]
                su_an = time.time()

                # --- SENARYO 1: AL ---
                if buy_daily:
                    df_hourly = get_data(hisse, tv_obj, source_mode, "HOURLY")
                    
                    puan = 50 + (wt1 - wt2)*5
                    if wt1 < -60: puan += 10
                    puan = min(100, int(puan))
                    
                    if puan >= 60:
                        if df_hourly is not None and not df_hourly.empty:
                            giris = ml.optimal_giris(df_hourly) # BIST Uyumlu Hesaplanacak
                        else:
                            giris = ml.bist_yuvarlama(fiyat)
                        
                        atr = ml.calculate_atr(df_daily)
                        raw_stop = giris - (atr * 1.5)
                        stop_loss = ml.bist_yuvarlama(raw_stop) # Stop da kurallara uymalı

                        msg = f"🟢 <b>DEV TREND BAŞLIYOR! (#{hisse})</b>\n\n"
                        msg += f"🦁 <b>Hisse:</b> #{hisse}\n"
                        msg += f"⭐ <b>Kalite:</b> {puan}/100\n"
                        msg += f"💰 <b>Anlık Fiyat:</b> {fiyat} TL\n"
                        msg += f"🎯 <b>BIST Uyumlu Giriş:</b> {giris} TL\n"
                        msg += f"🛡️ <b>Stop Loss:</b> {stop_loss} TL\n\n"
                        
                        send_telegram(msg)
                        sinyal_sayisi += 1
                        hafiza[hisse] = su_an
                        hafiza_islem("save", hafiza)

                # --- SENARYO 2: SAT ---
                elif sell_daily:
                    if hisse in hafiza:
                        if (su_an - hafiza[hisse]) <= 172800:
                            msg = f"🔴 <b>DİKKAT! TREND BOZULDU (#{hisse})</b>\nStop Ol / Kar Al."
                            send_telegram(msg)
                        del hafiza[hisse]
                        hafiza_islem("save", hafiza)

            except: continue
        
        status.success(f"Tur Tamamlandı. {sinyal_sayisi} fırsat bulundu. Yeniden başlıyor...")
    else:
        st.warning("🌙 Piyasa Kapalı.")

    time.sleep(60)
    st.rerun()
