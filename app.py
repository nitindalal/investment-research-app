from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.company_analyzer import CompanyAnalyzer
from services.valuation_calculator import ValuationCalculator
from services.sentiment_analyzer import SentimentAnalyzer
from services.market_data_service import MarketDataService
import logging
import math
import numpy as np

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("services.company_analyzer").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize services
company_analyzer = CompanyAnalyzer()
valuation_calculator = ValuationCalculator()
sentiment_analyzer = SentimentAnalyzer()
market_data_service = MarketDataService()

def clean_nans(obj):
    if isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nans(x) for x in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    else:
        return obj

@app.route('/')
def index():
    """Main page of the investment research application"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_company():
    """Analyze a company based on name or stock symbol"""
    try:
        data = request.get_json()
        company_input = data.get('company_input', '').strip()
        
        if not company_input:
            return jsonify({'error': 'Company name or symbol is required'}), 400
        
        logger.info(f"Analyzing company: {company_input}")
        
        # Get basic company information
        company_info = company_analyzer.get_company_info(company_input)
        
        if not company_info:
            return jsonify({'error': 'Company not found'}), 404
        
        # Get financial data
        financial_data = company_analyzer.get_financial_data(company_info['symbol'])
        
        # Get market data
        market_data = market_data_service.get_market_data(company_info['symbol'])
        
        # Get sentiment analysis
        sentiment_data = sentiment_analyzer.analyze_sentiment(company_info['name'])
        
        # Calculate valuations (existing)
        valuations = valuation_calculator.calculate_valuations(financial_data)
        
        # Add DCF and peer comparison using market data
        dcf_result = valuation_calculator.calculate_dcf(company_info['symbol'])
        peer_comparison = valuation_calculator.compare_with_peers(company_info['symbol'])
        valuations['dcf_detailed'] = dcf_result
        valuations['peer_comparison'] = peer_comparison
        
        # Get competitive analysis
        competitive_analysis = company_analyzer.get_competitive_analysis(company_info['symbol'])
        
        # Get industry analysis
        industry_analysis = company_analyzer.get_industry_analysis(company_info['sector'])
        
        # Compile comprehensive analysis
        analysis_result = {
            'company_info': company_info,
            'financial_data': financial_data,
            'market_data': market_data,
            'sentiment_data': sentiment_data,
            'valuations': valuations,
            'competitive_analysis': competitive_analysis,
            'industry_analysis': industry_analysis,
            'investment_recommendation': company_analyzer.generate_recommendation(
                financial_data, market_data, sentiment_data, valuations
            )
        }
        
        return jsonify(clean_nans(analysis_result))
        
    except Exception as e:
        logger.error(f"Error analyzing company: {str(e)}")
        return jsonify({'error': 'An error occurred during analysis'}), 500

@app.route('/api/companies/search', methods=['GET'])
def search_companies():
    """Search for companies by name or symbol"""
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify([])
        
        results = company_analyzer.search_companies(query)
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error searching companies: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/valuation/dcf', methods=['POST'])
def calculate_dcf():
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        # Use default rates or calculate from market data if needed
        dcf_result = valuation_calculator.calculate_dcf(symbol)
        return jsonify(clean_nans(dcf_result))
    except Exception as e:
        logger.error(f"Error in DCF endpoint: {str(e)}")
        return jsonify({'error': 'DCF calculation failed'}), 500

@app.route('/api/valuation/comparison', methods=['POST'])
def compare_valuations():
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        comparison_result = valuation_calculator.compare_with_peers(symbol)
        return jsonify(clean_nans(comparison_result))
    except Exception as e:
        logger.error(f"Error in peer comparison endpoint: {str(e)}")
        return jsonify({'error': 'Peer comparison failed'}), 500

@app.route('/api/sentiment/trends', methods=['GET'])
def get_sentiment_trends():
    """Get sentiment trends for a company"""
    try:
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({'error': 'Stock symbol is required'}), 400
        
        trends = sentiment_analyzer.get_sentiment_trends(symbol)
        return jsonify(trends)
        
    except Exception as e:
        logger.error(f"Error getting sentiment trends: {str(e)}")
        return jsonify({'error': 'Failed to get sentiment trends'}), 500

@app.route('/api/market/overview', methods=['GET'])
def get_market_overview():
    """Get market overview and sector performance"""
    try:
        overview = market_data_service.get_market_overview()
        return jsonify(overview)
        
    except Exception as e:
        logger.error(f"Error getting market overview: {str(e)}")
        return jsonify({'error': 'Failed to get market overview'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 