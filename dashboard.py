import streamlit as st
import json
import pandas as pd
from datetime import datetime

# Load signal history
def load_signals():
    try:
        with open("signals.json", "r") as f:
            data = json.load(f)
        return data
    except:
        return []

def render_signals_by_timeframe(data, timeframe):
    tf_data = [s for s in data if s["timeframe"] == timeframe]
    tf_data = sorted(tf_data, key=lambda x: x["timestamp"], reverse=True)
    st.subheader(f"📊 Signals - {timeframe}")
    for signal in tf_data:
        st.markdown(f"""
        🕒 `{signal['timestamp']}` — **{signal['asset']}**  
        🔹 Direction: `{signal['direction']}` | Confidence: `{signal['confidence']}%`  
        💬 Reason: {signal['reason']}  
        ✅ Result: `{signal.get('result', 'pending')}`
        ---
        """)

def render_performance(data):
    st.subheader("📈 Performance Summary")
    results = {"1m": [], "3m": [], "5m": [], "10m": []}

    for sig in data:
        tf = sig['timeframe']
        results[tf].append(sig.get("result", "pending"))

    for tf, res_list in results.items():
        total = len(res_list)
        wins = res_list.count("win")
        losses = res_list.count("loss")
        if total:
            accuracy = round(wins / total * 100, 2)
        else:
            accuracy = 0.0

        st.markdown(f"**{tf}**: {wins} ✅ / {losses} ❌ | Accuracy: `{accuracy}%`")

# Streamlit UI
st.set_page_config(page_title="Pocket Option Signals", layout="centered")
st.title("📡 Pocket Option Real-Time Signals")

signal_data = load_signals()

with st.sidebar:
    st.header("🔍 Filters")
    timeframe_filter = st.selectbox("Select Timeframe", ["1m", "3m", "5m", "10m"])

render_signals_by_timeframe(signal_data, timeframe_filter)
render_performance(signal_data)
