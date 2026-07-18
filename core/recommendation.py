"""
Stock recommendation module for AI Market Trend Analyzer.
Generates intelligent stock recommendations based on multiple factors.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime
from config import RecommendationWeights, RECOMMENDATION_RATINGS, RISK_LEVELS
from core.indicators import TechnicalIndicators, SignalGenerator

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Generate stock recommendations based on multiple factors.
    """
    
    def __init__(self):
        """Initialize recommendation engine."""
        self.weights = RecommendationWeights()
        self.ratings = RECOMMENDATION_RATINGS
        self.indicators = TechnicalIndicators()
    
    def generate_recommendation(
        self,
        ticker: str,
        technical_score: float,
        sentiment_score: float,
        forex_score: float,
        market_score: float,
        volatility_score: float
    ) -> Dict:
        """
        Generate comprehensive recommendation for a stock.
        
        Args:
            ticker: Stock ticker
            technical_score: Technical analysis score (0-1)
            sentiment_score: News sentiment score (0-1)
            forex_score: Forex strength score (0-1)
            market_score: Market trend score (0-1)
            volatility_score: Volatility score (0-1)
            
        Returns:
            Dictionary with recommendation details
        """
        try:
            # Calculate weighted confidence score
            confidence = (
                technical_score * self.weights.TECHNICAL_ANALYSIS +
                sentiment_score * self.weights.NEWS_SENTIMENT +
                forex_score * self.weights.FOREX_TREND +
                market_score * self.weights.MARKET_TREND +
                volatility_score * self.weights.VOLATILITY
            )
            
            # Ensure score is between 0 and 1
            confidence = max(0, min(1, confidence))
            
            # Determine rating
            rating = self._get_rating_from_score(confidence)
            
            # Calculate risk level
            risk_level = self._calculate_risk_level(volatility_score, technical_score)
            
            # Determine expected trend
            expected_trend = self._determine_trend(technical_score, sentiment_score)
            
            # Calculate potential upside (simplified)
            potential_upside = self._estimate_upside(technical_score, sentiment_score)
            
            return {
                'ticker': ticker,
                'confidence_score': confidence,
                'confidence_percentage': round(confidence * 100, 2),
                'rating': rating,
                'stars': self.ratings[rating]['stars'],
                'risk_level': risk_level,
                'expected_trend': expected_trend,
                'potential_upside': potential_upside,
                'technical_score': technical_score,
                'sentiment_score': sentiment_score,
                'forex_score': forex_score,
                'market_score': market_score,
                'volatility_score': volatility_score,
                'timestamp': datetime.now().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendation for {ticker}: {str(e)}")
            return None
    
    @staticmethod
    def _get_rating_from_score(score: float) -> str:
        """
        Convert score to rating.
        
        Args:
            score: Confidence score (0-1)
            
        Returns:
            Rating string
        """
        for rating, data in RECOMMENDATION_RATINGS.items():
            if data['range'][0] <= score < data['range'][1]:
                return rating
        return "Hold"
    
    @staticmethod
    def _calculate_risk_level(volatility: float, technical: float) -> str:
        """
        Calculate risk level based on volatility and technical indicators.
        
        Args:
            volatility: Volatility score
            technical: Technical analysis score
            
        Returns:
            Risk level string
        """
        # High volatility and weak technical = high risk
        risk_score = (volatility * 0.6) + ((1 - technical) * 0.4)
        
        for risk, data in RISK_LEVELS.items():
            if data['range'][0] <= risk_score < data['range'][1]:
                return risk
        return "Medium"
    
    @staticmethod
    def _determine_trend(technical: float, sentiment: float) -> str:
        """
        Determine expected trend.
        
        Args:
            technical: Technical score
            sentiment: Sentiment score
            
        Returns:
            Trend string (Bullish, Neutral, Bearish)
        """
        avg_score = (technical + sentiment) / 2
        
        if avg_score >= 0.65:
            return "Bullish"
        elif avg_score <= 0.35:
            return "Bearish"
        else:
            return "Neutral"
    
    @staticmethod
    def _estimate_upside(technical: float, sentiment: float) -> float:
        """
        Estimate potential upside percentage.
        
        Args:
            technical: Technical score
            sentiment: Sentiment score
            
        Returns:
            Estimated upside percentage
        """
        # Positive scores indicate potential for upside
        avg_score = (technical + sentiment) / 2
        
        # Estimate upside from 0% to 30%
        upside = avg_score * 30
        
        return round(upside, 2)
    
    def explain_recommendation(self, recommendation: Dict) -> str:
        """
        Generate explanation for recommendation.
        
        Args:
            recommendation: Recommendation dictionary
            
        Returns:
            Explanation string
        """
        ticker = recommendation['ticker']
        rating = recommendation['rating']
        confidence = recommendation['confidence_percentage']
        risk = recommendation['risk_level']
        trend = recommendation['expected_trend']
        
        explanation = f"""
        **{ticker} - {rating}**
        
        Confidence: {confidence}%
        Risk Level: {risk}
        Expected Trend: {trend}
        Potential Upside: {recommendation['potential_upside']}%
        
        Rationale:
        - Technical Analysis Score: {recommendation['technical_score']:.2f}/1.0
        - Sentiment Score: {recommendation['sentiment_score']:.2f}/1.0
        - Forex Impact: {recommendation['forex_score']:.2f}/1.0
        - Market Trend: {recommendation['market_score']:.2f}/1.0
        - Volatility: {recommendation['volatility_score']:.2f}/1.0
        """
        
        return explanation.strip()


class PortfolioAnalyzer:
    """
    Analyze and recommend portfolios.
    """
    
    def __init__(self, recommendation_engine: RecommendationEngine):
        """Initialize portfolio analyzer.
        
        Args:
            recommendation_engine: RecommendationEngine instance
        """
        self.engine = recommendation_engine
    
    def get_top_opportunities(self, recommendations: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Get top opportunity stocks.
        
        Args:
            recommendations: List of recommendation dictionaries
            top_n: Number of top stocks to return
            
        Returns:
            List of top opportunities sorted by confidence
        """
        try:
            # Sort by confidence score
            sorted_recs = sorted(
                recommendations,
                key=lambda x: x['confidence_score'],
                reverse=True
            )
            
            logger.info(f"Selected top {min(top_n, len(sorted_recs))} opportunities")
            return sorted_recs[:top_n]
            
        except Exception as e:
            logger.error(f"Error getting top opportunities: {str(e)}")
            return []
    
    def get_stocks_to_watch(self, recommendations: List[Dict], top_n: int = 20) -> List[Dict]:
        """
        Get stocks to watch (neutral positions).
        
        Args:
            recommendations: List of recommendation dictionaries
            top_n: Number of stocks to return
            
        Returns:
            List of stocks to watch
        """
        try:
            # Filter for "Hold" and "Sell" ratings
            watch_list = [
                r for r in recommendations
                if r['rating'] in ['Hold', 'Sell']
            ]
            
            # Sort by confidence
            watch_list.sort(
                key=lambda x: x['confidence_score'],
                reverse=True
            )
            
            logger.info(f"Selected {len(watch_list[:top_n])} stocks to watch")
            return watch_list[:top_n]
            
        except Exception as e:
            logger.error(f"Error getting stocks to watch: {str(e)}")
            return []
    
    def identify_high_risk_stocks(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Identify high-risk stocks to avoid.
        
        Args:
            recommendations: List of recommendation dictionaries
            
        Returns:
            List of high-risk stocks
        """
        try:
            # Filter for high-risk and sell ratings
            high_risk = [
                r for r in recommendations
                if r['risk_level'] == 'High' or r['rating'] in ['Strong Sell', 'Sell']
            ]
            
            # Sort by risk
            high_risk.sort(
                key=lambda x: x['volatility_score'],
                reverse=True
            )
            
            logger.info(f"Identified {len(high_risk)} high-risk stocks")
            return high_risk
            
        except Exception as e:
            logger.error(f"Error identifying high-risk stocks: {str(e)}")
            return []
    
    def calculate_portfolio_metrics(self, recommendations: List[Dict]) -> Dict:
        """
        Calculate overall portfolio metrics.
        
        Args:
            recommendations: List of recommendation dictionaries
            
        Returns:
            Dictionary with portfolio metrics
        """
        try:
            if not recommendations:
                return {}
            
            df = pd.DataFrame(recommendations)
            
            metrics = {
                'total_stocks': len(recommendations),
                'avg_confidence': df['confidence_score'].mean(),
                'bullish_count': len(df[df['expected_trend'] == 'Bullish']),
                'bearish_count': len(df[df['expected_trend'] == 'Bearish']),
                'neutral_count': len(df[df['expected_trend'] == 'Neutral']),
                'high_risk_count': len(df[df['risk_level'] == 'High']),
                'medium_risk_count': len(df[df['risk_level'] == 'Medium']),
                'low_risk_count': len(df[df['risk_level'] == 'Low']),
                'strong_buy_count': len(df[df['rating'] == 'Strong Buy']),
                'buy_count': len(df[df['rating'] == 'Buy']),
                'hold_count': len(df[df['rating'] == 'Hold']),
                'sell_count': len(df[df['rating'] == 'Sell']),
                'strong_sell_count': len(df[df['rating'] == 'Strong Sell']),
            }
            
            logger.info(f"Calculated portfolio metrics: {metrics['avg_confidence']:.2%} avg confidence")
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {str(e)}")
            return {}


logger.info("Recommendation module loaded successfully")
