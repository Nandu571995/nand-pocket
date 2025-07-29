import requests
import pandas as pd

# ✅ Full list of assets to scan (OTC, FX, Crypto, Commodities)
ASSETS = [
    # 🔄 OTC Assets
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC",
    "EUR/JPY OTC", "EUR/GBP OTC", "GBP/JPY OTC", "USD/CAD OTC", "NZD/USD OTC",

    # 💱 Major Forex Pairs
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD",
    "EUR/JPY", "EUR/GBP", "GBP/JPY", "USD/CAD", "NZD/USD",

    # 🪙 Cryptocurrencies
    "BTC/USD", "ETH/USD", "LTC/USD", "XRP/USD",

    # 🛢️ Commodities
    "GOLD/USD", "SILVER/USD", "CRUDE OIL"
]

# ✅ Mapping of timeframe to seconds
TIMEFRAME_MAP = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "10m": 600
}

# ✅ Normalize asset names for URL comp
