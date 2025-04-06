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
        
        # 1. Check USDT balance
        usdt_balance = client.get_balance('USDT')
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