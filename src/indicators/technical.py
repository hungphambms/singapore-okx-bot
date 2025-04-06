import talib as ta
import pandas as pd
from config import INDICATOR_CONFIG

class TechnicalIndicators:
    @staticmethod
    def calculate_all(data):
        try:
            data = TechnicalIndicators.calculate_value_area(data)
            data = TechnicalIndicators.calculate_vwap(data)
            data = TechnicalIndicators.calculate_momentum(data)
            return data
        except Exception as e:
            raise Exception(f"Error calculating indicators: {str(e)}")

    @staticmethod
    def calculate_value_area(data):
        val_length = INDICATOR_CONFIG['VALUE_AREA']['length']
        volume_profile = data['high'].rolling(val_length).max() - data['low'].rolling(val_length).min()
        
        data['VAH'] = data['close'].rolling(val_length).max() - (volume_profile * INDICATOR_CONFIG['VALUE_AREA']['vah_multiplier'])
        data['VAL'] = data['close'].rolling(val_length).min() + (volume_profile * INDICATOR_CONFIG['VALUE_AREA']['val_multiplier'])
        data['POC'] = data['close'].rolling(val_length).max() - (volume_profile * INDICATOR_CONFIG['VALUE_AREA']['poc_multiplier'])
        
        return data

    @staticmethod
    def calculate_vwap(data):
        data['typical_price'] = (data['high'] + data['low'] + data['close']) / 3
        data['cumulative_volume'] = data['volume'].cumsum()
        data['cumulative_typical_price_volume'] = (data['typical_price'] * data['volume']).cumsum()
        data['vwap'] = data['cumulative_typical_price_volume'] / data['cumulative_volume']
        return data

    @staticmethod
    def calculate_momentum(data):
        # MACD
        data['macdLine'], data['signalLine'], _ = ta.MACD(
            data['close'],
            fastperiod=INDICATOR_CONFIG['MACD']['fast_period'],
            slowperiod=INDICATOR_CONFIG['MACD']['slow_period'],
            signalperiod=INDICATOR_CONFIG['MACD']['signal_period']
        )
        
        # RSI
        data['rsi'] = ta.RSI(data['close'], timeperiod=INDICATOR_CONFIG['RSI']['period'])
        
        # EMAs
        data['ema9'] = ta.EMA(data['close'], timeperiod=INDICATOR_CONFIG['EMA']['short_period'])
        data['ema21'] = ta.EMA(data['close'], timeperiod=INDICATOR_CONFIG['EMA']['long_period'])
        
        return data 