import requests
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ✅ List of assets: all major currency pairs + OTC
def get_all_assets():
    return [
        "EURUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC", "AUDUSD_OTC", "NZDUSD_OTC",
        "EURJPY_OTC", "GBPJPY_OTC", "EURGBP_OTC", "USDCHF_OTC",
        "EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "NZDUSD",
        "EURJPY", "GBPJPY", "EURGBP", "USDCHF"
    ]

# ✅ Get multiple candles for a given asset & timeframe
def get_candles(asset, timeframe, limit=50):
    try:
        end_time = int(datetime.utcnow().timestamp())
        url = "https://api.pocketoption.com/chart/history"
        params = {
            "asset": asset,
            "type": timeframe,
            "count": limit,
            "end": end_time
        }

        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json().get("candles", [])

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.set_index('timestamp', inplace=True)
        return df[["open", "high", "low", "close", "volume"]]

    except Exception as e:
        print(f"❌ Error fetching candles for {asset} [{timeframe}]: {e}")
        return pd.DataFrame()

# ✅ Get only the most recent candle for performance validation
def get_latest_candle(asset, timeframe):
    df = get_candles(asset, timeframe, limit=2)
    if not df.empty:
        return df.iloc[-1].to_dict()
    return None
