import os
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SIGNAL_LOG_PATH = "signals.json"

# Load signals from file
def load_signals():
    try:
        with open(SIGNAL_LOG_PATH, "r") as f:
            return json.load(f)
    except:
        return []

# Handler to display performance summary
def handle_performance(update: Update, context: CallbackContext):
    signals = load_signals()
    if not signals:
        update.message.reply_text("No signals recorded yet.")
        return

    summary = {}

    for s in signals:
        tf = s.get("timeframe", "unknown")
        if tf not in summary:
            summary[tf] = {"correct": 0, "wrong": 0, "total": 0}
        summary[tf]["total"] += 1
        if s.get("success") is True:
            summary[tf]["correct"] += 1
        elif s.get("success") is False:
            summary[tf]["wrong"] += 1

    text = "📊 *Signal Performance Summary*\n\n"
    for tf, stats in summary.items():
        total = stats["total"]
        correct = stats["correct"]
        wrong = stats["wrong"]
        accuracy = round((correct / total) * 100, 1) if total > 0 else 0
        text += f"🕒 *{tf}*\n✅ {correct}  ❌ {wrong}  📈 {accuracy}% accuracy\n\n"

    update.message.reply_text(text, parse_mode="Markdown")

# Send a trading signal as Telegram message
def send_telegram_message(signal):
    text = (
        f"📢 *Next Candle {signal['timeframe'].upper()} Signal*\n\n"
        f"🪙 *Asset:* {signal['asset']}\n"
        f"📈 *Direction:* {signal['direction']}\n"
        f"🧠 *Confidence:* {signal.get('confidence', 'N/A')}%\n"
        f"📝 *Reason:* {signal.get('reason', 'N/A')}\n"
        f"⏰ *Time:* {signal.get('timestamp', '')}"
    )
    updater.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="Markdown")

# Initialize Telegram bot
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add performance command
dispatcher.add_handler(CommandHandler("performance", handle_performance))

# Only run polling if script is executed directly
if __name__ == "__main__":
    print("🤖 Telegram bot is polling...")
    updater.start_polling()
    updater.idle()
