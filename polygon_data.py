import requests
import pandas as pd
import streamlit as st
import time

API_KEY = st.secrets["POLYGON_API_KEY"]

@st.cache_data(ttl=3600, show_spinner=False)
def get_polygon_data(ticker, timeframe="day", limit=300):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{timeframe}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": limit,
        "apiKey": API_KEY
    }

    try:
        r = requests.get(url, params=params, timeout=10)

        # ❌ Erreurs HTTP
        if r.status_code != 200:
            return None

        # ❌ Réponse vide
        if not r.text or r.text.strip() == "":
            return None

        data = r.json()

        # ❌ Polygon renvoie parfois un JSON sans results
        if "results" not in data or data["results"] is None:
            return None

        df = pd.DataFrame(data["results"])

        if df.empty:
            return None

        df["t"] = pd.to_datetime(df["t"], unit="ms")
        df.set_index("t", inplace=True)

        df.rename(columns={
            "o": "Open",
            "h": "High",
            "l": "Low",
            "c": "Close",
            "v": "Volume"
        }, inplace=True)

        return df

    except requests.exceptions.RequestException:
        return None

    except ValueError:
        # JSONDecodeError tombe ici
        return None
