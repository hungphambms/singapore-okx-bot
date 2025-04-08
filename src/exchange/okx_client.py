import ccxt
from config import API_CONFIG, TRADING_CONFIG
from utils.logger import logger

class OKXClient:
    def __init__(self):
        self.exchange = ccxt.okx({
            'apiKey': API_CONFIG['API_KEY'],
            'secret': API_CONFIG['SECRET'],
            'password': API_CONFIG['PASSWORD'],
            'enableRateLimit': True,
            'testnet': API_CONFIG['TESTNET'],
            'hostname': API_CONFIG['HOSTNAME'],
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

    def get_balance(self, currency='USDT'):
        """
        Get available balance for a specific currency
        Args:
            currency (str): Currency symbol (default: USDT)
        Returns:
            float: Available balance
        """
        try:
            # Fetch the balance
            balance = self.exchange.fetch_balance()
            
            # Debug: Log the structure of the balance response
            logger.debug(f"Balance response keys: {list(balance.keys())}")
            
            # Check if 'free' exists in the balance response
            if 'free' not in balance:
                logger.error(f"'free' key not found in balance response. Available keys: {list(balance.keys())}")
                # Try to find the currency in the main balance structure
                if currency in balance:
                    logger.info(f"Found {currency} directly in balance structure")
                    return float(balance[currency])
                else:
                    logger.error(f"Currency {currency} not found in balance structure")
                    return 0.0
            
            # Check if the currency exists in the 'free' balance
            if currency not in balance['free']:
                logger.error(f"Currency {currency} not found in 'free' balance. Available currencies: {list(balance['free'].keys())}")
                return 0.0
            
            # Get the available balance
            available = float(balance['free'][currency])
            logger.info(f"Available {currency} balance: {available}")
            return available
            
        except Exception as e:
            logger.error(f"Error fetching balance: {str(e)}")
            # Log more details about the error
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {str(e)}")
            raise

    def place_buy_order(self, symbol, amount, price=None):
        """
        Place a buy order
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
            amount (float): Amount to buy
            price (float, optional): Limit price. If None, places market order
        Returns:
            dict: Order information
        """
        try:
            order_type = 'market' if price is None else 'limit'
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side='buy',
                amount=amount,
                price=price
            )
            logger.info(f"Successfully placed buy order: {order}")
            return order
        except Exception as e:
            logger.error(f"Error placing buy order: {str(e)}")
            raise

    def place_sell_order(self, symbol, amount, price=None):
        """
        Place a sell order
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
            amount (float): Amount to sell
            price (float, optional): Limit price. If None, places market order
        Returns:
            dict: Order information
        """
        try:
            order_type = 'market' if price is None else 'limit'
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type,
                side='sell',
                amount=amount,
                price=price
            )
            logger.info(f"Successfully placed sell order: {order}")
            return order
        except Exception as e:
            logger.error(f"Error placing sell order: {str(e)}")
            raise

    def get_position(self, symbol):
        """
        Get current position for a symbol
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
        Returns:
            dict: Position information
        """
        try:
            positions = self.exchange.fetch_positions([symbol])
            if positions:
                position = positions[0]
                logger.info(f"Current position for {symbol}: {position}")
                return position
            return None
        except Exception as e:
            logger.error(f"Error fetching position: {str(e)}")
            raise

    def cancel_order(self, order_id, symbol):
        """
        Cancel an existing order
        Args:
            order_id (str): Order ID to cancel
            symbol (str): Trading pair symbol
        Returns:
            dict: Cancellation confirmation
        """
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Successfully cancelled order {order_id}")
            return result
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise 