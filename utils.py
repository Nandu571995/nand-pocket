import json
import os
from datetime import datetime

SIGNAL_FILE = "signals.json"

def load_signals():
    if not os.path.exists(SIGNAL_FILE):
        return []
    with open(SIGNAL_FILE, "r") as f:
        return json.load(f)

def save_signals(signals):
    with open(SIGNAL_FILE, "w") as f:
        json.dump(signals, f, indent=2)

def log_signal(signal):
    signals = load_signals()
    signals.append(signal)
    save_signals(signals)

def validate_signal(signal, latest_close):
    direction = signal["direction"]
    signal_time = signal["timestamp"]
    expiry = signal["expiry"]
    
    result = "PENDING"
    if direction == "BUY" and latest_close > signal["open"]:
        result = "WIN"
    elif direction == "SELL" and latest_close < signal["open"]:
        result = "WIN"
    else:
        result = "LOSS"

    signal["result"] = result
    return signal

def calculate_performance():
    signals = load_signals()
    summary = {}
    for signal in signals:
        tf = signal["timeframe"]
        result = signal.get("result", "PENDING")
        if tf not in summary:
            summary[tf] = {"WIN": 0, "LOSS": 0, "PENDING": 0}
        summary[tf][result] += 1
    return summary
