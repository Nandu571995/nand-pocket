import json
import os
from datetime import datetime

SIGNALS_FILE = "signals.json"

def load_signals():
    if not os.path.exists(SIGNALS_FILE):
        return []
    with open(SIGNALS_FILE, "r") as file:
        return json.load(file)

def log_signal(signal):
    signals = load_signals()
    signals.append(signal)
    with open(SIGNALS_FILE, "w") as file:
        json.dump(signals, file, indent=2)

def evaluate_signal_performance():
    signals = load_signals()
    result = {
        "1m": {"total": 0, "correct": 0},
        "3m": {"total": 0, "correct": 0},
        "5m": {"total": 0, "correct": 0},
        "10m": {"total": 0, "correct": 0},
    }

    for signal in signals:
        tf = signal.get("timeframe")
        if tf not in result:
            continue

        result[tf]["total"] += 1
        if signal.get("result") == "correct":
            result[tf]["correct"] += 1

    performance_stats = {
        tf: {
            "accuracy": round((data["correct"] / data["total"]) * 100, 2) if data["total"] else 0,
            "total": data["total"],
            "correct": data["correct"],
        }
        for tf, data in result.items()
    }

    return performance_stats
