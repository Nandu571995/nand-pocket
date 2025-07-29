import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {
    "Content-Type": "application/json"
}

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_message(signal):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram BOT_TOKEN or CHAT_ID is missing")
        return

    message = (
        f"📡 *Signal Alert* ({signal.get('timeframe', 'N/A')});\n"
        f"🔹 *Asset:* {signal.get('asset', 'N/A')};\n"
        f"📈 *Direction:* {signal.get('direction', 'N/A')};\n"
        f"🎯 *Time:* {signal.get('timestamp', 'N/A')};\n"
        f"💬 *Reason:* {signal.get('reason', 'N/A')};\n"
        f"📊 *Confidence:* {signal.get('confidence', 0)}%"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(TELEGRAM_API_URL, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"✅ Signal sent to Telegram: {signal.get('asset')} ({signal.get('timeframe')})")
        else:
            print(f"❌ Failed to send message to Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")

def run_telegram_bot_background():
    test_msg = {
        "asset": "SYSTEM",
        "direction": "READY",
        "timeframe": "INIT",
        "timestamp": "Launching",
        "reason": "Bot initialized successfully.",
        "confidence": 100
    }
    send_telegram_message(test_msg)
    print("✅ Test message sent to Telegram.")
