import json
import os
from datetime import datetime

SIGNALS_FILE = "signals.json"

def log_signal(signal):
    """Append a new signal to signals.json"""
    signal["validated"] = None  # Placeholder for future performance tracking
    if not os.path.exists(SIGNALS_FILE):
        with open(SIGNALS_FILE, "w") as f:
            json.dump([signal], f, indent=4)
    else:
        with open(SIGNALS_FILE, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(signal)
            f.seek(0)
            json.dump(data, f, indent=4)

def load_signals():
    """Load all logged signals"""
    if not os.path.exists(SIGNALS_FILE):
        return []
    with open(SIGNALS_FILE, "r") as f:
        return json.load(f)
