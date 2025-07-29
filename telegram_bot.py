import os
import json
import requests
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from utils import load_signals, calculate_performance

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {
    "Content-Type": "application/json"
}

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram BOT_TOKEN or CHAT_ID is missing")
        return

    if isinstance(message, dict):
        text = (
            f"📡 *Signal Alert* ({message['timeframe']});\n"
            f"🔹 *Asset:* {message['asset']};\n"
            f"📈 *Direction:* {message['direction']};\n"
            f"🎯 *Time:* {message.get('timestamp', 'N/A')};\n"
            f"💬 *Reason:* {message.get('reason', 'N/A')};\n"
            f"📊 *Confidence:* {message.get('confidence', 0)}%"
        )
    else:
        text = str(message)

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(TELEGRAM_API_URL, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"✅ Sent to Telegram: {text.splitlines()[0]}")
        else:
            print(f"❌ Failed to send message to Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")


def send_daily_performance():
    signals = load_signals()
    if not signals:
        send_telegram_message("⚠️ No signals logged today.")
        return

    report = calculate_performance(signals)
    text = (
        "📊 *Daily Performance Summary*\n\n"
        f"✅ Correct: {report['correct']}\n"
        f"❌ Wrong: {report['wrong']}\n"
        f"📈 Accuracy: {report['accuracy']}%\n"
        f"📦 Total Signals: {report['total']}"
    )
    send_telegram_message(text)


def run_telegram_bot_background():
    print("📡 Initializing Telegram bot and scheduler...")
    # Send welcome message
    test_msg = {
        "asset": "SYSTEM",
        "direction": "READY",
        "timeframe": "ALL",
        "reason": "Bot initialized successfully.",
        "confidence": 100,
        "
