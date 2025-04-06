import ccxt
from config import API_CONFIG

def test_okx_connection():
    try:
        # Get API credentials from config
        api_key = API_CONFIG['API_KEY']
        api_secret = API_CONFIG['SECRET']
        password = API_CONFIG['PASSPHRASE']
        
        if not all([api_key, api_secret, password]):
            print("❌ Error: Missing API credentials in config.py")
            print("Please make sure you have API_KEY, SECRET, and PASSPHRASE in your config.py file")
            return False
            
        # Initialize OKX exchange
        exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
            'enableRateLimit': True
        })
        
        # Test connection by fetching account balance
        print("🔄 Testing connection to OKX...")
        balance = exchange.fetch_balance()
        
        if balance:
            print("✅ Successfully connected to OKX API!")
            print("Account type:", balance.get('info', {}).get('accountType', 'Unknown'))
            return True
            
    except Exception as e:
        print("❌ Error connecting to OKX:")
        print(str(e))
        return False

if __name__ == "__main__":
    test_okx_connection()
