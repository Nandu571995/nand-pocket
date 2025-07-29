from telegram import Bot
import os

# Your Telegram bot token and chat ID (set via environment or hardcode temporarily)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8062898551:AAFp6Mzz3TU2Ngeqf4gL4KL55S1guuRwcnA")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1014815784")

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(signal):
    try:
        message = f"""📡 *Pocket Option Signal*
🕒 *Timeframe*: {signal['timeframe']}
💱 *Asset*: {signal['asset']}
🎯 *Direction*: {signal['direction']}
⚡ *Confidence*: {signal['confidence']}%
📖 *Reason*: {signal['reason']}
⏰ *Generated At*: {signal.get('timestamp', 'N/A')}"""

        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
        print(f"✅ Signal sent to Telegram: {signal['asset']} {signal['timeframe']}")
    except Exception as e:
        print(f"❌ Failed to send Telegram message: {e}")
