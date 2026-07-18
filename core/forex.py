"""
Forex analysis module for AI Market Trend Analyzer.
Fetches and analyzes forex pairs and trends.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
import logging
from datetime import datetime, timedelta
from core.market_data import MarketDataFetcher
from core.indicators import TechnicalIndicators, SignalGenerator
from config import MarketConfig

logger = logging.getLogger(__name__)


class ForexAnalyzer:
    """
    Analyze forex pairs and detect trends.
    """
    
    def __init__(self):
        """Initialize forex analyzer."""
        self.fetcher = MarketDataFetcher()
        self.indicators = TechnicalIndicators()
        self.config = MarketConfig()
    
    def analyze_forex_pair(self, pair_ticker: str, period: str = '1mo') -> Optional[Dict]:
        """
        Analyze a forex pair comprehensively.
        
        Args:
            pair_ticker: Forex pair ticker (e.g., 'EURUSD=X')
            period: Analysis period (default: 1mo)
            
        Returns:
            Dictionary with forex analysis or None if failed
        """
        try:
            logger.info(f"Analyzing forex pair {pair_ticker}")
            
            # Fetch data
            data = self.fetcher.get_stock_data(pair_ticker, period=period, interval='1d')
            if data is None or data.empty:
                logger.warning(f"No data for {pair_ticker}")
                return None
            
            # Calculate indicators
            close_prices = data['Close']
            
            rsi = self.indicators.calculate_rsi(close_prices)
            macd, signal, histogram = self.indicators.calculate_macd(close_prices)
            sma_short = self.indicators.calculate_sma(close_prices, period=20)
            sma_long = self.indicators.calculate_sma(close_prices, period=50)
            upper_bb, middle_bb, lower_bb = self.indicators.calculate_bollinger_bands(close_prices)
            atr = self.indicators.calculate_atr(data['High'], data['Low'], close_prices)
            
            # Current values
            current_price = close_prices.iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_macd = macd.iloc[-1]
            current_signal = signal.iloc[-1]
            current_sma_short = sma_short.iloc[-1]
            current_sma_long = sma_long.iloc[-1]
            current_atr = atr.iloc[-1]
            
            # Trend detection
            trend = self._detect_trend(current_price, current_sma_short, current_sma_long)
            
            # Support and resistance
            support, resistance = self._calculate_support_resistance(data, period=20)
            
            # Volume trend
            volume_trend = self._analyze_volume_trend(data)
            
            # Generate signals
            rsi_signal = SignalGenerator.generate_rsi_signal(current_rsi)
            macd_signal = SignalGenerator.generate_macd_signal(current_macd, current_signal)
            trend_signal = SignalGenerator.generate_trend_signal(current_price, current_sma_short, current_sma_long)
            
            # Calculate strength
            strength = self._calculate_trend_strength(current_rsi, current_macd, current_signal)
            
            # Price change
            price_change = ((current_price - close_prices.iloc[-5]) / close_prices.iloc[-5]) * 100 if len(close_prices) >= 5 else 0
            
            return {
                'pair': pair_ticker,
                'current_price': current_price,
                'price_change_5d': price_change,
                'trend': trend,
                'trend_strength': strength,
                'rsi': current_rsi,
                'rsi_signal': rsi_signal,
                'macd': current_macd,
                'signal_line': current_signal,
                'macd_signal': macd_signal,
                'sma_short': current_sma_short,
                'sma_long': current_sma_long,
                'trend_signal': trend_signal,
                'atr': current_atr,
                'support': support,
                'resistance': resistance,
                'volume_trend': volume_trend,
                'bb_upper': upper_bb.iloc[-1],
                'bb_middle': middle_bb.iloc[-1],
                'bb_lower': lower_bb.iloc[-1],
            }
            
        except Exception as e:
            logger.error(f"Error analyzing forex pair {pair_ticker}: {str(e)}")
            return None
    
    def analyze_all_forex_pairs(self, period: str = '1mo') -> Dict[str, Dict]:
        """
        Analyze all configured forex pairs.
        
        Args:
            period: Analysis period (default: 1mo)
            
        Returns:
            Dictionary of analyses indexed by pair name
        """
        results = {}
        
        for pair_name, pair_ticker in self.config.FOREX_PAIRS.items():
            try:
                analysis = self.analyze_forex_pair(pair_ticker, period=period)
                if analysis:
                    results[pair_name] = analysis
            except Exception as e:
                logger.error(f"Error analyzing {pair_name}: {str(e)}")
                continue
        
        logger.info(f"Analyzed {len(results)} forex pairs")
        return results
    
    @staticmethod
    def _detect_trend(price: float, sma_short: float, sma_long: float) -> str:
        """
        Detect trend based on moving averages.
        
        Args:
            price: Current price
            sma_short: Short-term SMA
            sma_long: Long-term SMA
            
        Returns:
            Trend string (Bullish, Bearish, Neutral)
        """
        if sma_short > sma_long and price > sma_short:
            return "Bullish"
        elif sma_short < sma_long and price < sma_short:
            return "Bearish"
        else:
            return "Neutral"
    
    @staticmethod
    def _calculate_support_resistance(data: pd.DataFrame, period: int = 20) -> Tuple[float, float]:
        """
        Calculate support and resistance levels.
        
        Args:
            data: OHLCV data
            period: Lookback period (default: 20)
            
        Returns:
            Tuple of (support, resistance)
        """
        recent_data = data.tail(period)
        support = recent_data['Low'].min()
        resistance = recent_data['High'].max()
        
        return support, resistance
    
    @staticmethod
    def _analyze_volume_trend(data: pd.DataFrame) -> str:
        """
        Analyze volume trend.
        
        Args:
            data: OHLCV data
            
        Returns:
            Volume trend string (Increasing, Decreasing, Stable)
        """
        if len(data) < 3:
            return "Insufficient Data"
        
        recent_volume = data['Volume'].iloc[-1]
        previous_volume = data['Volume'].iloc[-2]
        avg_volume = data['Volume'].tail(20).mean()
        
        if recent_volume > avg_volume * 1.2:
            return "Increasing"
        elif recent_volume < avg_volume * 0.8:
            return "Decreasing"
        else:
            return "Stable"
    
    @staticmethod
    def _calculate_trend_strength(rsi: float, macd: float, signal: float) -> float:
        """
        Calculate overall trend strength (0-100).
        
        Args:
            rsi: RSI value
            macd: MACD value
            signal: Signal line value
            
        Returns:
            Trend strength score
        """
        # RSI strength (0-100, normalized from 0-100)
        rsi_strength = abs(rsi - 50) / 50
        
        # MACD strength (normalized)
        macd_strength = min(abs(macd - signal) / max(abs(macd), 1), 1)
        
        # Average strength
        strength = ((rsi_strength + macd_strength) / 2) * 100
        
        return strength


class ForexCorrelation:
    """
    Calculate and analyze correlations between forex pairs.
    """
    
    def __init__(self):
        """Initialize forex correlation analyzer."""
        self.fetcher = MarketDataFetcher()
        self.config = MarketConfig()
    
    def calculate_pair_correlations(self, period: str = '3mo') -> Optional[pd.DataFrame]:
        """
        Calculate correlations between all forex pairs.
        
        Args:
            period: Data period (default: 3mo)
            
        Returns:
            Correlation matrix DataFrame or None if failed
        """
        try:
            logger.info("Calculating forex pair correlations")
            
            pair_tickers = list(self.config.FOREX_PAIRS.values())
            correlation = self.fetcher.get_correlation_matrix(pair_tickers, period=period)
            
            if correlation is not None:
                logger.info(f"Successfully calculated correlations for {len(pair_tickers)} pairs")
            
            return correlation
            
        except Exception as e:
            logger.error(f"Error calculating pair correlations: {str(e)}")
            return None


logger.info("Forex analysis module loaded successfully")
