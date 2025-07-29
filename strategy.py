import pandas as pd
import ta

def analyze_signal(df, asset, timeframe):
    """
    Analyze a dataframe of candle data and return a signal dict if any valid signal is found.
    """
    if df.empty or len(df) < 50:
        return None

    # Technical indicators
    df['ema_fast'] = ta.trend.ema_indicator(df['close'], window=9)
    df['ema_slow'] = ta.trend.ema_indicator(df['close'], window=21)
    df['macd'] = ta.trend.macd_diff(df['close'])
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    last = df.iloc[-1]

    direction = None
    reason = []

    if last['ema_fast'] > last['ema_slow']:
        direction = "GREEN"
        reason.append("EMA Crossover")
    elif last['ema_fast'] < last['ema_slow']:
        direction = "RED"
        reason.append("EMA Crossover")

    if last['macd'] > 0:
        reason.append("MACD Bullish")
    elif last['macd'] < 0:
        reason.append("MACD Bearish")

    if last['rsi'] > 70:
        reason.append("RSI Overbought")
    elif last['rsi'] < 30:
        reason.append("RSI Oversold")

    if last['close'] > last['bb_upper']:
        reason.append("Above Bollinger")
    elif last['close'] < last['bb_lower']:
        reason.append("Below Bollinger")

    if not direction:
        return None

    confidence = min(100, len(reason) * 20)

    return {
        "asset": asset,
        "timeframe": timeframe,
        "timestamp": pd.Timestamp.now().strftime("%H:%M"),
        "direction": direction,
        "reason": ", ".join(reason),
        "confidence": confidence
    }
