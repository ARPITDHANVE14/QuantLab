from config import (
    BANKNIFTY_1M,
    BANKNIFTY_5M,
    BANKNIFTY_15M
)

from data_loader import DataLoader
from utils.resampler import resample_to_2m
from indicators.technical_indicators import IndicatorEngine
from utils.timeframe_merge import merge_timeframes
from strategies.banknifty_strategy import generate_signals
from backtesting.backtester import Backtester


# ===================================
# Load Data
# ===================================

df1 = DataLoader.load_csv(BANKNIFTY_1M)
df5 = DataLoader.load_csv(BANKNIFTY_5M)
df15 = DataLoader.load_csv(BANKNIFTY_15M)


# ===================================
# Generate 2-Minute Candles
# ===================================

df2 = resample_to_2m(df1)


# ===================================
# Indicators (2 Minute)
# ===================================

df2 = IndicatorEngine.ema(df2, "high", 169, "EMA169_HIGH")
df2 = IndicatorEngine.ema(df2, "low", 169, "EMA169_LOW")
df2 = IndicatorEngine.ema(df2, "close", 13, "EMA13")
df2 = IndicatorEngine.rsi(df2)


# ===================================
# Indicators (5 Minute)
# ===================================

df5 = IndicatorEngine.ema(df5, "low", 169, "EMA169_LOW")


# ===================================
# Indicators (15 Minute)
# ===================================

df15 = IndicatorEngine.ema(df15, "low", 169, "EMA169_LOW")


# ===================================
# Merge Timeframes
# ===================================

merged_df = merge_timeframes(df2, df5, df15)


# ===================================
# Generate Strategy Signals
# ===================================

merged_df = generate_signals(merged_df)


# ===================================
# Show Signals
# ===================================

# ===================================
# Backtest Strategy
# ===================================

backtester = Backtester(merged_df)

trades = backtester.run()

print("\nFirst 20 Trades:\n")
print(trades.head(20))

print()

backtester.performance(trades)