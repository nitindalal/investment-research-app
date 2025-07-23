import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Investment Research Platform"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # API Keys
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'demo')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Application Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # API Rate Limiting (requests per minute)
    ALPHA_VANTAGE_RATE_LIMIT = 5  # Free tier limit
    NEWS_API_RATE_LIMIT = 100     # Free tier limit
    
    # Cache Settings
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Financial Analysis Settings
    DEFAULT_GROWTH_RATE = 0.05    # 5% default growth rate
    DEFAULT_DISCOUNT_RATE = 0.10  # 10% default discount rate
    RISK_FREE_RATE = 0.04         # 4% risk-free rate
    MARKET_RISK_PREMIUM = 0.06    # 6% market risk premium
    
    # Sentiment Analysis Settings
    SENTIMENT_ANALYSIS_ENABLED = True
    NEWS_ANALYSIS_ENABLED = True
    SOCIAL_MEDIA_ANALYSIS_ENABLED = bool(TWITTER_BEARER_TOKEN)
    
    # Technical Analysis Settings
    TECHNICAL_INDICATORS_ENABLED = True
    DEFAULT_RSI_PERIOD = 14
    DEFAULT_MACD_FAST = 12
    DEFAULT_MACD_SLOW = 26
    DEFAULT_MACD_SIGNAL = 9
    
    # Valuation Settings
    DCF_ENABLED = True
    PEER_COMPARISON_ENABLED = True
    SENSITIVITY_ANALYSIS_ENABLED = True
    
    # Data Sources
    PRIMARY_DATA_SOURCE = 'yfinance'  # yfinance or alpha_vantage
    BACKUP_DATA_SOURCE = 'alpha_vantage'
    
    # Error Handling
    SHOW_DETAILED_ERRORS = DEBUG
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SHOW_DETAILED_ERRORS = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SHOW_DETAILED_ERRORS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable is required for production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 