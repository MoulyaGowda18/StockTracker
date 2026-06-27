# test_fix.py
from stock_data import get_stock_data
from indicators import add_indicators
import pandas as pd

print("--- Step 1: Fetching data ---")
data = get_stock_data("AAPL", period="6mo")

print("Columns     :", list(data.columns))
print("Is MultiIndex:", isinstance(data.columns, pd.MultiIndex))
print("Shape        :", data.shape)
print()

print("--- Step 2: Adding indicators ---")
data = add_indicators(data)

print("Columns after:", list(data.columns))
print()
print(data[["Close", "SMA20", "RSI"]].tail(5))
print()

if "RSI" in data.columns:
    print("SUCCESS - RSI column exists")
else:
    print("FAIL - RSI column still missing")