import pandas as pd


def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    BUY  → RSI < 30 and price above SMA20 (oversold bounce)
    SELL → RSI > 70 and price below SMA20 (overbought rejection)
    """
    data = data.copy()

    required = {"RSI", "SMA20", "Close"}
    missing = required - set(data.columns)
    if missing:
        raise KeyError(
            f"generate_signals() is missing columns: {missing}\n"
            f"Ensure add_indicators() ran successfully before this call."
        )

    data["Signal"] = ""

    buy_mask  = (data["RSI"] < 30) & (data["Close"] > data["SMA20"])
    sell_mask = (data["RSI"] > 70) & (data["Close"] < data["SMA20"])

    data.loc[buy_mask,  "Signal"] = "BUY"
    data.loc[sell_mask, "Signal"] = "SELL"

    return data