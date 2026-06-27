import pandas as pd


def add_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds SMA20 and RSI(14) to the DataFrame.
    Uses Wilder's EMA smoothing for accurate RSI.
    """
    data = data.copy()

    # --- Guard: catch column issues early with a clear error ---
    if "Close" not in data.columns:
        raise KeyError(
            f"'Close' column not found in DataFrame.\n"
            f"Actual columns: {list(data.columns)}\n"
            f"This is usually caused by MultiIndex columns from yfinance. "
            f"Fix is in stock_data.py."
        )

    if len(data) < 20:
        raise ValueError(
            f"Not enough data rows ({len(data)}) to compute SMA20. "
            "Fetch at least 1 month of daily data."
        )

    close = data["Close"]  # guaranteed Series now

    # --- SMA 20 ---
    data["SMA20"] = close.rolling(window=20).mean()

    # --- RSI 14 (Wilder's smoothing via EWM) ---
    delta = close.diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=13, min_periods=14).mean()
    avg_loss = loss.ewm(com=13, min_periods=14).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = (100 - (100 / (1 + rs))).round(2)

    return data