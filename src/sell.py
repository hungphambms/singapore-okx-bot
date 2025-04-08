from exchange.okx_client import OKXClient
from config import TRADING_CONFIG
from utils.logger import logger

def calculate_profit_percentage(entry_price, current_price):
    """
    Calculate profit percentage
    Args:
        entry_price (float): Entry price of the position
        current_price (float): Current market price
    Returns:
        float: Profit percentage
    """
    return ((current_price - entry_price) / entry_price) * 100

def should_take_profit(entry_price, current_price, min_profit=2.0):
    """
    Check if we should take profit
    Args:
        entry_price (float): Entry price of the position
        current_price (float): Current market price
        min_profit (float): Minimum profit percentage to take profit
    Returns:
        bool: True if should take profit
    """
    profit_percentage = calculate_profit_percentage(entry_price, current_price)
    return profit_percentage >= min_profit

def execute_sell_strategy():
    """
    Execute the selling strategy
    Returns:
        bool: True if sell order was successful, False otherwise
    """
    try:
        client = OKXClient()
        symbol = TRADING_CONFIG['SYMBOL']  # e.g., 'BTC/USDT'
        
        # 1. Check current position
        position = client.get_position(symbol)
        if not position or float(position['size']) <= 0:
            logger.warning(f"No position to sell in {symbol}")
            return False
            
        position_size = float(position['size'])
        entry_price = float(position['entryPrice'])
        
        # 2. Get current market price
        ohlcv = client.fetch_ohlcv_data()
        current_price = ohlcv[-1][4]  # Close price of the latest candle
        
        # 3. Check take profit conditions
        min_profit = TRADING_CONFIG.get('MIN_PROFIT_PERCENTAGE', 2.0)
        if not should_take_profit(entry_price, current_price, min_profit):
            logger.info(f"Current profit not reaching minimum threshold: {min_profit}%")
            return False
            
        # 4. Place market sell order
        order = client.place_sell_order(
            symbol=symbol,
            amount=position_size
        )
        
        # 5. Log profit information
        profit_percentage = calculate_profit_percentage(entry_price, current_price)
        logger.info(f"Successfully placed sell order with profit: {profit_percentage:.2f}%")
        logger.info(f"Order details: {order}")
        return True
        
    except Exception as e:
        logger.error(f"Error executing sell strategy: {str(e)}")
        return False

def execute_stop_loss():
    """
    Execute the stop loss strategy
    Returns:
        bool: True if stop loss should be triggered, False otherwise
    """
    try:
        client = OKXClient()
        symbol = TRADING_CONFIG['SYMBOL']
        
        # 1. Check current position
        position = client.get_position(symbol)
        if not position or float(position['size']) <= 0:
            logger.warning(f"No position to apply stop loss in {symbol}")
            return False
            
        position_size = float(position['size'])
        entry_price = float(position['entryPrice'])
        
        # 2. Get current market price
        ohlcv = client.fetch_ohlcv_data()
        current_price = ohlcv[-1][4]  # Close price of the latest candle
        
        # 3. Check stop loss conditions
        stop_loss_percentage = TRADING_CONFIG.get('STOP_LOSS_PERCENTAGE', -5.0)
        loss_percentage = ((current_price - entry_price) / entry_price) * 100
        
        if loss_percentage <= stop_loss_percentage:
            logger.info(f"Current loss ({loss_percentage:.2f}%) reaching stop loss threshold: {stop_loss_percentage}%")
            return True
            
        return False
        
    except Exception as e:
        logger.error(f"Error executing stop loss strategy: {str(e)}")
        return False

def execute_sell_decision():
    """
    Execute the sell decision based on both take profit and stop loss strategies
    Returns:
        bool: True if sell order was successful, False otherwise
    """
    try:
        # First check if stop loss should be triggered
        if execute_stop_loss():
            logger.info("Stop loss triggered, executing sell order")
            return execute_sell_strategy()
        
        # If not, check if take profit should be triggered
        return execute_sell_strategy()
        
    except Exception as e:
        logger.error(f"Error executing sell decision: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    success = execute_sell_decision()
    if success:
        print("Sell order executed successfully!")
    else:
        print("Failed to execute sell order or no position to sell") 