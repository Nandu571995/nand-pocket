import json
from datetime import datetime
from pocket_option_scraper import get_latest_candle

def load_signals(filepath='signals.json'):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading signals: {e}")
        return []

def save_signals(data, filepath='signals.json'):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving signals: {e}")

def validate_signals():
    signals = load_signals()
    now = datetime.utcnow()

    for signal in signals:
        if 'result' not in signal and 'asset' in signal and 'timeframe' in signal:
            end_time_str = signal['end_time']
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

            if now >= end_time:
                # Get latest candle for asset & timeframe
                candle = get_latest_candle(signal['asset'], signal['timeframe'])

                if candle:
                    direction = signal['direction'].lower()
                    candle_result = 'green' if candle['close'] > candle['open'] else 'red'

                    if (direction == 'green' and candle_result == 'green') or (direction == 'red' and candle_result == 'red'):
                        signal['result'] = 'correct'
                    else:
                        signal['result'] = 'wrong'

    save_signals(signals)

def calculate_performance(signals):
    correct = 0
    wrong = 0

    for signal in signals:
        if 'result' in signal:
            if signal['result'] == 'correct':
                correct += 1
            elif signal['result'] == 'wrong':
                wrong += 1

    total = correct + wrong
    accuracy = round((correct / total) * 100, 2) if total > 0 else 0.0

    return {
        'correct': correct,
        'wrong': wrong,
        'accuracy': accuracy,
        'total': total
    }
