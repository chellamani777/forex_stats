"""
Main Streamlit Application for AI Market Trend Analyzer.
Entry point for the application.
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta
from config import AppConfig, MarketConfig, APIKeys
from core.market_data import MarketDataFetcher, MarketSentiment
from core.forex import ForexAnalyzer
from core.news import NewsAnalyzer
from core.indicators import TechnicalIndicators
from core.recommendation import RecommendationEngine, PortfolioAnalyzer
from core.ai_engine import AIEngine
from visualization.charts import ChartBuilder
from export.report import ReportGenerator
from utils import show_success_alert, show_error_alert, show_info_alert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Market Trend Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables."""
    if 'market_data' not in st.session_state:
        st.session_state.market_data = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []
    if 'news_analysis' not in st.session_state:
        st.session_state.news_analysis = None
    if 'forex_analysis' not in st.session_state:
        st.session_state.forex_analysis = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = None

initialize_session_state()

# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """Render application header."""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("📊 AI Market Trend Analyzer")
        st.caption("Real-time financial market analysis, forex trends, and AI-powered stock recommendations")
    
    with col2:
        st.metric(
            "Last Updated",
            datetime.now().strftime("%H:%M:%S"),
            "Today"
        )

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

def render_sidebar():
    """Render sidebar with filters and settings."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Status
        st.subheader("API Status")
        api_status = {}
        api_status['OpenAI'] = '✅' if APIKeys.OPENAI_API_KEY else '❌'
        api_status['Alpha Vantage'] = '✅' if APIKeys.ALPHA_VANTAGE_API_KEY else '❌'
        api_status['Finnhub'] = '✅' if APIKeys.FINNHUB_API_KEY else '❌'
        api_status['NewsAPI'] = '✅' if APIKeys.NEWS_API_KEY else '❌'
        
        for api, status in api_status.items():
            st.write(f"{status} {api}")
        
        st.divider()
        
        # Analysis Filters
        st.subheader("📊 Analysis Filters")
        
        timeframe = st.selectbox(
            "Timeframe",
            ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y'],
            index=3
        )
        
        country = st.selectbox(
            "Country",
            ['USA', 'India', 'UK', 'Canada', 'Australia', 'Japan']
        )
        
        sector = st.selectbox(
            "Sector",
            ['All'] + MarketConfig.SECTORS
        )
        
        risk_level = st.multiselect(
            "Risk Level",
            ['Low', 'Medium', 'High'],
            default=['Low', 'Medium']
        )
        
        st.divider()
        
        # Data Refresh
        st.subheader("🔄 Data Management")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.session_state.clear()
                initialize_session_state()
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        
        cache_enabled = st.checkbox(
            "Enable Caching",
            value=True,
            help="Cache data to reduce API calls"
        )
        
        theme = st.selectbox(
            "Theme",
            ['Light', 'Dark', 'Auto'],
            index=2
        )
        
        st.divider()
        
        # About
        st.subheader("ℹ️ About")
        st.info(
            """AI Market Trend Analyzer v1.0\n\n
            Powered by:\n
            • OpenAI GPT\n
            • Yahoo Finance\n
            • NewsAPI\n
            • Technical Analysis\n
            Built with ❤️ for traders
            """
        )
        
        return {
            'timeframe': timeframe,
            'country': country,
            'sector': sector,
            'risk_level': risk_level,
            'cache_enabled': cache_enabled,
            'theme': theme
        }

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def render_market_overview():
    """Render global market overview."""
    st.subheader("🌍 Global Market Overview")
    
    try:
        fetcher = MarketDataFetcher()
        
        # Major indices
        col1, col2, col3, col4 = st.columns(4)
        
        indices_data = {
            'S&P 500': '^GSPC',
            'NASDAQ': '^IXIC',
            'Dow Jones': '^DJI',
            'NIFTY 50': '^NSEI',
        }
        
        with col1:
            data = fetcher.get_index_data('^GSPC', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                previous = data['Close'].iloc[-5] if len(data) > 5 else data['Close'].iloc[0]
                change = ((current - previous) / previous) * 100
                st.metric(
                    "S&P 500",
                    f"{current:,.0f}",
                    f"{change:.2f}%",
                    delta_color="normal" if change >= 0 else "inverse"
                )
        
        with col2:
            data = fetcher.get_index_data('^IXIC', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                previous = data['Close'].iloc[-5] if len(data) > 5 else data['Close'].iloc[0]
                change = ((current - previous) / previous) * 100
                st.metric(
                    "NASDAQ",
                    f"{current:,.0f}",
                    f"{change:.2f}%",
                    delta_color="normal" if change >= 0 else "inverse"
                )
        
        with col3:
            data = fetcher.get_index_data('^DJI', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                previous = data['Close'].iloc[-5] if len(data) > 5 else data['Close'].iloc[0]
                change = ((current - previous) / previous) * 100
                st.metric(
                    "Dow Jones",
                    f"{current:,.0f}",
                    f"{change:.2f}%",
                    delta_color="normal" if change >= 0 else "inverse"
                )
        
        with col4:
            # VIX Index
            sentiment = MarketSentiment(fetcher)
            vix = sentiment.get_vix_level()
            if vix:
                st.metric(
                    "VIX Index",
                    f"{vix:.2f}",
                    sentiment.interpret_vix(vix),
                    delta_color="inverse" if vix > 20 else "normal"
                )
    
    except Exception as e:
        st.error(f"Error fetching market data: {str(e)}")
        logger.error(f"Error in market overview: {str(e)}")

# ============================================================================
# STOCK RECOMMENDATIONS
# ============================================================================

def render_recommendations():
    """Render stock recommendations section."""
    st.subheader("🎯 AI Stock Recommendations")
    
    try:
        # Fetch popular stocks
        fetcher = MarketDataFetcher()
        engine = RecommendationEngine()
        
        tickers = MarketConfig.POPULAR_STOCKS[:10]
        recommendations = []
        
        with st.spinner("Analyzing stocks..."):
            for ticker in tickers:
                try:
                    # Get data
                    data = fetcher.get_stock_data(ticker, period='3mo')
                    if data is None:
                        continue
                    
                    # Calculate indicators
                    close_prices = data['Close']
                    rsi = TechnicalIndicators.calculate_rsi(close_prices)
                    macd, signal, _ = TechnicalIndicators.calculate_macd(close_prices)
                    
                    # Generate scores (simplified)
                    technical_score = min(rsi.iloc[-1] / 100, 1.0)
                    sentiment_score = 0.6  # Placeholder
                    forex_score = 0.7  # Placeholder
                    market_score = 0.65  # Placeholder
                    volatility_score = 0.5  # Placeholder
                    
                    # Generate recommendation
                    rec = engine.generate_recommendation(
                        ticker,
                        technical_score,
                        sentiment_score,
                        forex_score,
                        market_score,
                        volatility_score
                    )
                    
                    if rec:
                        recommendations.append(rec)
                
                except Exception as e:
                    logger.warning(f"Error analyzing {ticker}: {str(e)}")
                    continue
        
        # Display recommendations
        if recommendations:
            st.session_state.recommendations = recommendations
            
            # Create DataFrame
            df = pd.DataFrame(recommendations)
            df = df[['ticker', 'rating', 'confidence_percentage', 'stars', 'risk_level', 'expected_trend']]
            df.columns = ['Ticker', 'Rating', 'Confidence %', 'Stars', 'Risk', 'Trend']
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Download options
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = ReportGenerator.generate_recommendation_csv(recommendations)
                if csv_data:
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv_data.getvalue(),
                        file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            with col2:
                excel_data = ReportGenerator.generate_recommendation_excel(recommendations)
                if excel_data:
                    st.download_button(
                        label="📥 Download as Excel",
                        data=excel_data.getvalue(),
                        file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        else:
            st.warning("No recommendations available at this time.")
    
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        logger.error(f"Error in recommendations: {str(e)}")

# ============================================================================
# NEWS SENTIMENT
# ============================================================================

def render_news_sentiment():
    """Render news sentiment section."""
    st.subheader("📰 Market News & Sentiment")
    
    try:
        analyzer = NewsAnalyzer()
        
        with st.spinner("Fetching and analyzing news..."):
            news_analysis = analyzer.analyze_market_news(query='stock market', limit=30)
        
        if news_analysis:
            overall = news_analysis['overall_sentiment']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Positive Articles",
                    overall['positive_count'],
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Negative Articles",
                    overall['negative_count'],
                    delta=None
                )
            
            with col3:
                st.metric(
                    "Neutral Articles",
                    overall['neutral_count'],
                    delta=None
                )
            
            with col4:
                sentiment_label = overall['overall_sentiment']
                st.metric(
                    "Overall Sentiment",
                    sentiment_label,
                    f"{overall['average_score']:.2f}"
                )
            
            # Top news
            st.write("**📌 Top News Today:**")
            for idx, article in news_analysis['top_news'].head(5).iterrows():
                with st.expander(f"📰 {article['title']}"):
                    st.write(f"**Source:** {article['source']}")
                    st.write(f"**Sentiment:** {article.get('sentiment', 'N/A')}")
                    st.write(f"**Description:** {article['description']}")
                    st.write(f"[Read Full Article]({article['url']})")
    
    except Exception as e:
        st.warning(f"Error fetching news: {str(e)}")
        logger.error(f"Error in news sentiment: {str(e)}")

# ============================================================================
# FOREX ANALYSIS
# ============================================================================

def render_forex_section():
    """Render forex analysis section."""
    st.subheader("💱 Forex Analysis")
    
    try:
        analyzer = ForexAnalyzer()
        
        with st.spinner("Analyzing forex pairs..."):
            forex_data = analyzer.analyze_all_forex_pairs(period='1mo')
        
        if forex_data:
            st.session_state.forex_analysis = forex_data
            
            # Create DataFrame
            df_list = []
            for pair_name, data in forex_data.items():
                df_list.append({
                    'Pair': pair_name,
                    'Current Price': data.get('current_price', 0),
                    'Trend': data.get('trend', 'N/A'),
                    'Strength': f"{data.get('trend_strength', 0):.1f}%",
                    'RSI': f"{data.get('rsi', 0):.1f}",
                    'Support': f"{data.get('support', 0):.4f}",
                    'Resistance': f"{data.get('resistance', 0):.4f}"
                })
            
            df = pd.DataFrame(df_list)
            st.dataframe(df, use_container_width=True)
    
    except Exception as e:
        st.warning(f"Error analyzing forex: {str(e)}")
        logger.error(f"Error in forex analysis: {str(e)}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application function."""
    render_header()
    
    # Sidebar
    filters = render_sidebar()
    
    st.divider()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard",
        "🎯 Recommendations",
        "📰 News",
        "💱 Forex",
        "🔍 Stock Finder",
        "🤖 AI Chat"
    ])
    
    with tab1:
        render_market_overview()
        st.divider()
        render_forex_section()
    
    with tab2:
        render_recommendations()
    
    with tab3:
        render_news_sentiment()
    
    with tab4:
        st.info("Detailed forex analysis coming soon...")
    
    with tab5:
        st.subheader("🔍 Stock Finder")
        ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, MSFT):")
        if ticker:
            try:
                fetcher = MarketDataFetcher()
                data = fetcher.get_stock_data(ticker.upper(), period='3mo')
                info = fetcher.get_stock_info(ticker.upper())
                
                if data is not None and info:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Current Price", f"${info.get('current_price', 0):.2f}")
                    with col2:
                        st.metric("Market Cap", f"${info.get('market_cap', 0) / 1e9:.2f}B")
                    with col3:
                        st.metric("P/E Ratio", f"{info.get('pe_ratio', 0):.2f}")
                    
                    # Price chart
                    st.subheader("Price Chart")
                    fig = ChartBuilder.create_candlestick_chart(data, f"{ticker.upper()} Price Chart")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error(f"Could not find data for {ticker}")
            
            except Exception as e:
                st.error(f"Error fetching stock data: {str(e)}")
    
    with tab6:
        st.subheader("🤖 AI Chat Assistant")
        st.info("Chat with our AI about markets, stocks, and forex trends.")
        
        # Chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.write(msg['content'])
        
        # User input
        user_input = st.chat_input("Ask me about markets...")
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Get AI response
            ai = AIEngine()
            response = ai.chat(user_input, st.session_state.chat_history[:-1])
            
            if response:
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                st.rerun()
    
    # Footer
    st.divider()
    st.caption(
        "🔐 Data Sources: Yahoo Finance, NewsAPI, Alpha Vantage | "
        "📊 Analysis: Technical & AI-Powered | "
        "⚠️ Disclaimer: For educational purposes only"
    )


if __name__ == "__main__":
    main()
