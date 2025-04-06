from config import TRADING_CONFIG
from utils.logger import logger

class ValueAreaStrategy:
    @staticmethod
    def generate_signals(data):
        try:
            # Long Conditions
            data = ValueAreaStrategy.calculate_long_conditions(data)
            
            # Short Conditions
            data = ValueAreaStrategy.calculate_short_conditions(data)
            
            # Combine Conditions
            data = ValueAreaStrategy.combine_conditions(data)
            
            # Calculate Targets and Stop-Loss
            data = ValueAreaStrategy.calculate_risk_levels(data)
            
            return data
            
        except Exception as e:
            logger.error(f"Error generating trading signals: {str(e)}")
            raise

    @staticmethod
    def calculate_long_conditions(data):
        data['priceOpensBelowVAL'] = data['open'] < data['VAL']
        data['priceReentersVAL'] = (data['close'] > data['VAL']) & (data['open'] < data['VAL'])
        data['priceAbovePOC'] = data['close'] > data['POC']
        data['bullishEngulfing'] = data['bullishEngulfing']
        data['bullishPinBar'] = data['pinBar'] & (data['close'] > data['open'])
        
        # Combine long conditions
        data['longCondition'] = (
            data['priceOpensBelowVAL'] & 
            data['priceReentersVAL'] & 
            data['priceAbovePOC'] & 
            (data['bullishEngulfing'] | data['bullishPinBar'])
        )
        
        return data

    @staticmethod
    def calculate_short_conditions(data):
        data['priceOpensAboveVAH'] = data['open'] > data['VAH']
        data['priceReentersVAH'] = (data['close'] < data['VAH']) & (data['open'] > data['VAH'])
        data['priceBelowPOC'] = data['close'] < data['POC']
        data['bearishEngulfing'] = data['bearishEngulfing']
        data['bearishPinBar'] = data['pinBar'] & (data['close'] < data['open'])
        
        # Combine short conditions
        data['shortCondition'] = (
            data['priceOpensAboveVAH'] & 
            data['priceReentersVAH'] & 
            data['priceBelowPOC'] & 
            (data['bearishEngulfing'] | data['bearishPinBar'])
        )
        
        return data

    @staticmethod
    def combine_conditions(data):
        # Add position size based on conditions
        data['positionSize'] = 0.0
        data.loc[data['longCondition'], 'positionSize'] = TRADING_CONFIG['TRADE_SIZE']
        data.loc[data['shortCondition'], 'positionSize'] = -TRADING_CONFIG['TRADE_SIZE']
        
        return data

    @staticmethod
    def calculate_risk_levels(data):
        # Calculate stop loss and take profit levels
        data['stopLoss'] = 0.0
        data['takeProfit'] = 0.0
        
        # Long positions
        long_mask = data['positionSize'] > 0
        data.loc[long_mask, 'stopLoss'] = data.loc[long_mask, 'VAL'] * 0.99  # 1% below VAL
        data.loc[long_mask, 'takeProfit'] = data.loc[long_mask, 'VAH'] * 1.01  # 1% above VAH
        
        # Short positions
        short_mask = data['positionSize'] < 0
        data.loc[short_mask, 'stopLoss'] = data.loc[short_mask, 'VAH'] * 1.01  # 1% above VAH
        data.loc[short_mask, 'takeProfit'] = data.loc[short_mask, 'VAL'] * 0.99  # 1% below VAL
        
        return data 