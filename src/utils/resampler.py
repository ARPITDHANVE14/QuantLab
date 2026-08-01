import pandas as pd


def resample_to_2m(df):

    df = df.copy()

    df.set_index("date", inplace=True)

    df_2m = (
        df
        .resample("2min")
        .agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        })
        .dropna()
    )

    df_2m.reset_index(inplace=True)

    return df_2m