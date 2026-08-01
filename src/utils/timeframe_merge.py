import pandas as pd


def merge_timeframes(df2, df5, df15):

    df5 = df5[["date", "close", "EMA169_LOW"]].rename(
        columns={
            "close": "close_5m",
            "EMA169_LOW": "EMA169_LOW_5m"
        }
    )

    df15 = df15[["date", "close", "EMA169_LOW"]].rename(
        columns={
            "close": "close_15m",
            "EMA169_LOW": "EMA169_LOW_15m"
        }
    )

    merged = pd.merge_asof(
        df2.sort_values("date"),
        df5.sort_values("date"),
        on="date",
        direction="backward"
    )

    merged = pd.merge_asof(
        merged.sort_values("date"),
        df15.sort_values("date"),
        on="date",
        direction="backward"
    )

    return merged