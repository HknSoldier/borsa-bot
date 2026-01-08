import pandas as pd
import numpy as np
import time
import requests
import json
import os
import yfinance as yf
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval

# ==========================================
# 1. AYARLAR VE GİZLİ ANAHTARLAR
# ==========================================

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_GROUP_ID = os.environ.get("TELEGRAM_GROUP_ID")
SESSION_ID = os.environ.get("SESSION_ID")

ACTIVE_WHITELIST = [
    'AVOD', 'A1CAP', 'ACSEL', 'ADEL', 'ADESE', 'AFYON', 'AKENR', 'AKSUE', 'ALCAR', 'ALKIM', 
    'ALKA', 'ASUZU', 'ANGEN', 'ANELE', 'ARFYE', 'ARSAN', 'ARTMS', 'ARZUM', 'AVGYO', 'AVHOL', 
    'AYEN', 'AZTEK', 'BAGFS', 'BANVT', 'BARMA', 'BEGYO', 'BAYRK', 'BEYAZ', 'BLCYT', 'BRLSM', 
    'BIZIM', 'BOSSA', 'BURCE', 'BVSAN', 'BIGCH', 'CRFSA', 'CEOEM', 'CONSE', 'CGCAM', 'CATES', 
    'CEMTS', 'CMBTN', 'CUSAN', 'DAGI', 'DARDL', 'DGATE', 'DCTTR', 'DMSAS', 'DERIM', 'DESA', 
    'DESPC', 'DNISI', 'DITAS', 'DMRGD', 'DOCO', 'DOFER', 'DGNMO', 'DOKTA', 'DURDO', 'DYOBY', 
    'EDATA', 'EDIP', 'EPLAS', 'EGPRO', 'EGSER', 'EKOS', 'EKSUN', 'ELITE', 'EMKEL', 'ENSRI', 
    'ERBOS', 'KIMMR', 'ESCOM', 'ETILR', 'EYGYO', 'FADE', 'FMIZP', 'FONET', 'FORMT', 'FORTE', 
    'FRIGO', 'GARFA', 'GEDIK', 'GEDZA', 'GEREL', 'GZNMI', 'GMTAS', 'GOODY', 'GSDDE', 'GSDHO', 
    'GLRYH', 'GUNDG', 'HATEK', 'HDFGS', 'HEDEF', 'HKTM', 'HOROZ', 'HUNER', 'HURGZ', 'ICBCT', 
    'INGRM', 'IHLGM', 'IHGZT', 'IHAAS', 'IHYAY', 'IMASM', 'INFO', 'INTEM', 'ISSEN', 'ISGSY', 
    'ISYAT', 'IZMDC', 'IZFAS', 'JANTS', 'KFEIN', 'KAPLM', 'KRDMB', 'KRTEK', 'KARTN', 'KRVGD', 
    'KLMSN', 'KLSYN', 'KNFRT', 'KONKA', 'KGYO', 'KRPLS', 'KRGYO', 'KRSTL', 'KRONT', 'KBORU', 
    'KZGYO', 'KUTPO', 'KTSKR', 'LIDFA', 'LKMNH', 'LRSHO', 'LUKSK', 'LYDYE', 'MACKO', 'MAKIM', 
    'MAKTK', 'MANAS', 'MARKA', 'MAALT', 'MRSHL', 'MRGYO', 'MARTI', 'MTRKS', 'MEDTR', 'MEKAG', 
    'MNDRS', 'MERCN', 'MERIT', 'MERKO', 'METRO', 'MHRGY', 'MSGYO', 'MOGAN', 'MNDTR', 'EGEPO', 
    'NTGAZ', 'NETAS', 'NIBAS', 'NUGYO', 'OBASE', 'OFSYM', 'ONCSM', 'ONRYT', 'OSMEN', 'OSTIM', 
    'OTTO', 'OYYAT', 'OZGYO', 'OZSUB', 'OZYSR', 'PAMEL', 'PNLSN', 'PAGYO', 'PRDGS', 'PRKME', 
    'PCILT', 'PEKGY', 'PENGD', 'PENTA', 'PKENT', 'PETUN', 'PINSU', 'PNSUT', 'PKART', 'RAYSG', 
    'RTALB', 'RUBNS', 'RUZYE', 'SAFKR', 'SNICA', 'SANFM', 'SANKO', 'SAYAS', 'SEGMN', 'SELVA', 
    'SERNT', 'SMART', 'SOKE', 'SKTAS', 'SMRVA', 'SEGYO', 'SKYMD', 'TARKM', 'TATGD', 'TEKTU', 
    'TKNSA', 'TMPOL', 'TERA', 'TEHOL', 'TGSAS', 'TLMAN', 'TSGYO', 'TUCLK', 'MARBL', 'TRILC', 
    'TURGG', 'PRKAB', 'TBORG', 'UFUK', 'ULUFA', 'ULUSE', 'ULUUN', 'UNLU', 'VKGYO', 'VBTYZ', 
    'VRGYO', 'VERUS', 'VERTU', 'VKING', 'VSNMD', 'YATAS', 'YAYLA', 'YYAPI', 'YESIL', 'YIGIT', 
    'YKSLN', 'YUNSA', 'ZEDUR', 'BINHO', 'ADGYO', 'AGHOL', 'AGESA', 'AGROT', 'AHGAZ', 'AKBNK', 
    'AKCNS', 'AKFGY', 'AKFIS', 'AKFYE', 'AKSGY', 'AKSA', 'AKSEN', 'AKGRT', 'ALGYO', 'ALARK', 
    'ALBRK', 'ALFAS', 'ALTNY', 'ANSGR', 'AEFES', 'ANHYT', 'ARCLK', 'ARDYZ', 'ARMGD', 'ASGYO', 
    'ASELS', 'ASTOR', 'ATAKP', 'ATATP', 'AVPGY', 'AYDEM', 'AYGAZ', 'BALSU', 'BASGZ', 'BTCIM', 
    'BSOKE', 'BERA', 'BESLR', 'BJKAS', 'BIENY', 'BIMAS', 'BINBN', 'BIOEN', 'BIGEN', 'BOBET', 
    'BORLS', 'BRSAN', 'BRYAT', 'BFREN', 'BRISA', 'BUCIM', 'CEMZY', 'CCOLA', 'CVKMD', 'CWENE', 
    'CANTE', 'CLEBI', 'CIMSA', 'DAPGM', 'DSTKF', 'DEVA', 'DOFRB', 'DOHOL', 'ARASE', 'DOAS', 
    'EBEBK', 'ECZYT', 'EFOR', 'EGEEN', 'EGGUB', 'ECILC', 'EKGYO', 'ENDAE', 'ENJSA', 'ENERY', 
    'ENKAI', 'ERCB', 'EREGL', 'ESCAR', 'ESEN', 'TEZOL', 'EUREN', 'EUPWR', 'FENER', 'FROTO', 
    'FZLGY', 'GSRAY', 'GWIND', 'GLCVY', 'GENIL', 'GENTS', 'GIPTA', 'GESAN', 'GLYHO', 'GOKNR', 
    'GOLTS', 'GOZDE', 'GRTHO', 'GUBRF', 'GLRMK', 'GRSEL', 'SAHOL', 'HLGYO', 'HRKET', 'HATSN', 
    'HEKTS', 'HTTBT', 'ENTRA', 'INVEO', 'INVES', 'IEYHO', 'ISKPL', 'IHLAS', 'INDES', 'ISDMR', 
    'ISFIN', 'ISGYO', 'ISMEN', 'IZENR', 'KLKIM', 'KLSER', 'KLYPV', 'KRDMA', 'KRDMD', 'KAREL', 
    'KARSN', 'KTLEV', 'KATMR', 'KAYSE', 'TCKRC', 'KZBGY', 'KLGYO', 'KLRHO', 'KMPUR', 'KCAER', 
    'KCHOL', 'KOCMT', 'KONTR', 'KONYA', 'KORDS', 'KOTON', 'KOPOL', 'KUYAS', 'LIDER', 'LILAK', 
    'LMKDC', 'LINK', 'LOGO', 'LYDHO', 'MAGEN', 'MAVI', 'MEGMT', 'MIATK', 'MGROS', 'MPARK', 
    'MOBTL', 'MOPAS', 'NATEN', 'NTHOL', 'NUHCM', 'OBAMS', 'ODAS', 'ODINE', 'ORGE', 'OTKAR', 
    'OYAKC', 'OZKGY', 'OZATD', 'PAPIL', 'PARSN', 'PASEU', 'PSGYO', 'PAHOL', 'PATEK', 'PGSUS', 
    'PETKM', 'PLTUR', 'POLHO', 'POLTK', 'QUAGR', 'RALYH', 'REEDR', 'RYGYO', 'RYSAS', 'RGYAS', 
    'SARKY', 'SASA', 'SDTTR', 'SELEC', 'SRVGY', 'SNGYO', 'SMRTG', 'SUNTK', 'SURGY', 'SUWEN', 
    'SKBNK', 'SOKM', 'TABGD', 'TNZTP', 'TATEN', 'TAVHL', 'TKFEN', 'TOASO', 'TRGYO', 'TSPOR', 
    'TRMET', 'TRENJ', 'TUKAS', 'TRCAS', 'TUREX', 'TCELL', 'TMSN', 'TUPRS', 'TRALT', 'THYAO', 
    'GARAN', 'HALKB', 'ISCTR', 'TSKB', 'TURSG', 'SISE', 'VAKBN', 'TTKOM', 'TTRAK', 'USAK', 
    'ULKER', 'VAKFA', 'VAKFN', 'VAKKO', 'VESBE', 'VESTL', 'YKBNK', 'YAPRK', 'YYLGD', 'YGGYO', 
    'YEOTK', 'ZERGY', 'ZRGYO', 'ZOREN'
]

