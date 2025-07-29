# =======================
# 📦 File: strategy.py
# =======================
import pandas as pd
import ta

def generate_signal(df):
    if df is None or df.empty or len(df) < 50:
        return None, None, 0

    try:
        df = df.copy()
        df['EMA20'] = ta.trend.ema_indicator(df['close'], window=20)
        df['EMA50'] = ta.trend.ema_indicator(df['close'], window=50)
        df['MACD'] = ta.trend.macd_diff(df['close'])
        df['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()

        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        signals = []
        confidence = 0

        if last_row['EMA20'] > last_row['EMA50'] and prev_row['EMA20'] <= prev_row['EMA50']:
            signals.append("EMA Bullish Crossover")
            confidence += 30
        elif last_row['EMA20'] < last_row['EMA50'] and prev_row['EMA20'] >= prev_row['EMA50']:
            signals.append("EMA Bearish Crossover")
            confidence += 30

        if last_row['MACD'] > 0 and prev_row['MACD'] <= 0:
            signals.append("MACD Bullish Crossover")
            confidence += 25
        elif last_row['MACD'] < 0 and prev_row['MACD'] >= 0:
            signals.append("MACD Bearish Crossover")
            confidence += 25

        if last_row['RSI'] < 30:
            signals.append("RSI Oversold")
            confidence += 20
        elif last_row['RSI'] > 70:
            signals.append("RSI Overbought")
            confidence += 20

        if last_row['close'] > last_row['open']:
            direction = "GREEN"
        else:
            direction = "RED"

        reason = ", ".join(signals) if signals else "No strong signal"
        confidence = min(confidence, 100)

        return direction, reason, confidence

    except Exception as e:
        print(f"❌ Strategy error: {e}")
        return None, None, 0
