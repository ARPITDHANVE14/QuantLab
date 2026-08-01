from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Folder
DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Raw CSV Files
BANKNIFTY_1M = RAW_DATA_DIR / "banknifty_1m.csv"
BANKNIFTY_5M = RAW_DATA_DIR / "banknifty_5m.csv"
BANKNIFTY_15M = RAW_DATA_DIR / "banknifty_15m.csv"