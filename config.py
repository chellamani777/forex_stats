"""
Configuration module for AI Market Trend Analyzer.
Manages all settings, API keys, and constants.
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ============================================================================
# API KEYS
# ============================================================================
class APIKeys:
    """API keys configuration."""
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    FRED_API_KEY = os.getenv('FRED_API_KEY')

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
class AppConfig:
    """Application configuration."""
    APP_NAME = "AI Market Trend Analyzer"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    TIMEOUT = 30  # API request timeout in seconds
    PAGE_ICON = "📊"
    LAYOUT = "wide"

# ============================================================================
# MARKET DATA CONFIGURATION
# ============================================================================
class MarketConfig:
    """Market data configuration."""
    # Indices
    MAJOR_INDICES = {
        'S&P 500': '^GSPC',
        'NASDAQ': '^IXIC',
        'Dow Jones': '^DJI',
        'NIFTY 50': '^NSEI',
        'SENSEX': '^BSESN',
    }
    
    # Commodities
    COMMODITIES = {
        'Gold': 'GC=F',
        'Silver': 'SI=F',
        'Crude Oil': 'CL=F',
        'Natural Gas': 'NG=F',
    }
    
    # Cryptocurrencies
    CRYPTOCURRENCIES = {
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD',
        'Ripple': 'XRP-USD',
        'Cardano': 'ADA-USD',
    }
    
    # Forex Pairs
    FOREX_PAIRS = {
        'EURUSD': 'EURUSD=X',
        'GBPUSD': 'GBPUSD=X',
        'JPYUSD': 'JPY=X',
        'AUDUSD': 'AUDUSD=X',
        'CADUSD': 'CADUSD=X',
        'CHFUSD': 'CHFUSD=X',
    }
    
    # VIX and Fear Indices
    VOLATILITY_INDICES = {
        'VIX': '^VIX',
        'USD Index': 'DXY=F',
    }
    
    # Timeframes
    TIMEFRAMES = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y']
    
    # Popular stocks for recommendation
    POPULAR_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX',
        'JPM', 'BAC', 'GS', 'IBM', 'INTC', 'AMD', 'CSCO'
    ]
    
    # Sectors
    SECTORS = [
        'Technology', 'Healthcare', 'Finance', 'Energy',
        'Consumer', 'Industrial', 'Materials', 'Real Estate', 'Utilities'
    ]

# ============================================================================
# TECHNICAL INDICATORS CONFIGURATION
# ============================================================================
class IndicatorsConfig:
    """Technical indicators configuration."""
    # RSI (Relative Strength Index)
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    # MACD (Moving Average Convergence Divergence)
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    # Moving Averages
    SMA_SHORT = 20
    SMA_LONG = 50
    EMA_PERIOD = 12
    
    # Bollinger Bands
    BB_PERIOD = 20
    BB_STD_DEV = 2
    
    # Volume
    VOLUME_PERIOD = 20

# ============================================================================
# AI RECOMMENDATION WEIGHTS
# ============================================================================
class RecommendationWeights:
    """AI recommendation calculation weights."""
    TECHNICAL_ANALYSIS = 0.40  # 40%
    NEWS_SENTIMENT = 0.25      # 25%
    FOREX_TREND = 0.15         # 15%
    MARKET_TREND = 0.10        # 10%
    VOLATILITY = 0.10          # 10%

# ============================================================================
# SENTIMENT THRESHOLDS
# ============================================================================
class SentimentThresholds:
    """Sentiment analysis thresholds."""
    POSITIVE = 0.5
    NEGATIVE = -0.5
    NEUTRAL_RANGE = (-0.5, 0.5)

# ============================================================================
# RECOMMENDATION RATINGS
# ============================================================================
RECOMMENDATION_RATINGS = {
    'Strong Buy': {'stars': 5, 'range': (0.85, 1.0)},
    'Buy': {'stars': 4, 'range': (0.65, 0.85)},
    'Hold': {'stars': 3, 'range': (0.35, 0.65)},
    'Sell': {'stars': 2, 'range': (0.15, 0.35)},
    'Strong Sell': {'stars': 1, 'range': (0.0, 0.15)},
}

# ============================================================================
# NEWS SOURCES
# ============================================================================
class NewsConfig:
    """News configuration."""
    SOURCES = ['bloomberg', 'reuters', 'cnbc', 'financial-times']
    CATEGORIES = ['business', 'finance', 'market']
    LANGUAGE = 'en'
    SORT_BY = 'publishedAt'  # Options: 'publishedAt', 'relevancy', 'popularity'
    PAGE_SIZE = 50

# ============================================================================
# RISK LEVELS
# ============================================================================
RISK_LEVELS = {
    'Low': {'range': (0.0, 0.3), 'color': 'green'},
    'Medium': {'range': (0.3, 0.6), 'color': 'orange'},
    'High': {'range': (0.6, 1.0), 'color': 'red'},
}

# ============================================================================
# STREAMLIT CONFIGURATION
# ============================================================================
STREAMLIT_CONFIG = {
    'theme': {
        'primaryColor': '#1f77b4',
        'backgroundColor': '#ffffff',
        'secondaryBackgroundColor': '#f0f2f6',
        'textColor': '#262730',
        'font': 'sans serif'
    },
    'client': {
        'showErrorDetails': False,
    },
    'logger': {
        'level': LOG_LEVEL,
    }
}

# ============================================================================
# CACHE KEYS
# ============================================================================
class CacheKeys:
    """Cache key constants."""
    MARKET_DATA = 'market_data_{ticker}'
    FOREX_DATA = 'forex_data_{pair}'
    NEWS_DATA = 'news_data_{query}'
    INDICATORS = 'indicators_{ticker}_{period}'
    RECOMMENDATION = 'recommendation_{ticker}'

logger = logging.getLogger(__name__)
