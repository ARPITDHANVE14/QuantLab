import pandas as pd


def generate_signals(df):

    df = df.copy()

    # Previous candle values
    df["PREV_CLOSE"] = df["close"].shift(1)
    df["PREV_EMA169_LOW"] = df["EMA169_LOW"].shift(1)

    # Fresh Breakdown
    df["FRESH_BREAKDOWN"] = (
        (df["close"] < df["EMA169_LOW"]) &
        (df["PREV_CLOSE"] >= df["PREV_EMA169_LOW"])
    )

    # RSI Filter
    df["RSI_FILTER"] = df["RSI"] < 50

    # 5 Minute Filter
    df["FILTER_5M"] = (
        df["close_5m"] < df["EMA169_LOW_5m"]
    )

    # 15 Minute Filter
    df["FILTER_15M"] = (
        df["close_15m"] < df["EMA169_LOW_15m"]
    )

    # Time Filter (9:20 AM - 2:45 PM)
    df["TIME"] = df["date"].dt.time

    df["TIME_FILTER"] = (
        (df["TIME"] >= pd.to_datetime("09:20").time()) &
        (df["TIME"] <= pd.to_datetime("14:45").time())
    )

    # Final Entry Signal
    df["ENTRY"] = (
        df["FRESH_BREAKDOWN"] &
        df["RSI_FILTER"] &
        df["FILTER_5M"] &
        df["FILTER_15M"] &
        df["TIME_FILTER"]
    )

    return df