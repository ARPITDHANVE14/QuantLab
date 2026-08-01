import pandas as pd


class Backtester:

    def __init__(self, df):
        self.df = df
        self.trades = []

    def run(self):

        in_trade = False
        allow_entry = True

        entry_price = None
        entry_time = None

        for _, row in self.df.iterrows():

            # ----------------------------
            # Reset Logic
            # ----------------------------
            if row["close"] > row["EMA169_LOW"]:
                allow_entry = True

            # ----------------------------
            # Entry
            # ----------------------------
            if (
                not in_trade
                and allow_entry
                and row["ENTRY"]
            ):

                in_trade = True
                allow_entry = False

                entry_price = row["close"]
                entry_time = row["date"]

                continue

            # ----------------------------
            # Exit Logic
            # ----------------------------
            if in_trade:

                exit_reason = None

                # Stop Loss
                if row["close"] > row["EMA169_HIGH"]:
                    exit_reason = "STOP LOSS"

                # Target
                elif row["close"] > row["EMA13"]:
                    exit_reason = "TARGET"

                if exit_reason:

                    exit_price = row["close"]

                    pnl = entry_price - exit_price

                    self.trades.append({
                        "Entry Time": entry_time,
                        "Entry Price": entry_price,
                        "Exit Time": row["date"],
                        "Exit Price": exit_price,
                        "PnL": pnl,
                        "Reason": exit_reason
                    })

                    in_trade = False

        return pd.DataFrame(self.trades)

    def performance(self, trades):

        if trades.empty:
            print("No trades generated.")
            return

        total_trades = len(trades)

        winning_trades = (trades["PnL"] > 0).sum()
        losing_trades = (trades["PnL"] <= 0).sum()

        win_rate = (winning_trades / total_trades) * 100

        gross_profit = trades.loc[
            trades["PnL"] > 0,
            "PnL"
        ].sum()

        gross_loss = abs(
            trades.loc[
                trades["PnL"] <= 0,
                "PnL"
            ].sum()
        )

        net_points = trades["PnL"].sum()

        average_win = trades.loc[
            trades["PnL"] > 0,
            "PnL"
        ].mean()

        average_loss = trades.loc[
            trades["PnL"] <= 0,
            "PnL"
        ].mean()

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss != 0
            else float("inf")
        )

        largest_win = trades["PnL"].max()
        largest_loss = trades["PnL"].min()

        print("\n" + "=" * 60)
        print("BANKNIFTY STRATEGY BACKTEST REPORT")
        print("=" * 60)

        print(f"Total Trades      : {total_trades}")
        print(f"Winning Trades    : {winning_trades}")
        print(f"Losing Trades     : {losing_trades}")
        print(f"Win Rate          : {win_rate:.2f}%")
        print(f"Net Points        : {net_points:.2f}")
        print(f"Gross Profit      : {gross_profit:.2f}")
        print(f"Gross Loss        : {gross_loss:.2f}")
        print(f"Average Win       : {average_win:.2f}")
        print(f"Average Loss      : {average_loss:.2f}")
        print(f"Largest Win       : {largest_win:.2f}")
        print(f"Largest Loss      : {largest_loss:.2f}")
        print(f"Profit Factor     : {profit_factor:.2f}")

        print("=" * 60)

        return {
            "Total Trades": total_trades,
            "Winning Trades": winning_trades,
            "Losing Trades": losing_trades,
            "Win Rate": win_rate,
            "Net Points": net_points,
            "Profit Factor": profit_factor
        }