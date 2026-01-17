import pandas as pd
import streamlit as st

def load_sp500_universe():
    uploaded_file = st.file_uploader(
        "📂 Téléverse le fichier sp500_constituents.xlsx",
        type=["xlsx"]
    )

    if uploaded_file is None:
        st.warning("⬆️ Veuillez téléverser le fichier S&P 500.")
        return []

    df = pd.read_excel(uploaded_file)

    # adapte ici si le nom de colonne diffère
    if "Symbol" not in df.columns:
        st.error("❌ Colonne 'Symbol' introuvable dans le fichier.")
        return []

    tickers = (
        df["Symbol"]
        .dropna()
        .astype(str)
        .str.upper()
        .unique()
        .tolist()
    )

    return tickers
