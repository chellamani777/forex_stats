"""
News and sentiment analysis module for AI Market Trend Analyzer.
Fetches news and analyzes sentiment.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import NewsConfig, APIKeys, SentimentThresholds
from utils import retry_on_error, cache_data

logger = logging.getLogger(__name__)


class NewsCollector:
    """
    Collect news from multiple sources.
    """
    
    def __init__(self):
        """Initialize news collector."""
        self.api_key = APIKeys.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2"
        self.config = NewsConfig()
        self.timeout = 30
    
    @retry_on_error(max_retries=3)
    @cache_data(ttl_seconds=3600)
    def get_top_headlines(self, query: str = 'finance', limit: int = 50) -> Optional[List[Dict]]:
        """
        Fetch top financial news headlines.
        
        Args:
            query: Search query (default: 'finance')
            limit: Number of articles (default: 50)
            
        Returns:
            List of article dictionaries or None if failed
        """
        try:
            logger.info(f"Fetching headlines for query: {query}")
            
            params = {
                'q': query,
                'apiKey': self.api_key,
                'pageSize': limit,
                'sortBy': self.config.SORT_BY,
                'language': self.config.LANGUAGE,
            }
            
            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            logger.info(f"Retrieved {len(articles)} articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching headlines: {str(e)}")
            return None
    
    @retry_on_error(max_retries=3)
    @cache_data(ttl_seconds=1800)
    def get_stock_news(self, ticker: str, limit: int = 30) -> Optional[List[Dict]]:
        """
        Fetch news specific to a stock ticker.
        
        Args:
            ticker: Stock ticker symbol
            limit: Number of articles (default: 30)
            
        Returns:
            List of article dictionaries or None if failed
        """
        try:
            logger.info(f"Fetching news for {ticker}")
            
            return self.get_top_headlines(query=ticker, limit=limit)
            
        except Exception as e:
            logger.error(f"Error fetching stock news for {ticker}: {str(e)}")
            return None
    
    def format_articles(self, articles: List[Dict]) -> pd.DataFrame:
        """
        Format articles into DataFrame.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            DataFrame with formatted articles
        """
        if not articles:
            return pd.DataFrame()
        
        try:
            df = pd.DataFrame([
                {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'published_at': article.get('publishedAt', ''),
                    'url': article.get('url', ''),
                    'image': article.get('urlToImage', ''),
                }
                for article in articles
            ])
            
            # Parse datetime
            df['published_at'] = pd.to_datetime(df['published_at'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error formatting articles: {str(e)}")
            return pd.DataFrame()


class SentimentAnalyzer:
    """
    Analyze sentiment from news articles and text.
    """
    
    def __init__(self):
        """Initialize sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()
        self.thresholds = SentimentThresholds()
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores
        """
        try:
            if not text:
                return {'positive': 0, 'negative': 0, 'neutral': 1, 'compound': 0}
            
            scores = self.analyzer.polarity_scores(text)
            
            return {
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu'],
                'compound': scores['compound'],
            }
            
        except Exception as e:
            logger.error(f"Error analyzing text sentiment: {str(e)}")
            return {'positive': 0, 'negative': 0, 'neutral': 1, 'compound': 0}
    
    def categorize_sentiment(self, compound_score: float) -> str:
        """
        Categorize sentiment based on compound score.
        
        Args:
            compound_score: Compound sentiment score (-1 to 1)
            
        Returns:
            Sentiment category
        """
        if compound_score >= self.thresholds.POSITIVE:
            return "Positive"
        elif compound_score <= self.thresholds.NEGATIVE:
            return "Negative"
        else:
            return "Neutral"
    
    def analyze_articles(self, articles: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze sentiment for multiple articles.
        
        Args:
            articles: DataFrame of articles
            
        Returns:
            DataFrame with added sentiment columns
        """
        try:
            if articles.empty:
                return articles
            
            # Combine title and description for analysis
            articles['text'] = articles['title'].fillna('') + ' ' + articles['description'].fillna('')
            
            # Analyze each article
            sentiments = articles['text'].apply(lambda x: self.analyze_text(x))
            
            # Extract sentiment components
            articles['positive_score'] = sentiments.apply(lambda x: x['positive'])
            articles['negative_score'] = sentiments.apply(lambda x: x['negative'])
            articles['neutral_score'] = sentiments.apply(lambda x: x['neutral'])
            articles['compound_score'] = sentiments.apply(lambda x: x['compound'])
            articles['sentiment'] = articles['compound_score'].apply(self.categorize_sentiment)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error analyzing articles sentiment: {str(e)}")
            return articles
    
    def calculate_overall_sentiment(self, sentiments: List[Dict]) -> Dict:
        """
        Calculate overall sentiment from multiple articles.
        
        Args:
            sentiments: List of sentiment dictionaries
            
        Returns:
            Dictionary with overall sentiment metrics
        """
        if not sentiments:
            return {
                'average_score': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'overall_sentiment': 'Neutral',
            }
        
        try:
            scores = [s['compound'] for s in sentiments]
            positive_count = sum(1 for s in sentiments if s['compound'] > self.thresholds.POSITIVE)
            negative_count = sum(1 for s in sentiments if s['compound'] < self.thresholds.NEGATIVE)
            neutral_count = len(sentiments) - positive_count - negative_count
            
            avg_score = np.mean(scores)
            
            return {
                'average_score': avg_score,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'total_articles': len(sentiments),
                'overall_sentiment': self.categorize_sentiment(avg_score),
            }
            
        except Exception as e:
            logger.error(f"Error calculating overall sentiment: {str(e)}")
            return {'average_score': 0, 'overall_sentiment': 'Unknown'}


class NewsAnalyzer:
    """
    Combined news collection and sentiment analysis.
    """
    
    def __init__(self):
        """Initialize news analyzer."""
        self.collector = NewsCollector()
        self.sentiment = SentimentAnalyzer()
    
    def analyze_market_news(self, query: str = 'stock market', limit: int = 50) -> Optional[Dict]:
        """
        Analyze market news and sentiment.
        
        Args:
            query: Search query (default: 'stock market')
            limit: Number of articles (default: 50)
            
        Returns:
            Dictionary with analyzed news or None if failed
        """
        try:
            logger.info(f"Analyzing market news for query: {query}")
            
            # Fetch articles
            articles = self.collector.get_top_headlines(query=query, limit=limit)
            if not articles:
                return None
            
            # Format to DataFrame
            df = self.collector.format_articles(articles)
            
            # Analyze sentiment
            df = self.sentiment.analyze_articles(df)
            
            # Calculate overall sentiment
            sentiments = df[['positive_score', 'negative_score', 'neutral_score', 'compound_score']].to_dict('records')
            sentiments = [{'compound': s['compound_score']} for s in sentiments]
            overall = self.sentiment.calculate_overall_sentiment(sentiments)
            
            # Separate by sentiment
            positive_news = df[df['sentiment'] == 'Positive'].sort_values('published_at', ascending=False)
            negative_news = df[df['sentiment'] == 'Negative'].sort_values('published_at', ascending=False)
            neutral_news = df[df['sentiment'] == 'Neutral'].sort_values('published_at', ascending=False)
            
            return {
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'overall_sentiment': overall,
                'all_articles': df,
                'positive_articles': positive_news,
                'negative_articles': negative_news,
                'neutral_articles': neutral_news,
                'top_news': df.sort_values('published_at', ascending=False).head(10),
            }
            
        except Exception as e:
            logger.error(f"Error analyzing market news: {str(e)}")
            return None


logger.info("News and sentiment analysis module loaded successfully")
