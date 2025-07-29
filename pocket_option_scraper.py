import requests
import datetime
import pandas as pd

# Predefined list of OTC and major currency pairs + Commodities
ASSETS = [
    # Major currency pairs
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD", "EUR/GBP",
    # OTC assets
    "EUR/USD_otc", "GBP/USD_otc", "USD/JPY_otc", "USD/CHF_otc", "AUD/USD_otc", "NZD/USD_otc",
    "USD/CAD_otc", "EUR/GBP_otc", "EUR/JPY_otc", "GBP/JPY_otc", "AUD/JPY_otc", "USD/TRY_otc", "USD/ZAR_otc",
    # Commodities & Crypto
    "GOLD", "BTC/USD", "ETH/USD", "LTC/USD"
]

TIMEFRAME_MAP = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "10m": 600
}

def fetch_candles(asset: str, timeframe="1m", limit=100) -> pd.DataFrame:
    """
    Fetch real-time historical candle data from Pocket Option chart API.
    """
    # Construct Pocket Option format
    symbol = asset.replace("/", "").lower()
    if "otc" in asset.lower():
        symbol = symbol.replace("_otc", "") + "_otc"
    elif asset in ["GOLD", "BTC/USD", "ETH/USD", "LTC/USD"]:
        symbol = symbol.lower().replace("/", "") + "_otc"

    url = f"https://api.pocketoption.com/chart/history/{symbol}?period={TIMEFRAME_MAP[timeframe]}&limit={limit}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        candles = []
        for i in range(len(data['t'])):
            candles.append({
                "time": datetime.datetime.utcfromtimestamp(data['t'][i]).strftime("%H:%M"),
                "open": data['o'][i],
                "close": data['c'][i],
                "high": data['h'][i],
                "low": data['l'][i],
                "volume": data['v'][i],
            })

        return pd.DataFrame(candles)

    except Exception as e:
        print(f"❌ Error fetching data for {asset}: {e}")
        return pd.DataFrame([])

def get_candles(asset, timeframe="1m", limit=100):
    """
    Wrapper to fetch recent candles for given asset and timeframe.
    """
    return fetch_candles(asset, timeframe, limit)

def get_all_assets():
    """
    Return list of all assets supported.
    """
    return ASSETS
