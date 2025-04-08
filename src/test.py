import ccxt
from config import API_CONFIG

def test_okx_connection():
    try:
        # Get API credentials from config
        api_key = API_CONFIG['API_KEY']
        api_secret = API_CONFIG['SECRET']
        password = API_CONFIG['PASSWORD']
        
        # Print API configuration (first 8 characters only for security)
        print("\nAPI Configuration:")
        print(f"API Key: {api_key[:8]}..." if api_key else "None")
        print(f"Secret: {api_secret[:8]}..." if api_secret else "None")
        print(f"Passphrase: {password[:8]}..." if password else "None")
        
        if not all([api_key, api_secret, password]):
            print("❌ Error: Missing API credentials in config.py")
            print("Please make sure you have API_KEY, SECRET, and PASSPHRASE in your config.py file")
            return False
            
        # Initialize OKX exchange with testnet configuration
        exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            },
            "hostname": API_CONFIG['HOSTNAME'],
            'testnet': API_CONFIG['TESTNET']  # Enable testnet mode
        })
        
        # Test connection by fetching account balance
        print("\n🔄 Testing connection to OKX testnet...")
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
