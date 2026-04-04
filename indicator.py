import pandas as pd
import numpy as np
from typing import Tuple


class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1])

    @staticmethod
    def calculate_macd(prices: pd.Series) -> Tuple[float, float]:
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return float(macd.iloc[-1]), float(signal.iloc[-1])

    @staticmethod
    def calculate_bollinger_bands(
        prices: pd.Series, window: int = 20
    ) -> Tuple[float, float, float]:
        """Returns (Upper Band, Middle Band, Lower Band)"""
        sma = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        return (
            float(upper_band.iloc[-1]),
            float(sma.iloc[-1]),
            float(lower_band.iloc[-1]),
        )

    @staticmethod
    def calculate_sma(prices: pd.Series, window: int) -> float:
        """Standard Simple Moving Average (SMA)"""
        return float(prices.rolling(window=window).mean().iloc[-1])

    @staticmethod
    def calculate_atr(
        high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
    ) -> float:
        """Average True Range - measures market volatility/risk"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return float(atr.iloc[-1])
