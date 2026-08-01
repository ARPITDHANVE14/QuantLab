import pandas as pd


class IndicatorEngine:

    @staticmethod
    def ema(df, source, length, column_name):

        df[column_name] = (
            df[source]
            .ewm(span=length, adjust=False)
            .mean()
        )

        return df


    @staticmethod
    def rsi(df, period=14):

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()

        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

        rs = avg_gain / avg_loss

        df["RSI"] = 100 - (100 / (1 + rs))

        return df