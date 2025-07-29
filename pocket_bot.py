import time
import datetime
from strategy import analyze_signal
from telegram_bot import send_telegram_message as send_signal_telegram
from pocket_option_scraper import get_candles, get_all_assets
from utils import log_signal

TIMEFRAMES = ["1m", "3m", "5m", "10m"]
CONFIDENCE_THRESHOLD = 65  # Minimum confidence to send signal

def validate_signal(signal: dict) -> bool:
    """Return True if signal confidence is above threshold."""
    return signal.get("confidence", 0) >= CONFIDENCE_THRESHOLD

def generate_signal(asset: str, timeframe: str) -> dict | None:
    """Fetch data and analyze trading signal."""
    df = get_candles(asset, timeframe, limit=50)
    if df.empty or len(df) < 30:
        print(f"⚠️ Not enough data for {asset} [{timeframe}]")
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
    """Main loop that runs continuously and sends signals."""
    print("🚀 Pocket Option Signal Bot Running...")

    # Send startup message
    send_signal_telegram({
        "asset": "SYSTEM",
        "direction": "READY",
        "timeframe": "ALL",
        "reason": "Bot initialized successfully.",
        "confidence": 100,
        "time_range": "-"
    })

    while True:
        now = datetime.datetime.utcnow()
        seconds = now.second
        print(f"🕒 Tick: {now.strftime('%H:%M:%S')}")

        if seconds == 0:
            assets = get_all_assets()
            for asset in assets:
                for tf in TIMEFRAMES:
                    print(f"🔎 Scanning {asset} [{tf}]...")
                    try:
                        signal = generate_signal(asset, tf)
                        if signal and validate_signal(signal):
                            log_signal(signal)
                            send_signal_telegram(signal)
                    except Exception as e:
                        print(f"❌ Error in {asset} [{tf}]: {e}")

        time.sleep(1)
