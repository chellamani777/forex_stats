"""
Alerts and monitoring page module.
"""

import streamlit as st
import pandas as pd

def show():
    """Render alerts page."""
    st.title("🔔 Alerts & Monitoring")
    
    # Alert configuration
    st.subheader("Configure Alerts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Price Alerts**")
        ticker = st.text_input("Stock Ticker")
        alert_type = st.selectbox("Alert Type", ['Price Above', 'Price Below', 'Percentage Change'])
        alert_value = st.number_input("Alert Value")
        
        if st.button("Set Alert"):
            st.success(f"Alert set for {ticker}")
    
    with col2:
        st.write("**Technical Alerts**")
        tech_alert = st.selectbox(
            "Technical Indicator",
            ['RSI > 70', 'RSI < 30', 'MACD Crossover', 'Volume Spike']
        )
        if st.button("Enable Alert"):
            st.success(f"Technical alert enabled: {tech_alert}")
    
    st.divider()
    
    # Active alerts
    st.subheader("Active Alerts")
    
    alerts = [
        {'ticker': 'AAPL', 'type': 'Price Above $150', 'status': '✅ Active'},
        {'ticker': 'MSFT', 'type': 'RSI > 70', 'status': '✅ Active'},
        {'ticker': 'GOOGL', 'type': 'MACD Crossover', 'status': '⏳ Triggered'},
    ]
    
    df = pd.DataFrame(alerts)
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # Notification settings
    st.subheader("Notification Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Email Notifications", value=True)
        st.checkbox("Push Notifications", value=True)
    
    with col2:
        st.checkbox("Telegram Alerts", value=False)
        st.checkbox("SMS Alerts", value=False)
