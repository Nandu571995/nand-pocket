# pocket_option_scraper.py

import requests
import datetime
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_all_assets():
    url = "https://pocketoption.com/en/cabinet/demo/"
    response = requests.get(url, headers=HEADERS)
    assets = [
        "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDUSD_otc",
        "NZDUSD_otc", "USDCHF_otc", "USDCAD_otc", "EURGBP_otc",
        "EURJPY_otc", "GBPJPY_otc", "AUDJPY_otc", "AUDNZD_otc",
        "BTCUSD_otc", "ETHUSD_otc", "LTCUSD_otc", "XRPUSD_otc",
        "XAUUSD_otc", "XAGUSD_otc", "USOIL_otc"
    ]
    return assets

def get_candles(asset, interval="60", limit=3):
    now = int(time.time())
    url = f"https://api.pocketoption.com/api/v1/candles/{asset}?period={interval}&limit={limit}&to={now}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print(f"Error fetching candles for {asset}: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception while getting candles for {asset}: {e}")
        return []
