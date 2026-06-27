import yfinance as yf
import pandas as pd


def get_stock_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch OHLCV data. Handles yfinance 1.4.x MultiIndex columns.
    """
    # Use ticker.history() — cleaner output than yf.download() in v1.4+
    ticker = yf.Ticker(symbol)
    data = ticker.history(period=period, interval=interval)

    if data is None or data.empty:
        raise ValueError(
            f"No data returned for '{symbol}'. "
            "Check the ticker symbol and your internet connection."
        )

    # --- Flatten MultiIndex columns if present (yfinance 1.4.x safety net) ---
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # --- Normalize column names ---
    data.columns = [str(c).strip() for c in data.columns]

    # ticker.history() gives 'Close' directly, but guard against 'Adj Close'
    if "Close" not in data.columns and "Adj Close" in data.columns:
        data.rename(columns={"Adj Close": "Close"}, inplace=True)

    # Drop any rows with NaN in Close (can appear at data boundaries)
    data.dropna(subset=["Close"], inplace=True)
    data.sort_index(inplace=True)

    return data