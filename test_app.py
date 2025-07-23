#!/usr/bin/env python3
"""
Test script for the Investment Research Platform
This script tests the basic functionality of the application
"""

import requests
import json
import time
from services.company_analyzer import CompanyAnalyzer
from services.valuation_calculator import ValuationCalculator
from services.sentiment_analyzer import SentimentAnalyzer
from services.market_data_service import MarketDataService

def test_services():
    """Test the core services"""
    print("🧪 Testing Investment Research Platform Services")
    print("=" * 50)
    
    # Initialize services
    company_analyzer = CompanyAnalyzer()
    valuation_calculator = ValuationCalculator()
    sentiment_analyzer = SentimentAnalyzer()
    market_data_service = MarketDataService()
    
    # Test company: Apple Inc.
    test_symbol = "AAPL"
    test_company = "Apple"
    
    print(f"\n📊 Testing Company Analysis for {test_company} ({test_symbol})")
    print("-" * 40)
    
    try:
        # Test company info
        print("1. Testing Company Info...")
        company_info = company_analyzer.get_company_info(test_symbol)
        if company_info:
            print(f"   ✅ Company: {company_info.get('name', 'N/A')}")
            print(f"   ✅ Sector: {company_info.get('sector', 'N/A')}")
            print(f"   ✅ Market Cap: ${company_info.get('market_cap', 0) / 1e9:.2f}B")
        else:
            print("   ❌ Failed to get company info")
        
        # Test financial data
        print("\n2. Testing Financial Data...")
        financial_data = company_analyzer.get_financial_data(test_symbol)
        if financial_data:
            print("   ✅ Financial data retrieved")
            if financial_data.get('profitability_metrics'):
                roe = financial_data['profitability_metrics'].get('roe', 0)
                print(f"   ✅ ROE: {roe * 100:.2f}%" if roe else "   ⚠️ ROE not available")
        else:
            print("   ❌ Failed to get financial data")
        
        # Test market data
        print("\n3. Testing Market Data...")
        market_data = market_data_service.get_market_data(test_symbol)
        if market_data:
            print("   ✅ Market data retrieved")
            current_price = market_data.get('current_price', 0)
            print(f"   ✅ Current Price: ${current_price:.2f}" if current_price else "   ⚠️ Price not available")
        else:
            print("   ❌ Failed to get market data")
        
        # Test sentiment analysis
        print("\n4. Testing Sentiment Analysis...")
        sentiment_data = sentiment_analyzer.analyze_sentiment(test_company)
        if sentiment_data:
            print("   ✅ Sentiment analysis completed")
            overall_sentiment = sentiment_data.get('overall_sentiment', 0)
            print(f"   ✅ Overall Sentiment: {overall_sentiment:.3f}")
        else:
            print("   ❌ Failed to get sentiment data")
        
        # Test valuation
        print("\n5. Testing Valuation Analysis...")
        if financial_data:
            valuations = valuation_calculator.calculate_valuations(financial_data)
            if valuations:
                print("   ✅ Valuation analysis completed")
                if valuations.get('dcf_valuation'):
                    print("   ✅ DCF valuation available")
            else:
                print("   ❌ Failed to calculate valuations")
        else:
            print("   ⚠️ Skipping valuation (no financial data)")
        
        # Test competitive analysis
        print("\n6. Testing Competitive Analysis...")
        competitive_analysis = company_analyzer.get_competitive_analysis(test_symbol)
        if competitive_analysis:
            print("   ✅ Competitive analysis completed")
            if competitive_analysis.get('market_position', {}).get('swot_analysis'):
                print("   ✅ SWOT analysis available")
        else:
            print("   ❌ Failed to get competitive analysis")
        
        print("\n" + "=" * 50)
        print("✅ Service testing completed!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        print("This might be due to missing API keys or network issues.")

def test_api_endpoints():
    """Test the Flask API endpoints"""
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"⚠️ Server responded with status {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Flask application first.")
        print("   Run: python app.py")
        return
    
    # Test company search
    print("\n1. Testing Company Search...")
    try:
        response = requests.get(f"{base_url}/api/companies/search?q=AAPL", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Search completed, found {len(data)} results")
        else:
            print(f"   ❌ Search failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Search error: {str(e)}")
    
    # Test market overview
    print("\n2. Testing Market Overview...")
    try:
        response = requests.get(f"{base_url}/api/market/overview", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Market overview retrieved")
        else:
            print(f"   ❌ Market overview failed with status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Market overview error: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Investment Research Platform - Test Suite")
    print("=" * 60)
    
    # Test services
    test_services()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    print("🎉 Testing completed!")
    print("\nNext steps:")
    print("1. Set up your API keys in a .env file")
    print("2. Run: python app.py")
    print("3. Open http://localhost:5000 in your browser")
    print("4. Try analyzing a company like 'AAPL' or 'Apple'")

if __name__ == "__main__":
    main() 