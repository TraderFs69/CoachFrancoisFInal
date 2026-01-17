import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["POLYGON_API_KEY"]

def get_polygon_data(ticker, timeframe="day", limit=300):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{timeframe}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "limit": limit,
        "apiKey": API_KEY
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "results" not in data:
        return None

    df = pd.DataFrame(data["results"])
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