HAFIZA_DOSYASI = "sinyal_hafizasi.json"

# ==========================================
# 2. MOTORLAR (V10 MANTIĞI)
# ==========================================

def init_tv():
    # Session ID ile TradingView'a bağlan (Misafir Modu Engelleyici)
    try:
        temp_tv = TvDatafeed()
        if SESSION_ID:
            s_obj = None
            for attr in dir(temp_tv):
                try:
                    if isinstance(getattr(temp_tv, attr), requests.Session):
                        s_obj = getattr(temp_tv, attr)
                        break
                except: continue
            
            if s_obj:
                s_obj.cookies.update({'sessionid': SESSION_ID})
                s_obj.headers.update({'User-Agent': 'Mozilla/5.0'})
                print("✅ TV: Session ID Enjekte Edildi.")
            else:
                print("⚠️ TV: Session objesi bulunamadı, misafir modu.")
        return temp_tv
    except:
        return None

def get_data(symbol, tv_object, interval_str):
    try:
        if interval_str == 'DAILY':
            return tv_object.get_hist(symbol=symbol, exchange='BIST', interval=Interval.in_daily, n_bars=100)
        elif interval_str == 'HOURLY':
            return tv_object.get_hist(symbol=symbol, exchange='BIST', interval=Interval.in_1_hour, n_bars=100)
    except: return None

