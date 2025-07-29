from telegram.ext import CommandHandler
from utils import load_signals
from telegram import Update
from telegram.ext import CallbackContext

def get_performance():
    signals = load_signals()
    stats = {tf: {"✅": 0, "❌": 0} for tf in ["1m", "3m", "5m", "10m"]}

    for s in signals:
        tf = s.get("timeframe")
        if tf in stats and "result" in s:
            stats[tf][s["result"]] += 1

    report = "📊 *Signal Performance*\n"
    for tf, tf_stats in stats.items():
        total = tf_stats["✅"] + tf_stats["❌"]
        if total == 0:
            continue
        accuracy = (tf_stats["✅"] / total) * 100
        report += f"\n🕒 {tf} — ✅ {tf_stats['✅']} / ❌ {tf_stats['❌']} — *{accuracy:.1f}%*\n"
    return report or "No signal history yet."

def get_latest_signals():
    signals = load_signals()[-5:]  # Last 5
    if not signals:
        return "No signals found."

    text = "🕵️ *Latest 5 Signals:*\n"
    for s in signals:
        text += (
            f"\n🕒 {s['timeframe']} | {s['asset']} | {s['direction']} | "
            f"{s.get('confidence', '?')}% | {s['timestamp']}"
        )
    return text

def handle_performance(update: Update, context: CallbackContext):
    report = get_performance()
    update.message.reply_text(report, parse_mode='Markdown')

def handle_latest(update: Update, context: CallbackContext):
    report = get_latest_signals()
    update.message.reply_text(report, parse_mode='Markdown')

# Add these handlers to dispatcher
dispatcher.add_handler(CommandHandler("performance", handle_performance))
dispatcher.add_handler(CommandHandler("latest", handle_latest))
