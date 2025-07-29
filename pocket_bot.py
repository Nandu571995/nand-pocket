import time
import datetime
import json
from strategy import analyze_signal
from telegram_bot import send_signal_telegram
from pocket_option_scraper import get_candles, get_all_assets
from utils import log_signal, load_signals

TIMEFRAMES = ["1m", "3m", "5m", "10m"]

def validate_signal(signal):
    return signal.get("confidence", 0) >= 65  # Filter weak signals

def generate_signal(asset, timeframe):
    df = get_candles(asset, timeframe, limit=50)
    if df.empty or len(df) < 30:
        print(f"⚠️ Not enough data for {asset} {timeframe}")
        return None

    signal = analyze_signal(df)
    if signal:
        signal.update({
            "asset": asset,
            "timeframe": timeframe,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        })
        return signal
    return None

def start_pocket_bot():
    print("🚀 Pocket Option Signal Bot Running...")

    # Dummy welcome signal
    send_signal_telegram({
        "asset": "SYSTEM",
        "direction": "READY",
        "timeframe": "ALL",
        "reason": "Bot initialized successfully.",
        "confidence": 100
    })

    while True:
        now = datetime.datetime.utcnow()
        seconds = now.second
        print(f"🕒 Tick: {now.strftime('%H:%M:%S')} — Seconds: {seconds}")

        if seconds == 0:
            for asset in get_all_assets():
                for tf in TIMEFRAMES:
                    print(f"🔎 Generating signal for {asset} [{tf}]...")
                    try:
                        signal = generate_signal(asset, tf)
                        if signal and validate_signal(signal):
                            log_signal(signal)
                            send_signal_telegram(signal)
                    except Exception as e:
                        print(f"❌ Error processing {asset} {tf}: {e}")
        time.sleep(1)
