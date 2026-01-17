import pandas as pd
import streamlit as st

def load_sp500_universe():

    uploaded_file = st.file_uploader(
        "📂 Téléverse le fichier sp500_constituents.xlsx",
        type=["xlsx"]
    )

    if uploaded_file is None:
        st.warning("Veuillez téléverser le fichier S&P 500.")
        return []

    df = pd.read_excel(uploaded_file)

    if "Symbol" not in df.columns:
        st.error("La colonne 'Symbol' est introuvable.")
        return []

    return (
        df["Symbol"]
        .dropna()
        .astype(str)
        .str.upper()
        .unique()
        .tolist()
    )
