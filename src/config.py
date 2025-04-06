import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, encoding='utf-8')

# Configuration file that manages all settings for the trading bot
# Contains:
# 1. Environment variables loading from .env file
# 2. Trading configuration (DRY_RUN, trading pair, timeframe, position size)
# 3. API credentials for OKX exchange
# Note: API credentials should be moved to environment variables for security

# Trading Configuration
TRADING_CONFIG = {
    'DRY_RUN': os.getenv('DRY_RUN', 'True').lower() == 'true',
    'SYMBOL': 'BTC/USDT',          # Trading pair
    'TIMEFRAME': '15m',            # Timeframe for candlestick data
    'TRADE_SIZE': float(os.getenv('TRADE_SIZE', '0.001')),
    'MIN_USDT_BALANCE': 10,        # Minimum USDT balance required to trade
    'MIN_TRADE_AMOUNT': 0.001,     # Minimum trade amount per order
    'MIN_PROFIT_PERCENTAGE': 2.0,  # Minimum profit percentage to take profit
    'STOP_LOSS_PERCENTAGE': -2.0,  # Maximum loss percentage before stop loss
}

# API Configuration
API_CONFIG = {
    'API_KEY': 'your_api_key',
    'SECRET': 'your_secret_key',
    'PASSPHRASE': 'your_passphrase',
}

# Logging Configuration
LOGGING_CONFIG = {
    'LOG_LEVEL': 'INFO',
    'LOG_FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'LOG_FILE': 'trading_bot.log'
}

# Indicator Configuration
INDICATOR_CONFIG = {
    'VALUE_AREA': {
        'length': 20,
        'vah_multiplier': 0.7,
        'val_multiplier': 0.3,
        'poc_multiplier': 0.5
    },
    'MACD': {
        'fast_period': 12,
        'slow_period': 26,
        'signal_period': 9
    },
    'RSI': {
        'period': 14
    },
    'EMA': {
        'short_period': 9,
        'long_period': 21
    }
}

# ... (các config khác giữ nguyên như cũ) 