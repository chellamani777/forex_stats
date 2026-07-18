"""
Market data module for AI Market Trend Analyzer.
Fetches real-time market data from multiple sources.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
import requests
from config import MarketConfig, AppConfig, CacheKeys, APIKeys
from utils import cache_data, retry_on_error

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """
    Fetch market data from Yahoo Finance, Alpha Vantage, and other sources.
    """
    
    def __init__(self):
        """Initialize market data fetcher."""
        self.config = MarketConfig()
        self.timeout = AppConfig.TIMEOUT
    
    @retry_on_error(max_retries=3)
    @cache_data(ttl_seconds=3600)
    def get_stock_data(
        self,
        ticker: str,
        period: str = '1y',
        interval: str = '1d'
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data.
        
        Args:
            ticker: Stock ticker symbol
            period: Data period (default: 1y)
            interval: Data interval (default: 1d)
            
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            logger.info(f"Fetching stock data for {ticker}")
            
            stock = yf.Ticker(ticker, timeout=self.timeout)
            data = stock.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data returned for {ticker}")
                return None
            
            # Add ticker column
            data['Ticker'] = ticker
            logger.info(f"Successfully fetched {len(data)} records for {ticker}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {str(e)}")
            return None
    
    @retry_on_error(max_retries=3)
    @cache_data(ttl_seconds=3600)
    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Fetch stock information and fundamentals.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with stock info or None if failed
        """
        try:
            logger.info(f"Fetching stock info for {ticker}")
            
            stock = yf.Ticker(ticker, timeout=self.timeout)
            info = stock.info
            
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
            }
            
        except Exception as e:
            logger.error(f"Error fetching stock info for {ticker}: {str(e)}")
            return None
    
    @retry_on_error(max_retries=3)
    @cache_data(ttl_seconds=1800)
    def get_index_data(self, index_ticker: str, period: str = '1mo') -> Optional[pd.DataFrame]:
        """
        Fetch market index data.
        
        Args:
            index_ticker: Index ticker symbol
            period: Data period (default: 1mo)
            
        Returns:
            DataFrame with index data or None if failed
        """
        try:
            logger.info(f"Fetching index data for {index_ticker}")
            
            data = yf.download(
                index_ticker,
                period=period,
                interval='1d',
                progress=False
            )
            
            if data.empty:
                logger.warning(f"No data returned for index {index_ticker}")
                return None
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching index data for {index_ticker}: {str(e)}")
            return None
    
    @retry_on_error(max_retries=3)
    @cache_data(ttl_seconds=900)
    def get_multiple_stocks(self, tickers: List[str], period: str = '1y') -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks.
        
        Args:
            tickers: List of ticker symbols
            period: Data period (default: 1y)
            
        Returns:
            Dictionary of DataFrames indexed by ticker
        """
        results = {}
        
        for ticker in tickers:
            try:
                data = self.get_stock_data(ticker, period=period)
                if data is not None:
                    results[ticker] = data
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {str(e)}")
                continue
        
        logger.info(f"Successfully fetched data for {len(results)}/{len(tickers)} stocks")
        return results
    
    @retry_on_error(max_retries=3)
    def get_market_movers(
        self,
        tickers: List[str],
        period: str = '1d'
    ) -> Tuple[List[str], List[str]]:
        """
        Get market gainers and losers.
        
        Args:
            tickers: List of ticker symbols to analyze
            period: Period for comparison (default: 1d)
            
        Returns:
            Tuple of (gainers, losers) lists
        """
        gainers = []
        losers = []
        
        try:
            for ticker in tickers:
                data = self.get_stock_data(ticker, period=period)
                if data is not None and len(data) > 1:
                    current_price = data['Close'].iloc[-1]
                    previous_price = data['Close'].iloc[-2]
                    change_pct = ((current_price - previous_price) / previous_price) * 100
                    
                    if change_pct > 0:
                        gainers.append((ticker, change_pct))
                    else:
                        losers.append((ticker, change_pct))
            
            # Sort by magnitude
            gainers.sort(key=lambda x: x[1], reverse=True)
            losers.sort(key=lambda x: x[1])
            
        except Exception as e:
            logger.error(f"Error getting market movers: {str(e)}")
        
        return gainers, losers
    
    @retry_on_error(max_retries=3)
    def get_correlation_matrix(
        self,
        tickers: List[str],
        period: str = '1y'
    ) -> Optional[pd.DataFrame]:
        """
        Calculate correlation matrix between stocks.
        
        Args:
            tickers: List of ticker symbols
            period: Data period (default: 1y)
            
        Returns:
            Correlation matrix DataFrame or None if failed
        """
        try:
            data = self.get_multiple_stocks(tickers, period=period)
            if not data:
                return None
            
            # Extract closing prices
            prices = pd.DataFrame()
            for ticker, df in data.items():
                prices[ticker] = df['Close']
            
            # Calculate returns and correlation
            returns = prices.pct_change()
            correlation = returns.corr()
            
            logger.info(f"Calculated correlation matrix for {len(tickers)} stocks")
            return correlation
            
        except Exception as e:
            logger.error(f"Error calculating correlation matrix: {str(e)}")
            return None


class MarketSentiment:
    """
    Calculate overall market sentiment and health indicators.
    """
    
    def __init__(self, fetcher: MarketDataFetcher):
        """Initialize market sentiment calculator.
        
        Args:
            fetcher: MarketDataFetcher instance
        """
        self.fetcher = fetcher
    
    @cache_data(ttl_seconds=900)
    def get_vix_level(self) -> Optional[float]:
        """
        Get current VIX (Fear Index) level.
        
        Returns:
            VIX value or None if failed
        """
        try:
            vix_data = self.fetcher.get_stock_data('^VIX', period='1d', interval='1h')
            if vix_data is not None and not vix_data.empty:
                return vix_data['Close'].iloc[-1]
        except Exception as e:
            logger.error(f"Error fetching VIX: {str(e)}")
        return None
    
    def interpret_vix(self, vix_level: float) -> str:
        """
        Interpret VIX level.
        
        Args:
            vix_level: Current VIX value
            
        Returns:
            Interpretation string
        """
        if vix_level < 12:
            return "Extremely Low (Complacency)"
        elif vix_level < 16:
            return "Low (Confidence)"
        elif vix_level < 20:
            return "Normal (Neutral)"
        elif vix_level < 30:
            return "Elevated (Caution)"
        else:
            return "High (Fear/Uncertainty)"
    
    @cache_data(ttl_seconds=900)
    def get_market_breadth(self, index_tickers: List[str]) -> Dict[str, float]:
        """
        Calculate market breadth indicators.
        
        Args:
            index_tickers: List of index tickers to analyze
            
        Returns:
            Dictionary with breadth metrics
        """
        try:
            metrics = {}
            
            for ticker in index_tickers:
                data = self.fetcher.get_index_data(ticker, period='1d')
                if data is not None and len(data) > 1:
                    current = data['Close'].iloc[-1]
                    previous = data['Close'].iloc[-2]
                    change_pct = ((current - previous) / previous) * 100
                    metrics[ticker] = change_pct
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating market breadth: {str(e)}")
            return {}


logger.info("Market data module loaded successfully")
