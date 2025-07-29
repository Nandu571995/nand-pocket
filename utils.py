import datetime
import json
import os
import threading


def get_current_time():
    return datetime.datetime.now().strftime("%H:%M")


def load_signals():
    try:
        with open("signals.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_signals(data):
    with open("signals.json", "w") as f:
        json.dump(data, f, indent=2)


def get_confidence_level(score):
    if score >= 80:
        return "🟢 High"
    elif score >= 60:
        return "🟡 Medium"
    else:
        return "🔴 Low"


def format_telegram_message(signal):
    return (
        f"📡 *Signal Alert* ({signal['timeframe'].upper()})"
        f"\n🔹 *Asset:* {signal['asset']}"
        f"\n📈 *Direction:* {signal['direction']}"
        f"\n🎯 *Time:* {signal['time_range']}"
        f"\n💬 *Reason:* {signal['reason']}"
        f"\n📊 *Confidence:* {signal['confidence']}%"
    )


def log(message):
    print(f"{get_current_time()} | {message}")


def safe_run(target):
    def wrapper(*args, **kwargs):
        try:
            target(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ Error in thread: {e}")

    return threading.Thread(target=wrapper, daemon=True)


def is_new_signal(asset, tf, direction, time_range):
    signals = load_signals()
    key = f"{asset}_{tf}"
    return signals.get(key, {}).get("time_range") != time_range


def record_signal(asset, tf, direction, time_range, reason, confidence):
    signals = load_signals()
    key = f"{asset}_{tf}"
    signals[key] = {
        "asset": asset,
        "timeframe": tf,
        "direction": direction,
        "time_range": time_range,
        "reason": reason,
        "confidence": confidence
    }
    save_signals(signals)
