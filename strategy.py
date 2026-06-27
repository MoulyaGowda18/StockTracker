import pandas as pd


def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    BUY  → RSI < 35 (oversold)
    SELL → RSI > 65 (overbought)
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

    buy_mask  = data["RSI"] < 35
    sell_mask = data["RSI"] > 65

    data.loc[buy_mask,  "Signal"] = "BUY"
    data.loc[sell_mask, "Signal"] = "SELL"

    return data