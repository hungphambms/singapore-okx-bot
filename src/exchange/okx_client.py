import ccxt
from config import API_CONFIG, TRADING_CONFIG
from utils.logger import logger

class OKXClient:
    def __init__(self):
        self.exchange = ccxt.okx({
            'apiKey': API_CONFIG['API_KEY'],
            'secret': API_CONFIG['SECRET'],
            'passphrase': API_CONFIG['PASSPHRASE'],
            'enableRateLimit': True,
        })

    def fetch_ohlcv_data(self):
        """
        Fetch OHLCV (Open, High, Low, Close, Volume) data from OKX exchange
        Returns:
            list: List of OHLCV data points
        """
        try:
            symbol = TRADING_CONFIG['SYMBOL']
            timeframe = TRADING_CONFIG['TIMEFRAME']
            limit = 100  # Number of candles to fetch
            
            ohlcv = self.exchange.fetch_ohlcv(
                symbol=symbol,
                timeframe=timeframe,
                limit=limit
            )
            
            logger.info(f"Successfully fetched {len(ohlcv)} OHLCV data points for {symbol}")
            return ohlcv
            
        except Exception as e:
            logger.error(f"Error fetching OHLCV data: {str(e)}")
            raise 