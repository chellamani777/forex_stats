"""
Visualization module for AI Market Trend Analyzer.
Creates interactive charts and visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ChartBuilder:
    """
    Build interactive charts using Plotly.
    """
    
    @staticmethod
    def create_candlestick_chart(data: pd.DataFrame, title: str = "Price Chart") -> Optional[go.Figure]:
        """
        Create candlestick chart.
        
        Args:
            data: DataFrame with OHLCV data
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
            )])
            
            fig.update_layout(
                title=title,
                yaxis_title='Price',
                template='plotly_white',
                xaxis_rangeslider_visible=False,
                height=500
            )
            
            logger.debug(f"Created candlestick chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating candlestick chart: {str(e)}")
            return None
    
    @staticmethod
    def create_price_chart(data: pd.DataFrame, title: str = "Price Chart") -> Optional[go.Figure]:
        """
        Create line chart for price.
        
        Args:
            data: DataFrame with price data
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#1f77b4', width=2)
            ))
            
            fig.update_layout(
                title=title,
                yaxis_title='Price',
                template='plotly_white',
                height=500
            )
            
            logger.debug(f"Created price chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating price chart: {str(e)}")
            return None
    
    @staticmethod
    def create_volume_chart(data: pd.DataFrame, title: str = "Volume Chart") -> Optional[go.Figure]:
        """
        Create volume chart.
        
        Args:
            data: DataFrame with volume data
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            colors = ['red' if data['Close'].iloc[i] < data['Close'].iloc[i-1] else 'green'
                      for i in range(1, len(data))]
            colors = ['gray'] + colors
            
            fig = go.Figure(data=[go.Bar(
                x=data.index,
                y=data['Volume'],
                marker_color=colors
            )])
            
            fig.update_layout(
                title=title,
                yaxis_title='Volume',
                template='plotly_white',
                height=400
            )
            
            logger.debug(f"Created volume chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating volume chart: {str(e)}")
            return None
    
    @staticmethod
    def create_rsi_chart(data: pd.DataFrame, rsi: pd.Series, title: str = "RSI Chart") -> Optional[go.Figure]:
        """
        Create RSI indicator chart.
        
        Args:
            data: DataFrame with price data
            rsi: Series with RSI values
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure()
            
            # RSI line
            fig.add_trace(go.Scatter(
                x=data.index,
                y=rsi,
                mode='lines',
                name='RSI',
                line=dict(color='#ff7f0e', width=2)
            ))
            
            # Overbought line
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
            
            # Oversold line
            fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
            
            fig.update_layout(
                title=title,
                yaxis_title='RSI',
                template='plotly_white',
                height=400
            )
            
            logger.debug(f"Created RSI chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating RSI chart: {str(e)}")
            return None
    
    @staticmethod
    def create_macd_chart(
        data: pd.DataFrame,
        macd: pd.Series,
        signal: pd.Series,
        histogram: pd.Series,
        title: str = "MACD Chart"
    ) -> Optional[go.Figure]:
        """
        Create MACD indicator chart.
        
        Args:
            data: DataFrame with price data
            macd: Series with MACD values
            signal: Series with signal line values
            histogram: Series with histogram values
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure()
            
            # Histogram
            colors = ['red' if h < 0 else 'green' for h in histogram]
            fig.add_trace(go.Bar(
                x=data.index,
                y=histogram,
                name='Histogram',
                marker_color=colors,
                opacity=0.3
            ))
            
            # MACD line
            fig.add_trace(go.Scatter(
                x=data.index,
                y=macd,
                mode='lines',
                name='MACD',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Signal line
            fig.add_trace(go.Scatter(
                x=data.index,
                y=signal,
                mode='lines',
                name='Signal',
                line=dict(color='#ff7f0e', width=2)
            ))
            
            fig.update_layout(
                title=title,
                yaxis_title='MACD',
                template='plotly_white',
                height=400
            )
            
            logger.debug(f"Created MACD chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating MACD chart: {str(e)}")
            return None
    
    @staticmethod
    def create_bollinger_bands_chart(
        data: pd.DataFrame,
        upper: pd.Series,
        middle: pd.Series,
        lower: pd.Series,
        title: str = "Bollinger Bands"
    ) -> Optional[go.Figure]:
        """
        Create Bollinger Bands chart.
        
        Args:
            data: DataFrame with price data
            upper: Series with upper band values
            middle: Series with middle band values
            lower: Series with lower band values
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure()
            
            # Price
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name='Close',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Upper band
            fig.add_trace(go.Scatter(
                x=data.index,
                y=upper,
                mode='lines',
                name='Upper Band',
                line=dict(color='rgba(0,0,0,0)'),
                showlegend=False
            ))
            
            # Lower band
            fig.add_trace(go.Scatter(
                x=data.index,
                y=lower,
                mode='lines',
                name='Lower Band',
                line=dict(color='rgba(0,0,0,0)'),
                fillcolor='rgba(128,128,128,0.2)',
                fill='tonexty'
            ))
            
            # Middle band
            fig.add_trace(go.Scatter(
                x=data.index,
                y=middle,
                mode='lines',
                name='Middle Band',
                line=dict(color='rgba(128,128,128,0.5)', dash='dash')
            ))
            
            fig.update_layout(
                title=title,
                yaxis_title='Price',
                template='plotly_white',
                height=500
            )
            
            logger.debug(f"Created Bollinger Bands chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating Bollinger Bands chart: {str(e)}")
            return None
    
    @staticmethod
    def create_correlation_heatmap(correlation_matrix: pd.DataFrame, title: str = "Correlation Matrix") -> Optional[go.Figure]:
        """
        Create correlation heatmap.
        
        Args:
            correlation_matrix: DataFrame with correlation values
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.index,
                colorscale='RdBu',
                zmid=0
            ))
            
            fig.update_layout(
                title=title,
                template='plotly_white',
                height=600
            )
            
            logger.debug(f"Created correlation heatmap: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating correlation heatmap: {str(e)}")
            return None
    
    @staticmethod
    def create_multi_line_chart(
        data: pd.DataFrame,
        columns: List[str],
        title: str = "Multi-Line Chart"
    ) -> Optional[go.Figure]:
        """
        Create multi-line chart.
        
        Args:
            data: DataFrame with data
            columns: List of column names to plot
            title: Chart title
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            fig = go.Figure()
            
            for column in columns:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data[column],
                    mode='lines',
                    name=column
                ))
            
            fig.update_layout(
                title=title,
                template='plotly_white',
                height=500
            )
            
            logger.debug(f"Created multi-line chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating multi-line chart: {str(e)}")
            return None
    
    @staticmethod
    def create_bar_chart(
        categories: List[str],
        values: List[float],
        title: str = "Bar Chart",
        color: str = '#1f77b4'
    ) -> Optional[go.Figure]:
        """
        Create bar chart.
        
        Args:
            categories: List of category names
            values: List of values
            title: Chart title
            color: Bar color
            
        Returns:
            Plotly figure or None if failed
        """
        try:
            # Color bars based on positive/negative
            colors = ['green' if v >= 0 else 'red' for v in values]
            
            fig = go.Figure(data=[go.Bar(
                x=categories,
                y=values,
                marker_color=colors
            )])
            
            fig.update_layout(
                title=title,
                template='plotly_white',
                height=400
            )
            
            logger.debug(f"Created bar chart: {title}")
            return fig
            
        except Exception as e:
            logger.error(f"Error creating bar chart: {str(e)}")
            return None


class StyleConfig:
    """
    UI styling configuration.
    """
    
    # Colors
    PRIMARY_COLOR = "#1f77b4"
    SUCCESS_COLOR = "#2ca02c"
    DANGER_COLOR = "#d62728"
    WARNING_COLOR = "#ff7f0e"
    INFO_COLOR = "#17becf"
    NEUTRAL_COLOR = "#7f7f7f"
    
    # Sentiment colors
    POSITIVE_COLOR = "#2ecc71"  # Green
    NEGATIVE_COLOR = "#e74c3c"  # Red
    NEUTRAL_COLOR_SENTIMENT = "#95a5a6"  # Gray
    
    # Chart template
    CHART_TEMPLATE = "plotly_white"
    
    # Font
    FONT_FAMILY = "Arial, sans-serif"
    FONT_SIZE = 12


logger.info("Visualization module loaded successfully")
