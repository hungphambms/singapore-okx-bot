from exchange.okx_client import OKXClient
from config import TRADING_CONFIG
from utils.logger import logger

def calculate_buy_amount(available_usdt, current_price, max_position_size=0.8):
    """
    Calculate the amount of coins that can be bought
    Args:
        available_usdt (float): Available USDT balance
        current_price (float): Current price of the coin
        max_position_size (float): Maximum proportion of balance to use (0.8 = 80%)
    Returns:
        float: Amount of coins that can be bought
    """
    usdt_to_use = available_usdt * max_position_size
    possible_amount = usdt_to_use / current_price
    
    # Round the amount according to exchange requirements (e.g., 0.001 BTC)
    return round(possible_amount, 3)

def execute_buy_strategy():
    """
    Execute the buying strategy
    Returns:
        bool: True if buy order was successful, False otherwise
    """
    try:
        client = OKXClient()
        symbol = TRADING_CONFIG['SYMBOL']  # e.g., 'BTC/USDT'
        
        # 1. Check USDT balance with better error handling
        try:
            # Debug: Print the client configuration
            logger.info(f"Using OKX API with testnet: {TRADING_CONFIG.get('TESTNET', False)}")
            logger.info(f"Using hostname: {TRADING_CONFIG.get('HOSTNAME', 'eea.okx.com')}")
            
            # Try to get the balance with more detailed error handling
            usdt_balance = client.get_balance('USDT')
            logger.info(f"Successfully retrieved USDT balance: {usdt_balance}")
            
            # If USDT balance is insufficient, try USDC
            if usdt_balance < TRADING_CONFIG.get('MIN_USDT_BALANCE', 10):
                logger.info("USDT balance insufficient, trying USDC...")
                usdc_balance = client.get_balance('USDC')
                logger.info(f"USDC balance: {usdc_balance}")
                
                # If USDC balance is sufficient, use it instead
                if usdc_balance >= TRADING_CONFIG.get('MIN_USDT_BALANCE', 10):
                    logger.info(f"Using USDC balance instead of USDT: {usdc_balance}")
                    usdt_balance = usdc_balance  # Use USDC balance as if it were USDT
                else:
                    logger.warning(f"Insufficient USDT and USDC balance: USDT={usdt_balance}, USDC={usdc_balance}")
                    return False
        except Exception as balance_error:
            logger.error(f"Detailed balance error: {str(balance_error)}")
            # Try to get the raw balance for debugging
            try:
                raw_balance = client.exchange.fetch_balance()
                logger.info(f"Raw balance structure: {raw_balance.keys()}")
                if 'free' in raw_balance:
                    logger.info(f"Available currencies: {raw_balance['free'].keys()}")
                return False
            except Exception as raw_error:
                logger.error(f"Error fetching raw balance: {str(raw_error)}")
                return False
            
        if usdt_balance < TRADING_CONFIG.get('MIN_USDT_BALANCE', 10):
            logger.warning(f"Insufficient USDT balance: {usdt_balance}")
            return False
            
        # 2. Check current position
        current_position = client.get_position(symbol)
        if current_position and float(current_position['size']) > 0:
            logger.warning(f"Already have position in {symbol}")
            return False
            
        # 3. Get current market price
        ohlcv = client.fetch_ohlcv_data()
        current_price = ohlcv[-1][4]  # Close price of the latest candle
        
        # 4. Calculate buy amount based on available balance
        amount_to_buy = calculate_buy_amount(
            available_usdt=usdt_balance,
            current_price=current_price
        )
        
        # 5. Validate minimum trade amount
        if amount_to_buy < TRADING_CONFIG.get('MIN_TRADE_AMOUNT', 0.001):
            logger.warning(f"Buy amount too small: {amount_to_buy}")
            return False
            
        # 6. Place market buy order
        order = client.place_buy_order(
            symbol=symbol,
            amount=amount_to_buy
        )
        
        logger.info(f"Successfully placed buy order: {order}")
        return True
        
    except Exception as e:
        logger.error(f"Error executing buy strategy: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    success = execute_buy_strategy()
    if success:
        print("Buy order executed successfully!")
    else:
        print("Failed to execute buy order") 