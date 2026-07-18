"""
Utility functions for AI Market Trend Analyzer.
Common helper functions for data processing, caching, and formatting.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

# ============================================================================
# CACHING DECORATORS
# ============================================================================

def cache_data(ttl_seconds: int = 3600):
    """
    Cache function results with TTL (Time To Live).
    
    Args:
        ttl_seconds: Cache time to live in seconds
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a unique cache key
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            
            # Check if result is in cache and not expired
            if cache_key in st.session_state:
                cache_data = st.session_state[cache_key]
                if time.time() - cache_data['timestamp'] < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cache_data['value']
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            st.session_state[cache_key] = {
                'value': result,
                'timestamp': time.time()
            }
            logger.debug(f"Cached result for {func.__name__}")
            return result
        
        return wrapper
    return decorator


def retry_on_error(max_retries: int = 3, delay: int = 1):
    """
    Retry function on error with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay in seconds between retries
        
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Max retries exceeded for {func.__name__}: {str(e)}")
                        raise
                    wait_time = delay * (2 ** (retries - 1))
                    logger.warning(f"Retry {retries}/{max_retries} for {func.__name__} after {wait_time}s")
                    time.sleep(wait_time)
        return wrapper
    return decorator

# ============================================================================
# DATA FORMATTING
# ============================================================================

def format_currency(value: float, currency: str = 'USD') -> str:
    """
    Format value as currency string.
    
    Args:
        value: Numeric value to format
        currency: Currency code (default: USD)
        
    Returns:
        Formatted currency string
    """
    symbols = {'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}
    symbol = symbols.get(currency, currency)
    
    if abs(value) >= 1e9:
        return f"{symbol}{value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"{symbol}{value/1e6:.2f}M"
    elif abs(value) >= 1e3:
        return f"{symbol}{value/1e3:.2f}K"
    else:
        return f"{symbol}{value:.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format value as percentage string with color indicator.
    
    Args:
        value: Numeric value to format as percentage
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    sign = '+' if value >= 0 else ''
    return f"{sign}{value:.{decimals}f}%"


def get_trend_indicator(value: float) -> str:
    """
    Get emoji indicator for trend.
    
    Args:
        value: Numeric value to indicate trend
        
    Returns:
        Emoji indicator string
    """
    if value > 0.05:
        return "📈 Up"
    elif value < -0.05:
        return "📉 Down"
    else:
        return "➡️ Neutral"


def format_date(date_obj: datetime, format_str: str = '%Y-%m-%d') -> str:
    """
    Format datetime object to string.
    
    Args:
        date_obj: Datetime object to format
        format_str: Format string (default: YYYY-MM-DD)
        
    Returns:
        Formatted date string
    """
    return date_obj.strftime(format_str)

# ============================================================================
# DATA PROCESSING
# ============================================================================

def calculate_returns(prices: List[float]) -> List[float]:
    """
    Calculate percentage returns from price series.
    
    Args:
        prices: List of prices
        
    Returns:
        List of returns
    """
    if len(prices) < 2:
        return []
    
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] != 0:
            ret = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(ret)
    
    return returns


def calculate_volatility(returns: List[float], annualized: bool = True) -> float:
    """
    Calculate volatility from returns.
    
    Args:
        returns: List of returns
        annualized: Whether to annualize volatility (default: True)
        
    Returns:
        Volatility value
    """
    if not returns or len(returns) < 2:
        return 0.0
    
    volatility = np.std(returns)
    
    if annualized:
        volatility *= np.sqrt(252)  # 252 trading days per year
    
    return volatility


def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe ratio from returns.
    
    Args:
        returns: List of returns
        risk_free_rate: Annual risk-free rate (default: 0.02)
        
    Returns:
        Sharpe ratio value
    """
    if not returns or len(returns) < 2:
        return 0.0
    
    avg_return = np.mean(returns) * 252  # Annualized return
    volatility = calculate_volatility(returns, annualized=True)
    
    if volatility == 0:
        return 0.0
    
    return (avg_return - risk_free_rate) / volatility


def calculate_max_drawdown(prices: List[float]) -> float:
    """
    Calculate maximum drawdown from price series.
    
    Args:
        prices: List of prices
        
    Returns:
        Maximum drawdown as percentage
    """
    if not prices or len(prices) < 2:
        return 0.0
    
    cumulative = np.array(prices)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    
    return min(drawdown)

# ============================================================================
# VALIDATION
# ============================================================================

def is_valid_ticker(ticker: str) -> bool:
    """
    Validate stock ticker format.
    
    Args:
        ticker: Ticker symbol to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not ticker:
        return False
    
    # Check length and characters
    ticker = ticker.upper().strip()
    if len(ticker) < 1 or len(ticker) > 10:
        return False
    
    return ticker.isalnum()


def is_valid_date_range(start_date: datetime, end_date: datetime, max_days: int = 365) -> Tuple[bool, str]:
    """
    Validate date range.
    
    Args:
        start_date: Start date
        end_date: End date
        max_days: Maximum allowed days in range
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if start_date >= end_date:
        return False, "Start date must be before end date"
    
    days_diff = (end_date - start_date).days
    if days_diff > max_days:
        return False, f"Date range cannot exceed {max_days} days"
    
    return True, ""

# ============================================================================
# TIME UTILITIES
# ============================================================================

def get_market_hours() -> Tuple[datetime, datetime]:
    """
    Get current US market hours.
    
    Returns:
        Tuple of (market_open, market_close) for today
    """
    now = datetime.now()
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return market_open, market_close


def is_market_open() -> bool:
    """
    Check if US stock market is currently open.
    
    Returns:
        True if market is open, False otherwise
    """
    now = datetime.now()
    
    # Market closed on weekends
    if now.weekday() >= 5:
        return False
    
    market_open, market_close = get_market_hours()
    
    return market_open <= now <= market_close


def get_last_trading_day() -> datetime:
    """
    Get the last trading day (excluding weekends and holidays).
    
    Returns:
        Last trading day datetime
    """
    now = datetime.now()
    
    # Simple logic: if today is Monday, last trading day was Friday
    if now.weekday() == 0:
        return now - timedelta(days=3)
    elif now.weekday() == 6:
        return now - timedelta(days=2)
    else:
        return now - timedelta(days=1)

# ============================================================================
# UI HELPERS
# ============================================================================

def show_metric(label: str, value: Any, delta: Optional[float] = None, delta_color: str = 'normal'):
    """
    Display a metric in Streamlit with optional delta.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Change value (optional)
        delta_color: Color for delta ('normal', 'inverse', 'off')
    """
    if delta is not None:
        st.metric(label, value, delta=delta, delta_color=delta_color)
    else:
        st.metric(label, value)


def show_success_alert(message: str):
    """
    Show a success alert.
    
    Args:
        message: Alert message
    """
    st.success(f"✅ {message}")


def show_error_alert(message: str):
    """
    Show an error alert.
    
    Args:
        message: Alert message
    """
    st.error(f"❌ {message}")


def show_warning_alert(message: str):
    """
    Show a warning alert.
    
    Args:
        message: Alert message
    """
    st.warning(f"⚠️ {message}")


def show_info_alert(message: str):
    """
    Show an info alert.
    
    Args:
        message: Alert message
    """
    st.info(f"ℹ️ {message}")

logger.info("Utilities module loaded successfully")
