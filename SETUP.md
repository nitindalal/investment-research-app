# Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys (Optional but Recommended)
Create a `.env` file in the project root:
```env
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
```

**Free API Keys:**
- [Alpha Vantage](https://www.alphavantage.co/) - Financial data
- [News API](https://newsapi.org/) - News sentiment

### 3. Run the Application
```bash
python run.py
```

### 4. Open Your Browser
Navigate to: `http://localhost:5000`

### 5. Start Analyzing
Try these examples:
- **AAPL** (Apple Inc.)
- **MSFT** (Microsoft)
- **GOOGL** (Alphabet)
- **TSLA** (Tesla)

## 🧪 Test the Application
```bash
python test_app.py
```

## 📊 What You'll Get

### Company Analysis
- ✅ Revenue sources and cost drivers
- ✅ Financial metrics (ROE, ROA, margins)
- ✅ Growth projections
- ✅ Market position and competition

### Valuation Analysis
- ✅ DCF (Discounted Cash Flow) valuation
- ✅ Peer comparison
- ✅ Multiple valuation ratios
- ✅ Fair value range

### Market Intelligence
- ✅ Real-time stock data
- ✅ Technical indicators
- ✅ Market sentiment
- ✅ News sentiment analysis

### Investment Recommendations
- ✅ BUY/HOLD/SELL recommendations
- ✅ Confidence levels
- ✅ Risk assessment
- ✅ SWOT analysis

## 🔧 Troubleshooting

### Common Issues

**1. "Module not found" errors**
```bash
pip install -r requirements.txt
```

**2. API rate limits**
- Get free API keys from the providers
- The app works with demo keys but has limited functionality

**3. No data for some companies**
- Try different stock symbols
- Some companies may have limited public data

**4. Server won't start**
- Check if port 5000 is available
- Try: `python app.py --port 5001`

## 📈 Example Analysis

When you analyze **AAPL (Apple Inc.)**, you'll see:

- **Company Info**: Apple Inc., Technology sector, $2.5T+ market cap
- **Financial Metrics**: ROE ~150%, Gross Margin ~42%
- **Valuation**: DCF analysis, P/E comparison
- **Sentiment**: News and market sentiment scores
- **Recommendation**: BUY/HOLD/SELL with confidence level

## 🎯 Next Steps

1. **Get API Keys** for full functionality
2. **Analyze Your Portfolio** companies
3. **Compare Companies** side by side
4. **Export Data** for further analysis
5. **Customize** valuation parameters

## 📞 Support

- Check the main README.md for detailed documentation
- Run `python test_app.py` to diagnose issues
- Create an issue if you encounter problems

---

**Happy Investing! 📈💰** 