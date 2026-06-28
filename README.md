# 📈 Live Stock Price Tracker

A real-time stock analysis dashboard built with Python and Streamlit.

## 🔗 Live Demo
👉 [Click here to view the live app](https://stocktracker-u5mjudmjq7ynja2oc7xqfn.streamlit.app/)

## Features
- 📊 Live candlestick price chart with SMA20 overlay
- 📉 RSI (14) indicator with overbought/oversold signals
- 🟢 Automatic BUY/SELL signal detection
- 🔍 Supports any stock symbol (AAPL, TSLA, MSFT, NVDA etc.)
- 📅 Configurable time periods (1mo to 2y)

## Tech Stack
- Python
- Streamlit
- Plotly
- Pandas
- yfinance

## 📊 AAPL Price Chart

![AAPL Chart](images/stock_aapl_chart.png)

## 📈 RSI + SSMA Analysis

![RSI SSMA Graph](images/stock_rsi_ssma_graph.png)

## 🚦 Generated Trading Signals (Table)

![Signals Table](images/stock_signals_table.png)

## How to Run Locally
pip install -r requirements.txt
python -m streamlit run app.py
