import pandas as pd

SP500_PATH = "/mnt/data/sp500_constituents.xlsx"

def load_sp500_universe():
    df = pd.read_excel(SP500_PATH)

    tickers = (
        df["Symbol"]
        .dropna()
        .astype(str)
        .str.upper()
        .unique()
        .tolist()
    )

    return tickers
