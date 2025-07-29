# telegram_bot.py

import os
import json
from telegram import Bot
from telegram.ext import Updater
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(message: str):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        try:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        except Exception as e:
            print(f"Failed to send message: {e}")
    else:
        print("Telegram token or chat ID not set.")

def calculate_accuracy():
    try:
        with open("signals.json", "r") as f:
            signals = json.load(f)
        summary = {}
        for tf, items in signals.items():
            total = len(items)
            if total == 0:
                continue
            correct = sum(1 for x in items if x.get("result") == "✅")
            acc = round((correct / total) * 100, 2)
            summary[tf] = acc
        return summary
    except Exception as e:
        print(f"Error calculating accuracy: {e}")
        return {}

def send_daily_performance():
    accuracy = calculate_accuracy()
    if not accuracy:
        return
    msg = "📊 *Daily Signal Accuracy Summary*:\n"
    for tf, acc in accuracy.items():
        msg += f"🕒 {tf} — {acc}%\n"
    send_telegram_message(msg)

def run_telegram_bot_background():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_performance, "cron", hour=23, minute=59)
    scheduler.start()
