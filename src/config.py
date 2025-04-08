import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent.parent / '.env'
print(f"\nLooking for .env file at: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    # Print the contents of .env file (first few characters only)
    print("\nContents of .env file:")
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                print(f"{key}: {value[:8]}...")

# Try to load .env file
load_dotenv(dotenv_path=env_path, encoding='utf-8', override=True)

# Debug: Print environment variables
print("\nEnvironment variables after loading:")
print(f"OKX_API_KEY: {os.getenv('OKX_API_KEY', 'Not found')[:8]}..." if os.getenv('OKX_API_KEY') else "Not found")
print(f"OKX_SECRET: {os.getenv('OKX_SECRET', 'Not found')[:8]}..." if os.getenv('OKX_SECRET') else "Not found")
print(f"OKX_PASSPHRASE: {os.getenv('OKX_PASSPHRASE', 'Not found')[:8]}..." if os.getenv('OKX_PASSPHRASE') else "Not found")
print(f"OKX_TESTNET: {os.getenv('OKX_TESTNET', 'Not found')}")

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
    'API_KEY': os.getenv('OKX_API_KEY'),
    'SECRET': os.getenv('OKX_SECRET'),
    'PASSWORD': os.getenv('OKX_PASSPHRASE'),
    'TESTNET': os.getenv('OKX_TESTNET', 'False').lower() == 'true',
    'HOSTNAME': os.getenv('OKX_HOSTNAME', 'eea.okx.com'),
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

# ... (other configurations remain unchanged)