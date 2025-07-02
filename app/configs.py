import os

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    YFINANCE_CACHE_TTL = 300  # Cache stock data for 5 minutes
    NEWS_CACHE_TTL = 1800  # Cache news for 30 minutes
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    YFINANCE_CACHE_TTL = 600  # Cache stock data for 10 minutes in production
    
# Configuration dictionary
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Active configuration
active_config = config_dict[os.getenv('FLASK_ENV', 'default')]

#redis cache update