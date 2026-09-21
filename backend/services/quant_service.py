import pandas as pd
import pandas_ta as ta
import yfinance as yf
from typing import Dict, Any


def fetch_market_data(ticker: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    Use yfinance to download historical OHLCV data for the given ticker.
    """
    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(period=period, interval=interval)
    if df.empty:
        raise ValueError(f"No market data found for ticker '{ticker}'")
    return df


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Use pandas-ta to append technical indicators to the dataframe:
    - VWAP (Volume Weighted Average Price)
    - EMA_21 (21-period Exponential Moving Average)
    - RSI_14 (14-period Relative Strength Index)
    """
    df = df.copy()

    # Ensure DatetimeIndex for pandas-ta vwap calculation
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            pass

    # Calculate VWAP
    try:
        vwap_res = df.ta.vwap()
        if isinstance(vwap_res, pd.Series):
            df["VWAP"] = vwap_res
        elif isinstance(vwap_res, pd.DataFrame) and not vwap_res.empty:
            df["VWAP"] = vwap_res.iloc[:, 0]
        else:
            tp = (df["High"] + df["Low"] + df["Close"]) / 3
            df["VWAP"] = (tp * df["Volume"]).cumsum() / df["Volume"].cumsum()
    except Exception:
        tp = (df["High"] + df["Low"] + df["Close"]) / 3
        df["VWAP"] = (tp * df["Volume"]).cumsum() / df["Volume"].cumsum()

    # Calculate EMA 21
    try:
        ema_res = df.ta.ema(length=21)
        if isinstance(ema_res, pd.Series):
            df["EMA_21"] = ema_res
        else:
            df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()
    except Exception:
        df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()

    # Calculate RSI 14
    try:
        rsi_res = df.ta.rsi(length=14)
        if isinstance(rsi_res, pd.Series):
            df["RSI_14"] = rsi_res
        else:
            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df["RSI_14"] = 100 - (100 / (1 + rs))
    except Exception:
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI_14"] = 100 - (100 / (1 + rs))

    return df


def generate_signal(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze the most recent candle.
    - BUY_CALL if closing price is strictly greater than both VWAP and EMA_21, and RSI is between 50 and 70.
    - BUY_PUT if closing price is strictly less than both VWAP and EMA_21, and RSI is between 30 and 50.
    - Otherwise NEUTRAL.
    """
    if df.empty:
        raise ValueError("Cannot generate signal for empty dataframe")

    latest = df.iloc[-1]
    close = float(latest["Close"])
    vwap = float(latest["VWAP"]) if "VWAP" in latest and pd.notna(latest["VWAP"]) else close
    ema_21 = float(latest["EMA_21"]) if "EMA_21" in latest and pd.notna(latest["EMA_21"]) else close
    rsi_14 = float(latest["RSI_14"]) if "RSI_14" in latest and pd.notna(latest["RSI_14"]) else 50.0

    # Determine signal based on rules
    if close > vwap and close > ema_21 and 50.0 <= rsi_14 <= 70.0:
        signal = "BUY_CALL"
    elif close < vwap and close < ema_21 and 30.0 <= rsi_14 <= 50.0:
        signal = "BUY_PUT"
    else:
        signal = "NEUTRAL"

    return {
        "signal": signal,
        "current_price": close,
        "vwap": vwap,
        "ema_21": ema_21,
        "rsi_14": rsi_14,
    }
