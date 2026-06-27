import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from stock_data import get_stock_data
from indicators import add_indicators
from strategy import generate_signals

st.set_page_config(page_title="Stock Tracker", layout="wide")
st.title("📈 Live Stock Price Tracker")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    symbol = st.text_input("Stock Symbol", value="AAPL").upper().strip()
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
    interval = st.selectbox("Interval", ["1d", "1wk"], index=0)
    run = st.button("Fetch & Analyze", use_container_width=True)

# ── Main ───────────────────────────────────────────────────────────────────────
if run and symbol:
    try:
        # 1. Fetch
        with st.spinner(f"Fetching {symbol}..."):
            data = get_stock_data(symbol, period=period, interval=interval)

        # 2. Indicators
        data = add_indicators(data)

        # 3. Signals
        data = generate_signals(data)

        # ── Latest snapshot ─────────────────────────────────────────────────
        st.subheader(f"{symbol} — Latest 10 Rows")
        display_cols = ["Open", "High", "Low", "Close", "Volume", "SMA20", "RSI", "Signal"]
        st.dataframe(
            data[display_cols].tail(10)
                .style.format({
                    "Open":  "{:.2f}", "High":  "{:.2f}",
                    "Low":   "{:.2f}", "Close": "{:.2f}",
                    "SMA20": "{:.2f}", "RSI":   "{:.1f}",
                })
        )

        # ── Chart ───────────────────────────────────────────────────────────
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            row_heights=[0.7, 0.3],
            vertical_spacing=0.04,
            subplot_titles=(f"{symbol} Price + SMA20", "RSI (14)"),
        )

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data["Open"], high=data["High"],
            low=data["Low"],   close=data["Close"],
            name="Price",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350",
        ), row=1, col=1)

        # SMA20
        fig.add_trace(go.Scatter(
            x=data.index, y=data["SMA20"],
            name="SMA20", line=dict(color="#f59e0b", width=1.5),
        ), row=1, col=1)

        # BUY markers
        buys = data[data["Signal"] == "BUY"]
        if not buys.empty:
            fig.add_trace(go.Scatter(
                x=buys.index, y=buys["Low"] * 0.995,
                mode="markers", name="BUY",
                marker=dict(symbol="triangle-up", color="#22c55e", size=12),
            ), row=1, col=1)

        # SELL markers
        sells = data[data["Signal"] == "SELL"]
        if not sells.empty:
            fig.add_trace(go.Scatter(
                x=sells.index, y=sells["High"] * 1.005,
                mode="markers", name="SELL",
                marker=dict(symbol="triangle-down", color="#ef4444", size=12),
            ), row=1, col=1)

        # RSI line
        fig.add_trace(go.Scatter(
            x=data.index, y=data["RSI"],
            name="RSI", line=dict(color="#a855f7", width=1.5),
        ), row=2, col=1)

        # Overbought / oversold lines
        for level, color in [(70, "red"), (30, "green")]:
            fig.add_hline(
                y=level, line_dash="dash",
                line_color=color, opacity=0.5,
                row=2, col=1,
            )

        fig.update_layout(
            height=700,
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig)

        # ── Signals table ───────────────────────────────────────────────────
        signals_df = data[data["Signal"] != ""][["Close", "RSI", "Signal"]]
        st.subheader("Generated Signals")
        if not signals_df.empty:
            st.dataframe(signals_df.style.map(
                lambda v: "color: green" if v == "BUY" else "color: red" if v == "SELL" else "",
                subset=["Signal"],
            ))
        else:
            st.info("No BUY/SELL signals detected in this period. Try a longer period.")

    except ValueError as e:
        st.error(f"❌ Data error: {e}")
    except KeyError as e:
        st.error(f"❌ Column error: {e}")
    except Exception as e:
        st.exception(e)