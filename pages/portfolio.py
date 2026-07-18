"""
Portfolio tracking page module.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    """Render portfolio page."""
    st.title("💼 Portfolio Tracker")
    
    # Create sample portfolio
    portfolio = st.session_state.get('portfolio', [])
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Your Holdings")
    
    with col2:
        if st.button("➕ Add Stock", use_container_width=True):
            st.session_state.show_add_stock = True
    
    # Add stock form
    if st.session_state.get('show_add_stock', False):
        with st.expander("Add New Stock", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ticker = st.text_input("Ticker")
            with col2:
                shares = st.number_input("Shares", min_value=0.1, value=1.0)
            with col3:
                entry_price = st.number_input("Entry Price", min_value=0.0, value=0.0)
            
            if st.button("Add to Portfolio"):
                portfolio.append({
                    'ticker': ticker,
                    'shares': shares,
                    'entry_price': entry_price,
                    'date_added': datetime.now().isoformat()
                })
                st.session_state.portfolio = portfolio
                st.success(f"Added {shares} shares of {ticker}")
                st.session_state.show_add_stock = False
                st.rerun()
    
    # Display portfolio
    if portfolio:
        df = pd.DataFrame(portfolio)
        st.dataframe(df, use_container_width=True)
        
        # Portfolio metrics
        st.subheader("Portfolio Metrics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Holdings", len(portfolio))
        with col2:
            total_invested = sum([p['shares'] * p['entry_price'] for p in portfolio])
            st.metric("Total Invested", f"${total_invested:,.2f}")
        with col3:
            st.metric("Portfolio Value", "$0.00")
    else:
        st.info("No holdings yet. Add your first stock!")
