import os
import json
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from dotenv import load_dotenv
from utils import evaluate_signal_performance

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def send_telegram_message(signal: dict):
    """Send formatted trading signal to Telegram."""
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
        logging.error(f"❌ Failed to send signal: {e}")

def performance_handler(update: Update, context: CallbackContext):
    try:
        with open("signals.json", "r") as f:
            signals = json.load(f)

        stats = evaluate_signal_performance(signals)

        summary = (
            f"📊 Performance Summary:\n"
            f"Total Signals: {stats['total']}\n"
            f"✅ WIN: {stats['win']}\n"
            f"❌ LOSS: {stats['loss']}\n"
            f"⏳ Pending: {stats['pending']}\n\n"
        )
        for tf, tf_stats in stats["timeframes"].items():
            acc = tf_stats["accuracy"]
            summary += f"🕐 {tf}: {acc:.2f}% accuracy ({tf_stats['win']}W/{tf_stats['loss']}L)\n"

        update.message.reply_text(summary)

    except Exception as e:
        logging.error(f"⚠️ Error reading performance: {e}")
        update.message.reply_text("⚠️ Could not fetch performance stats.")

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is running. Use /performance to check stats.")

def run_telegram_bot_background():
    try:
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start_command))
        dp.add_handler(CommandHandler("performance", performance_handler))

        updater.start_polling()
        updater.idle()
    except Exception as e:
        logging.error(f"❌ Failed to run Telegram bot: {e}")
