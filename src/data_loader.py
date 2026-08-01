import pandas as pd


class DataLoader:

    REQUIRED_COLUMNS = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]

    @staticmethod
    def load_csv(path):

        df = pd.read_csv(path)

        # Convert date column
        df["date"] = pd.to_datetime(df["date"])

        # Sort by datetime
        df = df.sort_values("date")

        # Reset index
        df.reset_index(drop=True, inplace=True)

        # Validate columns
        missing = [
            col for col in DataLoader.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        return df