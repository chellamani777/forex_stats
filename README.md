# AI Market Trend Analyzer

A production-ready Streamlit application for real-time financial market analysis, forex trends, stock recommendations, and AI-powered investment insights.

## Features

- 📊 Global Market Dashboard with real-time data
- 💱 Comprehensive Forex Analysis with technical indicators
- 📰 AI-powered News Sentiment Analysis
- 🎯 Intelligent Stock Recommendation Engine
- ⚠️ High-Risk Stock Identification
- 📈 Interactive Technical Charts
- 🤖 AI Investment Summary & Insights
- 🔔 Real-time Alerts & Notifications
- 📥 Export Reports (PDF, CSV, Excel)

## Installation

```bash
# Clone the repository
git clone https://github.com/chellamani777/forex_stats.git
cd forex_stats

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with API keys
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Create a `.env` file with the following API keys:

```
OPENAI_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
FRED_API_KEY=your_key_here
```

## Running the Application

```bash
streamlit run app.py
```

## Project Structure

```
forex_stats/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── config.py             # Configuration and settings
├── utils.py              # Utility functions
│
├── core/
│   ├── ai_engine.py      # AI/GPT integration
│   ├── market_data.py    # Market data fetching
│   ├── forex.py          # Forex analysis
│   ├── news.py           # News collection & sentiment
│   ├── indicators.py     # Technical indicators
│   └── recommendation.py # Stock recommendation logic
│
├── pages/
│   ├── dashboard.py      # Main dashboard
│   ├── forex_analysis.py # Forex trends
│   ├── news_analyzer.py  # News & sentiment
│   ├── stock_finder.py   # Stock search & details
│   ├── alerts.py         # Alerts & monitoring
│   └── portfolio.py      # Portfolio tracker
│
├── visualization/
│   ├── charts.py         # Interactive charts
│   └── styles.py         # UI styling
│
├── export/
│   └── report.py         # Report generation (PDF/CSV/Excel)
│
└── assets/
    └── images/           # Logos, icons, etc.
```

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.9+
- **Data Sources**: Yahoo Finance, Alpha Vantage, Finnhub, NewsAPI, FRED
- **AI**: OpenAI GPT, LangChain
- **Visualization**: Plotly, Altair
- **Data Processing**: Pandas, NumPy

## License

MIT License

---

**Built with ❤️ for traders and investors**