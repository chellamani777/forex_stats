"""
Report export module for AI Market Trend Analyzer.
Generates and exports reports in PDF, CSV, and Excel formats.
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from io import BytesIO
import csv

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generate reports in multiple formats.
    """
    
    @staticmethod
    def generate_recommendation_csv(
        recommendations: List[Dict],
        filename: str = None
    ) -> Optional[BytesIO]:
        """
        Generate CSV report from recommendations.
        
        Args:
            recommendations: List of recommendation dictionaries
            filename: Output filename (optional)
            
        Returns:
            BytesIO object with CSV data or None if failed
        """
        try:
            logger.info("Generating recommendation CSV report")
            
            df = pd.DataFrame(recommendations)
            
            # Select relevant columns
            columns = [
                'ticker', 'rating', 'confidence_percentage', 'stars',
                'risk_level', 'expected_trend', 'potential_upside',
                'technical_score', 'sentiment_score', 'timestamp'
            ]
            
            df = df[columns]
            
            # Create BytesIO object
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)
            
            logger.info("Recommendation CSV report generated successfully")
            return output
            
        except Exception as e:
            logger.error(f"Error generating CSV report: {str(e)}")
            return None
    
    @staticmethod
    def generate_recommendation_excel(
        recommendations: List[Dict],
        filename: str = None
    ) -> Optional[BytesIO]:
        """
        Generate Excel report from recommendations.
        
        Args:
            recommendations: List of recommendation dictionaries
            filename: Output filename (optional)
            
        Returns:
            BytesIO object with Excel data or None if failed
        """
        try:
            logger.info("Generating recommendation Excel report")
            
            df = pd.DataFrame(recommendations)
            
            # Select relevant columns
            columns = [
                'ticker', 'rating', 'confidence_percentage', 'stars',
                'risk_level', 'expected_trend', 'potential_upside',
                'technical_score', 'sentiment_score', 'timestamp'
            ]
            
            df = df[columns]
            
            # Create BytesIO object
            output = BytesIO()
            
            # Write to Excel
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Recommendations', index=False)
                
                # Get worksheet
                worksheet = writer.sheets['Recommendations']
                
                # Adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            output.seek(0)
            logger.info("Recommendation Excel report generated successfully")
            return output
            
        except Exception as e:
            logger.error(f"Error generating Excel report: {str(e)}")
            return None
    
    @staticmethod
    def generate_news_csv(articles: pd.DataFrame) -> Optional[BytesIO]:
        """
        Generate CSV report from news articles.
        
        Args:
            articles: DataFrame with articles
            
        Returns:
            BytesIO object with CSV data or None if failed
        """
        try:
            logger.info("Generating news CSV report")
            
            # Select relevant columns
            if 'sentiment' in articles.columns:
                columns = ['title', 'source', 'sentiment', 'compound_score', 'published_at', 'url']
            else:
                columns = ['title', 'source', 'published_at', 'url']
            
            df = articles[columns].copy()
            
            # Create BytesIO object
            output = BytesIO()
            df.to_csv(output, index=False, encoding='utf-8')
            output.seek(0)
            
            logger.info("News CSV report generated successfully")
            return output
            
        except Exception as e:
            logger.error(f"Error generating news CSV report: {str(e)}")
            return None
    
    @staticmethod
    def generate_market_summary_text(
        summary_data: Dict,
        timestamp: datetime = None
    ) -> str:
        """
        Generate text summary of market analysis.
        
        Args:
            summary_data: Dictionary with summary data
            timestamp: Report timestamp
            
        Returns:
            Formatted text summary
        """
        try:
            if timestamp is None:
                timestamp = datetime.now()
            
            summary = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AI MARKET TREND ANALYZER - REPORT                         ║
║                         {timestamp.strftime('%Y-%m-%d %H:%M:%S')}                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 MARKET OVERVIEW
{'-' * 80}

Market Status: {summary_data.get('market_status', 'N/A')}
Overall Sentiment: {summary_data.get('overall_sentiment', 'N/A')}
VIX Level: {summary_data.get('vix_level', 'N/A')}


