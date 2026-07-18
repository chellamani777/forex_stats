"""
Dashboard page module.
"""

import streamlit as st
import pandas as pd
from core.market_data import MarketDataFetcher, MarketSentiment
from visualization.charts import ChartBuilder

def show():
    """Render dashboard page."""
    st.title("📊 Market Dashboard")
    
    try:
        fetcher = MarketDataFetcher()
        sentiment = MarketSentiment(fetcher)
        
        # Global market status
        st.subheader("🌍 Global Market Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            data = fetcher.get_index_data('^GSPC', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[0]
                change = ((current - prev) / prev) * 100
                st.metric("S&P 500", f"{current:,.0f}", f"{change:.2f}%")
        
        with col2:
            data = fetcher.get_index_data('^IXIC', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[0]
                change = ((current - prev) / prev) * 100
                st.metric("NASDAQ", f"{current:,.0f}", f"{change:.2f}%")
        
        with col3:
            data = fetcher.get_index_data('^DJI', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[0]
                change = ((current - prev) / prev) * 100
                st.metric("Dow Jones", f"{current:,.0f}", f"{change:.2f}%")
        
        with col4:
            vix = sentiment.get_vix_level()
            if vix:
                st.metric("VIX", f"{vix:.2f}", sentiment.interpret_vix(vix))
        
        st.divider()
        
        # Commodities
        st.subheader("💎 Commodities")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data = fetcher.get_stock_data('GC=F', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[0]
                change = ((current - prev) / prev) * 100
                st.metric("Gold", f"${current:.2f}", f"{change:.2f}%")
        
        with col2:
            data = fetcher.get_stock_data('CL=F', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[0]
                change = ((current - prev) / prev) * 100
                st.metric("Crude Oil", f"${current:.2f}", f"{change:.2f}%")
        
        with col3:
            data = fetcher.get_stock_data('BTC-USD', period='1mo')
            if data is not None and len(data) > 1:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[0]
                change = ((current - prev) / prev) * 100
                st.metric("Bitcoin", f"${current:,.0f}", f"{change:.2f}%")
    
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
