import requests
import pandas as pd
import streamlit as st

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

        if r.status_code != 200:
            return None

        if not r.text:
            return None

        data = r.json()

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

    except Exception:
        return None
