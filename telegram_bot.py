import logging
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import json
import os

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")  # Replace with your actual bot token
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your_chat_id_here")        # Replace with your actual chat ID
SIGNALS_FILE = "signals.json"

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def load_signals():
    try:
        with open(SIGNALS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def send_telegram_message(message: str):
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logging.error(f"Telegram send error: {e}")

def format_signal(signal: dict) -> str:
    return (
        f"📊 Signal Alert\n"
        f"Pair: {signal['pair']}\n"
        f"Timeframe: {signal['timeframe']}\n"
        f"Direction: {signal['direction'].upper()}\n"
        f"Confidence: {signal['confidence']}%\n"
        f"Time: {signal['time']}\n"
        f"Reason: {signal['reason']}"
    )

# Telegram bot command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Bot is running and ready to send trading signals!")

def last_signal(update: Update, context: CallbackContext):
    signals = load_signals()
    if signals:
        latest = signals[-1]
        update.message.reply_text("🕒 Last Signal:\n" + format_signal(latest))
    else:
        update.message.reply_text("No signals available yet.")

def all_signals(update: Update, context: CallbackContext):
    signals = load_signals()
    if not signals:
        update.message.reply_text("No signals found.")
        return

    for signal in signals[-5:]:
        update.message.reply_text(format_signal(signal))

def accuracy(update: Update, context: CallbackContext):
    from performance import get_latest_performance
    perf = get_latest_performance()
    text = "📈 Performance Stats:\n"
    for tf, stats in perf.items():
        text += (
            f"\n🕒 {tf.upper()}:\n"
            f"✅ {stats['correct_signals']} / {stats['total_signals']} correct\n"
            f"🎯 Accuracy: {stats['accuracy_percent']}%\n"
        )
    update.message.reply_text(text)

def run_bot():
    try:
        updater = Updater(token=BOT_TOKEN, use_context=True)
        dp = updater.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("last", last_signal))
        dp.add_handler(CommandHandler("signals", all_signals))
        dp.add_handler(CommandHandler("accuracy", accuracy))

        updater.start_polling()
        updater.idle()

    except telegram.error.Conflict as e:
        logging.error("⚠️ Telegram conflict: Make sure only one bot instance is running.")
    except Exception as e:
        logging.error(f"Telegram bot failed: {e}")
