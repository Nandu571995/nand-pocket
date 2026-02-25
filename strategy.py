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


def _clamp(value, lower=0.0, upper=100.0):
    return max(lower, min(upper, value))


def analyze_options_signal(payload):
    """
    Produce an options trading signal using weighted confluence across
    greeks, volatility, technical, fundamental and OI data.
    """
    # Greeks score
    delta_quality = 100 - abs(abs(payload["delta"]) - 0.5) * 180
    gamma_quality = payload["gamma"] * 450
    theta_penalty = abs(payload["theta"]) * 1.2
    vega_quality = 100 - abs(payload["vega"] - 80) * 0.8
    greeks_score = _clamp((delta_quality * 0.35) + (gamma_quality * 0.25) + (vega_quality * 0.25) + (100 - theta_penalty) * 0.15)

    # Volatility regime score
    if payload["iv_rank"] >= 65:
        vol_score = _clamp(70 + (payload["iv_rank"] - 65) * 0.8)
        vol_regime = "High IV"
    elif payload["iv_rank"] <= 30:
        vol_score = _clamp(65 + (30 - payload["iv_rank"]) * 0.7)
        vol_regime = "Low IV"
    else:
        vol_score = _clamp(55 - abs(payload["iv_rank"] - 47.5) * 0.6)
        vol_regime = "Neutral IV"

    # Technical score
    rsi_centered = 100 - abs(payload["rsi"] - 55) * 2
    trend_score = payload["trend_strength"]
    technical_score = _clamp((rsi_centered * 0.4) + (trend_score * 0.6))

    # Fundamental score
    fundamental_score = _clamp(payload["fundamental_score"])

    # OI and sentiment score
    oi_impulse = 50 + (payload["oi_change"] * 1.5)
    pcr_alignment = 100 - abs(payload["pcr"] - 1.0) * 60
    breadth_alignment = 50 + (payload["market_breadth"] * 0.4)
    oi_score = _clamp((oi_impulse * 0.4) + (pcr_alignment * 0.35) + (breadth_alignment * 0.25))

    composite_score = _clamp(
        (greeks_score * 0.30)
        + (vol_score * 0.20)
        + (technical_score * 0.25)
        + (fundamental_score * 0.10)
        + (oi_score * 0.15)
    )

    direction_bias = "Bullish" if payload["delta"] >= 0 else "Bearish"

    if composite_score >= 78:
        signal = f"STRONG {direction_bias}"
    elif composite_score >= 62:
        signal = f"{direction_bias}"
    elif composite_score >= 48:
        signal = "NEUTRAL / RANGE"
    else:
        signal = f"WEAK {direction_bias}"

    if signal.startswith("STRONG") and vol_regime == "Low IV":
        strategy = "Long Call/Put + Optional Debit Spread"
    elif signal.startswith("STRONG") and vol_regime == "High IV":
        strategy = "Ratio Backspread or Directional Credit Spread"
    elif signal == "NEUTRAL / RANGE" and vol_regime == "High IV":
        strategy = "Iron Condor / Short Strangle (hedged)"
    elif signal == "NEUTRAL / RANGE":
        strategy = "Calendar Spread around ATM"
    else:
        strategy = "Defined-risk Vertical Spread"

    rationale = (
        f"{signal} setup with {vol_regime} regime. "
        f"Composite score {composite_score:.1f}/100 built from Greeks ({greeks_score:.1f}), "
        f"volatility ({vol_score:.1f}), technicals ({technical_score:.1f}), "
        f"fundamental ({fundamental_score:.1f}), and OI flow ({oi_score:.1f})."
    )

    return {
        "signal": signal,
        "confidence": int(round(composite_score)),
        "strategy": strategy,
        "rationale": rationale,
        "component_scores": {
            "Greeks": round(greeks_score, 1),
            "Volatility": round(vol_score, 1),
            "Technical": round(technical_score, 1),
            "Fundamental": round(fundamental_score, 1),
            "Open Interest": round(oi_score, 1),
        },
    }
