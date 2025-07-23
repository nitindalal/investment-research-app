# Investment Research Platform

A comprehensive web application for analyzing companies and making informed investment decisions. This platform provides detailed financial analysis, competitive positioning, market sentiment, and valuation insights.

## Features

### 🔍 Company Analysis
- **Revenue Sources**: Identify and analyze primary revenue streams
- **Cost Drivers**: Understand cost structure and key expense factors
- **Projected Revenues**: Historical growth analysis and future projections
- **Market Share**: Competitive positioning and market dominance
- **Competition**: Comprehensive competitive landscape analysis
- **Economic Moat**: Evaluate sustainable competitive advantages
- **Public Sentiment**: News and social media sentiment analysis
- **Competitive Advantage**: SWOT analysis and strategic positioning
- **Leadership**: Executive team and governance analysis
- **Industry Position**: Sector analysis and industry trends

### 💰 Valuation Analysis
- **Discounted Cash Flow (DCF)**: Intrinsic value calculation
- **Peer Comparison**: Relative valuation metrics
- **Multiple Valuation Methods**: P/E, P/B, EV/EBITDA ratios
- **Sensitivity Analysis**: Scenario-based valuation ranges
- **Fair Value Range**: Comprehensive valuation assessment

### 📊 Market Data
- **Real-time Stock Data**: Live market prices and metrics
- **Technical Indicators**: RSI, MACD, Moving Averages
- **Options Analysis**: Put/Call ratios and implied volatility
- **Institutional Data**: Ownership and trading activity
- **Market Sentiment**: Fear/Greed indicators and market breadth

### 📈 Financial Metrics
- **Profitability Ratios**: ROE, ROA, ROIC, Margins
- **Liquidity Ratios**: Current Ratio, Quick Ratio, Debt Ratios
- **Efficiency Metrics**: Asset Turnover, Inventory Turnover
- **Growth Metrics**: Revenue and Earnings Growth Analysis
- **Historical Performance**: 5-year financial trend analysis

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Sources**: Yahoo Finance, Alpha Vantage, News APIs
- **Charts**: Chart.js
- **Sentiment Analysis**: TextBlob, News API
- **Valuation Models**: Custom DCF, Peer Comparison

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd investment-research-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   NEWS_API_KEY=your_news_api_key
   TWITTER_BEARER_TOKEN=your_twitter_token
   OPENAI_API_KEY=your_openai_key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## API Keys Setup

### Required API Keys

1. **Alpha Vantage** (Free tier available)
   - Sign up at: https://www.alphavantage.co/
   - Provides financial data and market information

2. **News API** (Free tier available)
   - Sign up at: https://newsapi.org/
   - Provides news sentiment analysis

3. **Twitter API** (Optional)
   - Sign up at: https://developer.twitter.com/
   - Provides social media sentiment analysis

4. **OpenAI API** (Optional)
   - Sign up at: https://openai.com/
   - Provides advanced text analysis

## Usage

### Basic Company Analysis

1. **Enter Company Information**
   - Type a company name or stock symbol in the search box
   - Examples: "AAPL", "Apple", "MSFT", "Microsoft"

2. **View Analysis Results**
   - **Overview Tab**: Key metrics, recommendation, SWOT analysis
   - **Financials Tab**: Revenue growth, profitability metrics
   - **Valuation Tab**: DCF analysis, peer comparison
   - **Competition Tab**: Competitive landscape analysis
   - **Sentiment Tab**: Market and news sentiment

3. **Interpret Results**
   - Review the investment recommendation (BUY/HOLD/SELL)
   - Check confidence level and risk assessment
   - Analyze SWOT factors and competitive advantages
   - Compare valuation metrics with peers

### Advanced Features

#### DCF Valuation
- Access detailed DCF calculations in the Valuation tab
- Adjust growth rates and discount rates for sensitivity analysis
- View terminal value and present value calculations

#### Peer Comparison
- Compare key metrics with industry peers
- Analyze relative valuation ratios
- Identify competitive positioning

#### Sentiment Analysis
- Review news sentiment trends
- Analyze social media sentiment
- Monitor market sentiment indicators

## Project Structure

```
investment-research-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .env                  # Environment variables (create this)
├── services/             # Core analysis services
│   ├── __init__.py
│   ├── company_analyzer.py      # Company and financial analysis
│   ├── valuation_calculator.py  # Valuation models
│   ├── sentiment_analyzer.py    # Sentiment analysis
│   └── market_data_service.py   # Market data and technical analysis
├── templates/            # HTML templates
│   └── index.html        # Main application interface
└── static/              # Static assets (CSS, JS, images)
```

## API Endpoints

### Core Analysis
- `POST /api/analyze` - Comprehensive company analysis
- `GET /api/companies/search` - Company search functionality

### Valuation
- `POST /api/valuation/dcf` - DCF valuation calculation
- `POST /api/valuation/comparison` - Peer comparison analysis

### Sentiment
- `GET /api/sentiment/trends` - Sentiment trend analysis

### Market Data
- `GET /api/market/overview` - Market overview and sector performance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for educational and research purposes only. The information provided should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation for common questions
- Review the API documentation for technical details

## Roadmap

### Planned Features
- [ ] Machine learning-based price predictions
- [ ] Portfolio analysis and optimization
- [ ] Real-time alerts and notifications
- [ ] Advanced technical analysis tools
- [ ] ESG (Environmental, Social, Governance) scoring
- [ ] International market support
- [ ] Mobile application
- [ ] API rate limiting and caching
- [ ] User authentication and saved analyses
- [ ] Export functionality (PDF reports, Excel data)

### Performance Improvements
- [ ] Database integration for faster queries
- [ ] Caching layer for API responses
- [ ] Asynchronous data processing
- [ ] Optimized chart rendering
- [ ] Progressive web app features 