def bist_yuvarlama(fiyat):
    if fiyat < 20.00: tick = 0.01
    elif fiyat < 50.00: tick = 0.02
    elif fiyat < 100.00: tick = 0.05
    elif fiyat < 250.00: tick = 0.10
    else: tick = 0.25
    return round(round(fiyat / tick) * tick, 2)

def calculate_metrics(df_daily, df_hourly, current_price):
    try:
        # GİRİŞ: Hourly VWAP - StdDev (V10 Özel Giriş Taktiği)
        df_hourly.columns = [c.capitalize() for c in df_hourly.columns]
        std_dev = df_hourly['Close'].rolling(window=20).std().iloc[-1]
        vwap = (df_hourly['High'].iloc[-1] + df_hourly['Low'].iloc[-1] + df_hourly['Close'].iloc[-1]) / 3
        giris = bist_yuvarlama(vwap - (std_dev * 0.5))
        if giris >= current_price: giris = current_price * 0.997

        # STOP/HEDEF: Daily ATR
        df_daily.columns = [c.capitalize() for c in df_daily.columns]
        high_low = df_daily['High'] - df_daily['Low']
        high_close = (df_daily['High'] - df_daily['Close'].shift()).abs()
        low_close = (df_daily['Low'] - df_daily['Close'].shift()).abs()
        atr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1).rolling(14).mean().iloc[-1]

        stop = bist_yuvarlama(giris - (atr * 1.5))
        tp1 = bist_yuvarlama(giris + (atr * 3.0))
        tp2 = bist_yuvarlama(giris + (atr * 5.0))

        return giris, stop, tp1, tp2
    except: return 0, 0, 0, 0

