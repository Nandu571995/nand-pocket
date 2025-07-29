import json
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from utils import evaluate_signal_performance

# 🔐 Replace with your actual token and chat_id in .env or directly here
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def send_telegram_message(signal):
    """Send a formatted trading signal to Telegram."""
    message = (
        f"📡 Signal Alert ({signal['timeframe']});\n"
        f"🔹 Asset: {signal['asset']}\n"
        f"📈 Direction: {signal['direction']}\n"
        f"🕐 Time: {signal.get('time_range', 'Next Candle')}\n"
        f"💬 Reason: {signal['reason']}\n"
        f"📊 Confidence: {signal['confidence']}%\n"
    )
    try:
        updater = Updater(TOKEN, use_context=True)
        updater.bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

def performance_handler(update: Update, context: CallbackContext):
    """Handle the /performance command."
