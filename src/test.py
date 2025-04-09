from exchange.okx_client import OKXClient
from config import API_CONFIG

def test_okx_connection():
    try:
        # Print API configuration (first 8 characters only for security)
        print("\nAPI Configuration:")
        print(f"API Key: {API_CONFIG['API_KEY'][:8]}..." if API_CONFIG['API_KEY'] else "None")
        print(f"Secret: {API_CONFIG['SECRET'][:8]}..." if API_CONFIG['SECRET'] else "None")
        print(f"Passphrase: {API_CONFIG['PASSWORD'][:8]}..." if API_CONFIG['PASSWORD'] else "None")
        
        if not all([API_CONFIG['API_KEY'], API_CONFIG['SECRET'], API_CONFIG['PASSWORD']]):
            print("❌ Error: Missing API credentials in config.py")
            print("Please make sure you have API_KEY, SECRET, and PASSPHRASE in your config.py file")
            return False
            
        # Initialize OKX client
        print("\n🔄 Testing connection to OKX testnet...")
        client = OKXClient()
        
        # Test connection by fetching account balance
        balance = client.get_balance('USDT')
        
        if balance is not None:
            print("✅ Successfully connected to OKX API!")
            print(f"USDT Balance: {balance}")
            return True
            
    except Exception as e:
        print("❌ Error connecting to OKX:")
        print(str(e))
        return False

if __name__ == "__main__":
    test_okx_connection()
