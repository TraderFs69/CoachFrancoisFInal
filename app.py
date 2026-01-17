import streamlit as st
import pandas as pd

from polygon_data import get_polygon_data
from indicators import compute_indicators
from universe import load_sp500_universe

st.set_page_config(
    page_title="Swing Scanner – Edge Score | Trading en Action",
    layout="wide"
)

st.title("📈 Swing Scanner S&P 500 – Edge Score Swing")
st.caption("Méthodologie Trading en Action | Swing trading robuste")

# ─────────────────────────
# PARAMÈTRES UTILISATEUR
# ─────────────────────────
direction = st.selectbox(
    "Direction du scan",
    ["LONG", "SHORT", "BOTH"],
    index=0
)

min_score = st.slider("Edge Score minimum", 40, 100, 65)

max_tickers = st.slider(
    "Nombre max de tickers analysés",
    50, 500, 150
)

capital = st.number_input(
    "Capital ($)",
    min_value=1000,
    value=10000,
    step=1000
)

risk_pct = st.slider(
    "Risque par trade (%)",
    0.25, 3.0, 1.0, 0.25
)

run_scan = st.button("🚀 Lancer le scan")

# ─────────────────────────
# CHARGEMENT UNIVERS
# ─────────────────────────
tickers = load_sp500_universe()[:max_tickers]
st.caption(f"{len(tickers)} tickers analysés")

# ─────────────────────────
# SCAN
# ─────────────────────────
results = []

if run_scan:
    with st.spinner("Scan en cours..."):
        for ticker in tickers:

            df = get_polygon_data(ticker)

            if df is None or len(df) < 250:
                continue

            df = compute_indicators(df)
            last = df.iloc[-1]

            # ───────── Swing conditions
            long_conditions = [
                last.Close > last.EMA50,
                last.EMA50 > last.EMA200,
                last.MACD > last.MACD_signal,
                last.MACD_hist > 0,
                last.RSI >= 50,
                last.ADX >= 20,
                last.Volume > last.Volume_MA20
            ]

            short_conditions = [
                last.Close < last.EMA50,
                last.EMA50 < last.EMA200,
                last.MACD < last.MACD_signal,
                last.MACD_hist < 0,
                last.RSI <= 50,
                last.ADX >= 20,
                last.Volume > last.Volume_MA20
            ]

            swing_long = sum(long_conditions) >= 6
            swing_short = sum(short_conditions) >= 6

            # ───────── Edge Score
            score = 0

            if last.EMA50 > last.EMA200 and last.Close > last.EMA50:
                score += 30
                bias = "LONG"
            elif last.EMA50 < last.EMA200 and last.Close < last.EMA50:
                score += 30
                bias = "SHORT"
            else:
                bias = "NEUTRE"

            score += 25 if abs(last.MACD_hist) > 0 else 0

            if 50 <= last.RSI <= 65:
                score += 15
            elif 45 <= last.RSI < 50:
                score += 8

            score += 15 if last.ADX >= 25 else 8 if last.ADX >= 20 else 0
            score += 10 if last.Volume > last.Volume_MA20 else 0

            atr_ratio = last.ATR / last.Close
            score += 5 if 0.01 <= atr_ratio <= 0.04 else 0

            if score < min_score:
                continue

            if direction == "LONG" and not swing_long:
                continue
            if direction == "SHORT" and not swing_short:
                continue

            # ───────── Position sizing ATR
            risk_amount = capital * (risk_pct / 100)
            stop_distance = 1.5 * last.ATR
            position_size = int(risk_amount / stop_distance) if stop_distance > 0 else 0

            results.append({
                "Ticker": ticker,
                "Bias": bias,
                "Edge Score": score,
                "Swing Long": swing_long,
                "Swing Short": swing_short,
                "Close": round(last.Close, 2),
                "RSI": round(last.RSI, 1),
                "ADX": round(last.ADX, 1),
                "ATR": round(last.ATR, 2),
                "Stop ($)": round(stop_distance, 2),
                "Position Size": position_size,
                "Risk ($)": round(risk_amount, 2)
            })

# ─────────────────────────
# AFFICHAGE & EXPORT
# ─────────────────────────
if results:
    df_results = (
        pd.DataFrame(results)
        .sort_values("Edge Score", ascending=False)
        .reset_index(drop=True)
    )

    st.subheader("📊 Résultats du scan")
    st.dataframe(df_results, use_container_width=True)

    st.download_button(
        "⬇️ Télécharger résultats (CSV)",
        data=df_results.to_csv(index=False),
        file_name="swing_edge_sp500.csv",
        mime="text/csv"
    )
else:
    st.info("Aucun ticker ne respecte les critères.")
