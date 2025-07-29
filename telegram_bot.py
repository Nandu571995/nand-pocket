import json
import threading
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import telegram
from telegram.error import TelegramError
from utils import load_signals, calculate_performance
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Config
TOKEN = os.getenv("TELEGRAM_TOKEN")  # your Telegram bot token from .env
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # your chat ID from .env
bot = telegram.Bot(token=TOKEN)

# Lock to prevent simultaneous sends
send_lock = threading.Lock()

def send_telegram_message(message):
    with send_lock:
        try:
            bot.send_message(chat_id=CHAT_ID, text=message)
        except TelegramError as e:
            print(f"Telegram error: {e}")

def format_signal(asset, timeframe, direction, time_range, confidence, reason):
    return f"""
📡 *Pocket Option Signal*

🪙 *Asset:* {asset}
⏱️ *Timeframe:* {timeframe}
🎯 *Direction:* {direction}
🕒 *Time Range:* {time_range}
📊 *Confidence:* {confidence}%
🧠 *Reason:* {reason}
""".strip()

def send_signal(asset, timeframe, direction, time_range, confidence, reason):
    message = format_signal(asset, timeframe, direction, time_range, confidence, reason)
    send_telegram_message(message)

def send_daily_performance():
    signals = load_signals()
    performance = calculate_performance(signals)

    message = f"""
📊 Daily Performance Summary

✅ Correct: {performance['correct']}
❌ Wrong: {performance['wrong']}
📈 Accuracy: {performance['accuracy']}%
📦 Total Signals: {performance['total']}
"""
    send_telegram_message(message.strip())

def run_telegram_bot_background():
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Kolkata"))
    scheduler.add_job(send_daily_performance, "cron", hour=23, minute=59)
    scheduler.start()

    print("Telegram bot is running in background...")
    while True:
        time.sleep(10)
