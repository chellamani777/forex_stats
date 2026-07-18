"""
Technical indicators module for AI Market Trend Analyzer.
Calculates RSI, MACD, Moving Averages, Bollinger Bands, etc.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
import logging
from config import IndicatorsConfig

logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """
    Calculate technical indicators for price analysis.
    """
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            prices: Series of prices
            period: RSI period (default: 14)
            
        Returns:
            Series of RSI values
        """
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            logger.debug(f"Calculated RSI with period {period}")
            return rsi
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_macd(
        prices: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            prices: Series of prices
            fast: Fast EMA period (default: 12)
            slow: Slow EMA period (default: 26)
            signal: Signal line period (default: 9)
            
        Returns:
            Tuple of (MACD, Signal, Histogram)
        """
        try:
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            
            macd = ema_fast - ema_slow
            signal_line = macd.ewm(span=signal).mean()
            histogram = macd - signal_line
            
            logger.debug(f"Calculated MACD with periods {fast}, {slow}, {signal}")
            return macd, signal_line, histogram
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_sma(prices: pd.Series, period: int = 20) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA).
        
        Args:
            prices: Series of prices
            period: SMA period (default: 20)
            
        Returns:
            Series of SMA values
        """
        try:
            sma = prices.rolling(window=period).mean()
            logger.debug(f"Calculated SMA with period {period}")
            return sma
            
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_ema(prices: pd.Series, period: int = 12) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA).
        
        Args:
            prices: Series of prices
            period: EMA period (default: 12)
            
        Returns:
            Series of EMA values
        """
        try:
            ema = prices.ewm(span=period, adjust=False).mean()
            logger.debug(f"Calculated EMA with period {period}")
            return ema
            
        except Exception as e:
            logger.error(f"Error calculating EMA: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_bollinger_bands(
        prices: pd.Series,
        period: int = 20,
        std_dev: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands.
        
        Args:
            prices: Series of prices
            period: Period for moving average (default: 20)
            std_dev: Number of standard deviations (default: 2.0)
            
        Returns:
            Tuple of (upper_band, middle_band, lower_band)
        """
        try:
            middle = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)
            
            logger.debug(f"Calculated Bollinger Bands with period {period}, std_dev {std_dev}")
            return upper, middle, lower
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR).
        
        Args:
            high: Series of high prices
            low: Series of low prices
            close: Series of close prices
            period: ATR period (default: 14)
            
        Returns:
            Series of ATR values
        """
        try:
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            
            logger.debug(f"Calculated ATR with period {period}")
            return atr
            
        except Exception as e:
            logger.error(f"Error calculating ATR: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
        """
        Calculate On-Balance Volume (OBV).
        
        Args:
            close: Series of close prices
            volume: Series of volumes
            
        Returns:
            Series of OBV values
        """
        try:
            obv = np.where(close > close.shift(), volume, np.where(close < close.shift(), -volume, 0)).cumsum()
            obv_series = pd.Series(obv, index=close.index)
            
            logger.debug("Calculated OBV")
            return obv_series
            
        except Exception as e:
            logger.error(f"Error calculating OBV: {str(e)}")
            return pd.Series()
    
    @staticmethod
    def calculate_stochastic(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14,
        smooth_k: int = 3,
        smooth_d: int = 3
    ) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator.
        
        Args:
            high: Series of high prices
            low: Series of low prices
            close: Series of close prices
            period: Period (default: 14)
            smooth_k: K smoothing (default: 3)
            smooth_d: D smoothing (default: 3)
            
        Returns:
            Tuple of (%K, %D)
        """
        try:
            lowest_low = low.rolling(window=period).min()
            highest_high = high.rolling(window=period).max()
            
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=smooth_d).mean()
            
            k_percent = k_percent.rolling(window=smooth_k).mean()
            
            logger.debug(f"Calculated Stochastic with period {period}")
            return k_percent, d_percent
            
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {str(e)}")
            return pd.Series(), pd.Series()


class SignalGenerator:
    """
    Generate trading signals from technical indicators.
    """
    
    @staticmethod
    def generate_rsi_signal(rsi: float) -> str:
        """
        Generate signal from RSI value.
        
        Args:
            rsi: Current RSI value
            
        Returns:
            Signal string
        """
        if rsi > IndicatorsConfig.RSI_OVERBOUGHT:
            return "Overbought - Sell Signal"
        elif rsi < IndicatorsConfig.RSI_OVERSOLD:
            return "Oversold - Buy Signal"
        else:
            return "Neutral"
    
    @staticmethod
    def generate_macd_signal(macd: float, signal: float) -> str:
        """
        Generate signal from MACD.
        
        Args:
            macd: MACD value
            signal: Signal line value
            
        Returns:
            Signal string
        """
        if macd > signal:
            return "Bullish - Buy Signal"
        elif macd < signal:
            return "Bearish - Sell Signal"
        else:
            return "Neutral"
    
    @staticmethod
    def generate_trend_signal(price: float, sma_short: float, sma_long: float) -> str:
        """
        Generate trend signal from moving averages.
        
        Args:
            price: Current price
            sma_short: Short-term SMA
            sma_long: Long-term SMA
            
        Returns:
            Signal string
        """
        if sma_short > sma_long:
            if price > sma_short:
                return "Strong Uptrend"
            else:
                return "Weak Uptrend"
        else:
            if price < sma_short:
                return "Strong Downtrend"
            else:
                return "Weak Downtrend"


logger.info("Technical indicators module loaded successfully")
