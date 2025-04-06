class CandlestickPatterns:
    @staticmethod
    def identify_patterns(data):
        data['bullishEngulfing'] = CandlestickPatterns.bullish_engulfing(data)
        data['bearishEngulfing'] = CandlestickPatterns.bearish_engulfing(data)
        data['pinBar'] = CandlestickPatterns.pin_bar(data)
        data['insideBar'] = CandlestickPatterns.inside_bar(data)
        return data

    @staticmethod
    def bullish_engulfing(data):
        return (
            (data['close'].shift(1) < data['open'].shift(1)) & 
            (data['close'] > data['open']) & 
            (data['close'] > data['open'].shift(1)) & 
            (data['open'] < data['close'].shift(1))
        )

    @staticmethod
    def bearish_engulfing(data):
        return (
            (data['close'].shift(1) > data['open'].shift(1)) & 
            (data['close'] < data['open']) & 
            (data['close'] < data['open'].shift(1)) & 
            (data['open'] > data['close'].shift(1))
        )

    @staticmethod
    def pin_bar(data):
        """
        Identify pin bar patterns
        A pin bar has a long tail (wick) and a small body
        """
        body_size = abs(data['close'] - data['open'])
        upper_wick = data['high'] - data[['open', 'close']].max(axis=1)
        lower_wick = data[['open', 'close']].min(axis=1) - data['low']
        
        # Bullish pin bar: long lower wick, small upper wick
        bullish_pin = (
            (lower_wick > 2 * body_size) &  # Long lower wick
            (upper_wick < body_size) &      # Small upper wick
            (body_size < (data['high'] - data['low']) * 0.3)  # Small body
        )
        
        # Bearish pin bar: long upper wick, small lower wick
        bearish_pin = (
            (upper_wick > 2 * body_size) &  # Long upper wick
            (lower_wick < body_size) &      # Small lower wick
            (body_size < (data['high'] - data['low']) * 0.3)  # Small body
        )
        
        return bullish_pin | bearish_pin

    @staticmethod
    def inside_bar(data):
        """
        Identify inside bar patterns
        An inside bar has a high and low that are inside the previous bar's range
        """
        return (
            (data['high'] <= data['high'].shift(1)) & 
            (data['low'] >= data['low'].shift(1))
        )

    # ... (các pattern khác) 