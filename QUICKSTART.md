# Quick Start Guide

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/chellamani777/forex_stats.git
cd forex_stats
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
FINNHUB_API_KEY=your_finnhub_key
NEWS_API_KEY=your_newsapi_key
FRED_API_KEY=your_fred_key
```

### 5. Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## API Keys Setup

### OpenAI API
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to `.env` file

### Alpha Vantage
1. Visit https://www.alphavantage.co/api/
2. Get your free API key
3. Add to `.env` file

### Finnhub
1. Go to https://finnhub.io/register
2. Sign up for free account
3. Copy API key to `.env` file

### NewsAPI
1. Visit https://newsapi.org/
2. Sign up for free account
3. Copy API key to `.env` file

### FRED (Federal Reserve Economic Data)
1. Go to https://fred.stlouisfed.org/docs/api/
2. Get API key
3. Add to `.env` file

## Features Overview

### 🎯 Dashboard
- Real-time market indices (S&P 500, NASDAQ, Dow Jones)
- Global market status and sentiment
- VIX fear index tracking
- Commodity prices (Gold, Oil, Bitcoin)

### 💼 Stock Recommendations
- AI-powered stock analysis
- Technical indicator-based scoring
- Risk assessment
- Buy/Sell/Hold ratings
- Confidence scores
- CSV/Excel export

### 📰 News & Sentiment
- Real-time financial news collection
- Sentiment analysis (Positive/Negative/Neutral)
- Market-moving news identification
- Sentiment-based trend prediction

### 💱 Forex Analysis
- Major currency pair analysis (EUR/USD, GBP/USD, etc.)
- Trend detection and strength calculation
- Support/Resistance levels
- Volume analysis
- Correlation matrix

### 🤖 AI Engine
- GPT-powered market analysis
- Investment summaries
- Risk assessments
- Natural language Q&A about markets

### 📊 Technical Analysis
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Moving Averages (SMA, EMA)
- ATR (Average True Range)
- Stochastic Oscillator

### 📈 Visualizations
- Interactive candlestick charts
- Volume analysis charts
- Technical indicator plots
- Correlation heatmaps
- Multi-line charts

### 📥 Export Options
- CSV export
- Excel export with formatting
- PDF reports
- Daily summaries

## Module Structure

### Core Modules
- **market_data.py**: Yahoo Finance integration
- **indicators.py**: Technical analysis calculations
- **forex.py**: Forex pair analysis
- **news.py**: News collection and sentiment analysis
- **ai_engine.py**: OpenAI GPT integration
- **recommendation.py**: Stock recommendation engine

### Visualization
- **charts.py**: Interactive chart generation

### Export
- **report.py**: Report generation and export

### Configuration
- **config.py**: All configuration constants
- **utils.py**: Helper utilities

## Usage Examples

### Basic Stock Analysis
```python
from core.market_data import MarketDataFetcher
from core.indicators import TechnicalIndicators

fetcher = MarketDataFetcher()
data = fetcher.get_stock_data('AAPL', period='1y')

indicators = TechnicalIndicators()
rsi = indicators.calculate_rsi(data['Close'])
macd, signal, hist = indicators.calculate_macd(data['Close'])
```

### Generate Stock Recommendation
```python
from core.recommendation import RecommendationEngine

engine = RecommendationEngine()
rec = engine.generate_recommendation(
    ticker='AAPL',
    technical_score=0.75,
    sentiment_score=0.65,
    forex_score=0.70,
    market_score=0.68,
    volatility_score=0.45
)
print(engine.explain_recommendation(rec))
```

### Analyze News Sentiment
```python
from core.news import NewsAnalyzer

analyzer = NewsAnalyzer()
analysis = analyzer.analyze_market_news(
    query='stock market',
    limit=50
)
print(analysis['overall_sentiment'])
```

## Troubleshooting

### API Key Issues
- Ensure `.env` file is in the project root
- Check API key validity
- Verify API rate limits

### Data Fetching Issues
- Check internet connection
- Verify API availability
- Check firewall/proxy settings

### Performance Issues
- Enable caching in settings
- Reduce number of stocks analyzed
- Use shorter timeframes

## Performance Tips

1. **Use Caching**: Enable data caching to reduce API calls
2. **Batch Analysis**: Analyze multiple stocks together
3. **Optimize Timeframes**: Use shorter periods for faster results
4. **API Rate Limits**: Respect API rate limits, add delays between requests

## Security Notes

- Never commit `.env` file to repository
- Keep API keys confidential
- Use environment variables for deployment
- Rotate API keys periodically
- Use API key restrictions when available

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black .
flake8 .
```

### Building Documentation
```bash
sphinx-build -b html docs/ docs/_build/
```

## Deployment

### Streamlit Cloud
```bash
streamlit login
streamlit deploy
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Docker Run
```bash
docker build -t ai-market-analyzer .
docker run -p 8501:8501 ai-market-analyzer
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/chellamani777/forex_stats/issues
- Email: support@example.com

## Disclaimer

⚠️ This tool is for educational and informational purposes only. It should not be considered financial advice. Always conduct your own research and consult with a financial advisor before making investment decisions.

Market analysis and recommendations are based on historical data and technical indicators. Past performance does not guarantee future results. Trade at your own risk.

---

**Built with ❤️ for traders and investors**
