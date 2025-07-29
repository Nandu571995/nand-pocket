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


def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram BOT_TOKEN or CHAT_ID is missing")
        return

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(TELEGRAM_API_URL, headers=HEADERS, data=json.dumps(payload))
        if response.status_code == 200:
            print(f"✅ Signal sent to Telegram: {message.splitlines()[0]}")
        else:
            print(f"❌ Failed to send message to Telegram: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Telegram exception: {e}")


def run_telegram_bot_background():
    test_msg = (
        "📡 *Signal Alert* (ALL);\n"
        "🔹 *Asset:* SYSTEM;\n"
        "📈 *Direction:* READY;\n"
        "🎯 *Time:* Initialization;\n"
        "💬 *Reason:* Bot initialized successfully.;\n"
        "📊 *Confidence:* 100%"
    )
    send_telegram_message(test_msg)
    print("✅ Test message sent. If you see this in Telegram, your bot is working!")
