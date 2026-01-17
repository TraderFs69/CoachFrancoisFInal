import ta

def compute_indicators(df):

    df["EMA50"] = ta.trend.ema_indicator(df["Close"], 50)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], 200)

    macd = ta.trend.MACD(df["Close"], 8, 21, 9)
    df["MACD_hist"] = macd.macd_diff()

    df["RSI"] = ta.momentum.rsi(df["Close"], 14)
    df["ADX"] = ta.trend.adx(df["High"], df["Low"], df["Close"], 14)

    df["Volume_MA20"] = df["Volume"].rolling(20).mean()

    df["ATR"] = ta.volatility.average_true_range(
        df["High"], df["Low"], df["Close"], 14
    )

    return df.dropna()
