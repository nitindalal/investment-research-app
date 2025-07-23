#!/usr/bin/env python3
"""
Startup script for the Investment Research Platform
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys
from app import app
from config import config

# Use 'development' as the default if FLASK_CONFIG is not set
config_name = os.getenv('FLASK_CONFIG') or 'development'
app.config.from_object(config.get(config_name, config['development']))

def main():
    """Main startup function"""
    print("🚀 Starting Investment Research Platform...")
    print("=" * 50)
    
    # Set configuration
    # config_name = os.getenv('FLASK_CONFIG', 'development')
    # app.config.from_object(config[config_name])
    
    # Check for required API keys
    print("\n🔑 Checking API Configuration...")
    
    if app.config['ALPHA_VANTAGE_API_KEY'] == 'demo':
        print("⚠️  Warning: Using demo Alpha Vantage API key")
        print("   Get a free key at: https://www.alphavantage.co/")
    
    if app.config['NEWS_API_KEY'] == 'demo':
        print("⚠️  Warning: Using demo News API key")
        print("   Get a free key at: https://newsapi.org/")
    
    if not app.config['TWITTER_BEARER_TOKEN']:
        print("ℹ️  Twitter API not configured (optional)")
        print("   Get a key at: https://developer.twitter.com/")
    
    if not app.config['OPENAI_API_KEY']:
        print("ℹ️  OpenAI API not configured (optional)")
        print("   Get a key at: https://openai.com/")
    
    print("\n✅ Configuration loaded successfully!")
    
    # Start the application
    print("\n🌐 Starting web server...")
    print("   URL: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=app.config['DEBUG'],
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 