import os
import json
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ START COMMAND
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is running. Use /performance to check stats.")

# 📊 PERFORMANCE COMMAND
def performance(update: Update, context: CallbackContext):
    try:
        with open("signals.json", "r") as f:
            signals = json.load(f)

        total = len(signals)
        win = sum(1 for s in signals if s["result"] == "WIN")
        loss = sum(1 for s in signals if s["result"] == "LOSS")
        pending = total - win - loss

        timeframes = {}
        for s in signals:
            tf = s["timeframe"]
            if tf not in timeframes:
                timeframes[tf] = {"win": 0, "loss": 0}
            if s["result"] == "WIN":
                timeframes[tf]["win"] += 1
            elif s["result"] == "LOSS":
                timeframes[tf]["loss"] += 1

        msg = f"📊 Performance Summary:\nTotal Signals: {total}\n✅ WIN: {win}\n❌ LOSS: {loss}\n⏳ Pending: {pending}\n\n"
        for tf, tf_stats in timeframes.items():
            total_tf = tf_stats["win"] + tf_stats["loss"]
            acc = (tf_stats["win"] / total_tf * 100) if total_tf > 0 else 0
            msg += f"🕐 {tf}: {acc:.2f}% accuracy ({tf_stats['win']}W/{tf_stats['loss']}L)\n"

        update.message.reply_text(msg)
    except Exception as e:
        logging.error(f"Error in /performance: {e}")
        update.message.reply_text("⚠️ Could not fetch performance stats.")

# 📡 SEND SIGNAL PROGRAMMATICALLY
def send_signal_to_telegram(signal: dict):
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
        logging.error(f"Failed to send signal: {e}")

# 🚀 RUN THE BOT
def run_telegram_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("performance", performance))

    logging.info("🤖 Telegram bot is running...")
    updater.start_polling()
    updater.idle()


# 🧪 Optional: Run directly for testing
if __name__ == "__main__":
    run_telegram_bot()
