"""
Core modules package.
"""

from .market_data import MarketDataFetcher, MarketSentiment
from .indicators import TechnicalIndicators, SignalGenerator
from .forex import ForexAnalyzer, ForexCorrelation
from .news import NewsCollector, SentimentAnalyzer, NewsAnalyzer
from .ai_engine import AIEngine, AIPromptBuilder
from .recommendation import RecommendationEngine, PortfolioAnalyzer

__all__ = [
    'MarketDataFetcher',
    'MarketSentiment',
    'TechnicalIndicators',
    'SignalGenerator',
    'ForexAnalyzer',
    'ForexCorrelation',
    'NewsCollector',
    'SentimentAnalyzer',
    'NewsAnalyzer',
    'AIEngine',
    'AIPromptBuilder',
    'RecommendationEngine',
    'PortfolioAnalyzer',
]