💹 TOP OPPORTUNITIES (Stocks to Buy)
{'-' * 80}
"""
            
            if 'top_buy' in summary_data and summary_data['top_buy']:
                for i, stock in enumerate(summary_data['top_buy'][:5], 1):
                    summary += f"""
{i}. {stock.get('ticker', 'N/A')} - Rating: {stock.get('rating', 'N/A')}
   Confidence: {stock.get('confidence_percentage', 0):.1f}%
   Risk: {stock.get('risk_level', 'N/A')} | Potential Upside: {stock.get('potential_upside', 0):.1f}%
"""
            else:
                summary += "No opportunities at this time.\n"
            
            summary += f"""

📌 STOCKS TO WATCH
{'-' * 80}
"""
            
            if 'watch_list' in summary_data and summary_data['watch_list']:
                for i, stock in enumerate(summary_data['watch_list'][:5], 1):
                    summary += f"""
{i}. {stock.get('ticker', 'N/A')} - Status: {stock.get('rating', 'N/A')}
   Confidence: {stock.get('confidence_percentage', 0):.1f}%
"""
            else:
                summary += "No stocks on watch list.\n"
            
            summary += f"""

⚠️  HIGH-RISK ALERTS
{'-' * 80}
"""
            
            if 'high_risk' in summary_data and summary_data['high_risk']:
                for i, stock in enumerate(summary_data['high_risk'][:5], 1):
                    summary += f"""
{i}. {stock.get('ticker', 'N/A')} - Risk: {stock.get('risk_level', 'N/A')}
   Avoid: {stock.get('rating', 'N/A')}
"""
            else:
                summary += "No high-risk alerts.\n"
            
            summary += f"""

📰 NEWS SENTIMENT
{'-' * 80}

Positive Articles: {summary_data.get('positive_news_count', 0)}
Negative Articles: {summary_data.get('negative_news_count', 0)}
Neutral Articles: {summary_data.get('neutral_news_count', 0)}

Overall News Sentiment: {summary_data.get('news_sentiment', 'N/A')}


💱 FOREX TRENDS
{'-' * 80}

{summary_data.get('forex_summary', 'No forex data available')}


📈 PORTFOLIO METRICS
{'-' * 80}

Total Stocks Analyzed: {summary_data.get('total_stocks', 0)}
Average Confidence: {summary_data.get('avg_confidence', 0):.2%}
Bullish Stocks: {summary_data.get('bullish_count', 0)}
Bearish Stocks: {summary_data.get('bearish_count', 0)}
Neutral Stocks: {summary_data.get('neutral_count', 0)}


📝 RECOMMENDATIONS
{'-' * 80}

{summary_data.get('recommendations', 'No specific recommendations at this time.')}


⚠️  RISK DISCLAIMERS
{'-' * 80}

This analysis is for informational purposes only and should not be considered
financial advice. Always conduct your own research and consult with a financial
advisor before making investment decisions.

Market conditions change rapidly. Recommendations are valid at the time of
generation and may become outdated.

{'-' * 80}
Report generated by AI Market Trend Analyzer v1.0
"""
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error generating summary text: {str(e)}")
            return ""


class PortfolioExporter:
    """
    Export portfolio data and analysis.
    """
    
    @staticmethod
    def export_portfolio(portfolio_data: Dict) -> Optional[BytesIO]:
        """
        Export complete portfolio analysis.
        
        Args:
            portfolio_data: Dictionary with portfolio data
            
        Returns:
            BytesIO object with exported data or None if failed
        """
        try:
            logger.info("Exporting portfolio data")
            
            output = BytesIO()
            
            # Create DataFrame from portfolio data
            if 'holdings' in portfolio_data:
                df = pd.DataFrame(portfolio_data['holdings'])
                df.to_csv(output, index=False, encoding='utf-8')
                output.seek(0)
                
                logger.info("Portfolio exported successfully")
                return output
            
            return None
            
        except Exception as e:
            logger.error(f"Error exporting portfolio: {str(e)}")
            return None


logger.info("Report export module loaded successfully")