def wavetrend_check(df):
    try:
        df.columns = [c.capitalize() for c in df.columns]
        hlc3 = (df['High'] + df['Low'] + df['Close']) / 3
        esa = hlc3.ewm(span=10, adjust=False).mean()
        d = (hlc3 - esa).abs().ewm(span=10, adjust=False).mean()
        ci = (hlc3 - esa) / (0.015 * d)
        wt1 = ci.ewm(span=21, adjust=False).mean()
        wt2 = wt1.rolling(window=4).mean()
        
        # NET KESİŞİM KURALI (V10 ile aynı)
        buy = (wt1.iloc[-2] < wt2.iloc[-2]) and (wt1.iloc[-1] > wt2.iloc[-1]) and (wt1.iloc[-1] < -40)
        sell = (wt1.iloc[-2] > wt2.iloc[-2]) and (wt1.iloc[-1] < wt2.iloc[-1])
        return buy, sell, wt1.iloc[-1], wt2.iloc[-1]
    except: return False, False, 0, 0

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_GROUP_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=5)
    except: pass

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

# ==========================================
# 3. GHOST MODE (TEK SEFERLİK ÇALIŞMA)
# ==========================================

if __name__ == "__main__":
    print("🦁 SNIPER AI - GHOST MODE BAŞLATILIYOR...")
    
    tv = init_tv()
    hafiza = hafiza_yukle()
    simdi = time.time()
    
    if tv is None:
        print("❌ HATA: Veri kaynağına bağlanılamadı.")
        exit()

    for hisse in ACTIVE_WHITELIST:
        try:
            # GÜNLÜK VERİ ÇEK (Sinyal İçin)
            df_daily = get_data(hisse, tv, 'DAILY')
            if df_daily is None or df_daily.empty: continue

            # ANALİZ YAP
            buy, sell, wt1, wt2 = wavetrend_check(df_daily)
            fiyat = df_daily['close'].iloc[-1]

            # --- AL SİNYALİ ---
            if buy:
                if hisse in hafiza: continue # Zaten portföyde var
                
                # Kalite Puanı Hesabı
                puan = 50 + (wt1 - wt2)*5
                if wt1 < -60: puan += 10
                puan = min(100, int(puan))

                if puan >= 60:
                    # SAATLİK VERİ ÇEK (Giriş Yeri İçin)
                    df_hourly = get_data(hisse, tv, 'HOURLY')
                    if df_hourly is not None:
                        giris, stop, tp1, tp2 = calculate_metrics(df_daily, df_hourly, fiyat)
                        
                        # YÜZDE HESAPLARI (Eski V10'daki gibi)
                        kazanc1 = round(((tp1 - giris)/giris)*100, 2)
                        kazanc2 = round(((tp2 - giris)/giris)*100, 2)

                        msg = f"🟢 <b>GÜNLÜK TREND YAKALANDI! (#{hisse})</b>\n\n"
                        msg += f"🦁 <b>Hisse:</b> #{hisse}\n"
                        msg += f"⭐ <b>Kalite:</b> {puan}/100\n"
                        msg += f"💰 <b>Akıllı Giriş:</b> {giris} TL\n"
                        msg += f"---------------------------------\n"
                        msg += f"🎯 <b>Hedef 1 (Kar Al):</b> {tp1} TL (+%{kazanc1})\n"
                        msg += f"🚀 <b>Hedef 2 (Ana Hedef):</b> {tp2} TL (+%{kazanc2})\n"
                        msg += f"---------------------------------\n"
                        msg += f"🛡️ <b>Zarar Kes (Stop):</b> {stop} TL\n"
                        
                        send_telegram(msg)
                        print(f"✅ SİNYAL: {hisse}")
                        hafiza[hisse] = simdi # Hafızaya ekle

            # --- SAT SİNYALİ (KORUMA) ---
            elif sell:
                if hisse in hafiza:
                    # 3 Gün (259200 sn) kuralı
                    gecen_sure = simdi - hafiza[hisse]
                    if gecen_sure < 259200: 
                        msg = f"🔴 <b>DİKKAT! TREND BOZULDU (#{hisse})</b>\nStop Ol / Kar Al."
                        send_telegram(msg)
                        print(f"⚠️ ÇIKIŞ: {hisse}")
                    
                    del hafiza[hisse] # Listeden sil

        except Exception as e:
            continue

    # HAFIZAYI GÜNCELLE
    hafiza_kaydet(hafiza)
    print("🦁 TARAMA TAMAMLANDI. SİSTEM UYKUYA GEÇİYOR.")
