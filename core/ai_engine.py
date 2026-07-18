"""
AI engine module for AI Market Trend Analyzer.
Integrates OpenAI GPT for intelligent market analysis and recommendations.
"""

import openai
import logging
from typing import Dict, List, Optional
from datetime import datetime
from config import APIKeys, AppConfig
from utils import retry_on_error, cache_data

logger = logging.getLogger(__name__)


class AIEngine:
    """
    AI-powered market analysis using OpenAI GPT.
    """
    
    def __init__(self):
        """Initialize AI engine."""
        self.api_key = APIKeys.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 2000
        self.temperature = 0.7
    
    def validate_api_key(self) -> bool:
        """
        Validate OpenAI API key.
        
        Returns:
            True if valid, False otherwise
        """
        if not self.api_key:
            logger.error("OpenAI API key not configured")
            return False
        return True
    
    @retry_on_error(max_retries=2)
    def generate_market_summary(self, market_data: Dict) -> Optional[str]:
        """
        Generate AI-powered market summary.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Generated summary string or None if failed
        """
        if not self.validate_api_key():
            return None
        
        try:
            logger.info("Generating market summary with AI")
            
            prompt = f"""
            Based on the following market data, provide a comprehensive market summary:
            
            Market Data:
            {str(market_data)}
            
            Please provide:
            1. Overall market sentiment
            2. Key trends observed
            3. Potential risks
            4. Investment recommendations
            5. Outlook for next 24 hours
            
            Keep the response concise and actionable.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            summary = response['choices'][0]['message']['content']
            logger.info("Market summary generated successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating market summary: {str(e)}")
            return None
    
    @retry_on_error(max_retries=2)
    def analyze_stock(self, ticker: str, analysis_data: Dict) -> Optional[str]:
        """
        Generate AI analysis for a specific stock.
        
        Args:
            ticker: Stock ticker symbol
            analysis_data: Dictionary with technical and fundamental data
            
        Returns:
            Generated analysis string or None if failed
        """
        if not self.validate_api_key():
            return None
        
        try:
            logger.info(f"Analyzing {ticker} with AI")
            
            prompt = f"""
            Analyze the following stock data for {ticker}:
            
            Analysis Data:
            {str(analysis_data)}
            
            Please provide:
            1. Technical analysis interpretation
            2. Risk assessment
            3. Price target suggestion
            4. Entry/exit points
            5. Confidence level (0-100%)
            
            Be specific and data-driven in your analysis.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            analysis = response['choices'][0]['message']['content']
            logger.info(f"Stock analysis for {ticker} generated successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing stock {ticker}: {str(e)}")
            return None
    
    @retry_on_error(max_retries=2)
    def generate_investment_summary(self, summary_data: Dict) -> Optional[str]:
        """
        Generate daily investment summary and recommendations.
        
        Args:
            summary_data: Dictionary with all summary data
            
        Returns:
            Generated summary string or None if failed
        """
        if not self.validate_api_key():
            return None
        
        try:
            logger.info("Generating investment summary")
            
            prompt = f"""
            Create a comprehensive daily investment summary based on:
            
            Data:
            {str(summary_data)}
            
            Include:
            1. Daily Market Summary
            2. Top Opportunities (Stocks to Buy)
            3. Stocks to Watch
            4. High-Risk Warnings
            5. Market Sentiment Assessment
            6. Sector Performance
            7. Economic Impact
            8. Action Items for Today
            
            Format as a professional investment report.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            summary = response['choices'][0]['message']['content']
            logger.info("Investment summary generated successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating investment summary: {str(e)}")
            return None
    
    @retry_on_error(max_retries=2)
    def analyze_news_sentiment(self, news_data: Dict) -> Optional[str]:
        """
        Analyze news sentiment and its market impact.
        
        Args:
            news_data: Dictionary with news articles and sentiments
            
        Returns:
            Generated analysis string or None if failed
        """
        if not self.validate_api_key():
            return None
        
        try:
            logger.info("Analyzing news sentiment impact")
            
            prompt = f"""
            Analyze the following news and sentiment data for market impact:
            
            News Data:
            {str(news_data)}
            
            Provide:
            1. Overall Market Sentiment
            2. Sectors Most Affected
            3. Key News Drivers
            4. Potential Market Reactions
            5. Investment Implications
            
            Be concise and focus on actionable insights.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            analysis = response['choices'][0]['message']['content']
            logger.info("News sentiment analysis generated successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing news sentiment: {str(e)}")
            return None
    
    @retry_on_error(max_retries=2)
    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> Optional[str]:
        """
        Chat with AI assistant about markets.
        
        Args:
            user_message: User's question/message
            conversation_history: Previous conversation messages
            
        Returns:
            AI response string or None if failed
        """
        if not self.validate_api_key():
            return None
        
        try:
            logger.info("Processing user message")
            
            # Build message history
            messages = []
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": user_message})
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            assistant_message = response['choices'][0]['message']['content']
            logger.info("Chat response generated successfully")
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return None


class AIPromptBuilder:
    """
    Build structured prompts for AI analysis.
    """
    
    @staticmethod
    def build_stock_analysis_prompt(ticker: str, metrics: Dict) -> str:
        """
        Build a structured prompt for stock analysis.
        
        Args:
            ticker: Stock ticker
            metrics: Technical and fundamental metrics
            
        Returns:
            Formatted prompt string
        """
        return f"""
        Analyze {ticker} based on these metrics:
        - Current Price: {metrics.get('current_price', 'N/A')}
        - 52-week High: {metrics.get('high_52w', 'N/A')}
        - 52-week Low: {metrics.get('low_52w', 'N/A')}
        - P/E Ratio: {metrics.get('pe_ratio', 'N/A')}
        - RSI: {metrics.get('rsi', 'N/A')}
        - MACD Signal: {metrics.get('macd_signal', 'N/A')}
        - Market Sentiment: {metrics.get('sentiment', 'N/A')}
        
        Provide a concise recommendation with confidence score.
        """
    
    @staticmethod
    def build_risk_assessment_prompt(stocks: List[Dict]) -> str:
        """
        Build prompt for risk assessment.
        
        Args:
            stocks: List of stock data
            
        Returns:
            Formatted prompt string
        """
        stocks_info = "\n".join([
            f"- {s['ticker']}: Volatility={s.get('volatility', 'N/A')}, PE={s.get('pe', 'N/A')}"
            for s in stocks
        ])
        
        return f"""
        Assess risk levels for these stocks:
        {stocks_info}
        
        Rate each as Low/Medium/High risk with justification.
        """


logger.info("AI engine module loaded successfully")
