import ccxt
import os
from dotenv import load_dotenv

def test_okx_connection():
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Hardcoded API credentials for debugging
        api_key = "f4c0c56e-c1c2-4455-b6ed-4b81a1f40226"
        secret = "9C5D613140292CA1DCEE758F672638BF"
        password = "Linchakpan1!"
        testnet = False  # Changed to mainnet
        
        if not all([api_key, secret, password]):
            print("❌ Error: Missing API credentials")
            return False
            
        # Initialize OKX exchange with credentials and specific domain
        exchange = ccxt.okx({
            'apiKey': api_key,
            'secret': secret,
            'password': password,
            'enableRateLimit': True,
            'testnet': testnet,
            'urls': {
                'api': {
                    'rest': 'https://eea.okx.com'
                }
            }
        })
        
        # Test connection by fetching account balance
        print("\n🔄 Testing connection to OKX...")
        print(f"Using {'testnet' if testnet else 'mainnet'} environment")
        print(f"API Key: {api_key[:8]}...{api_key[-4:]}")
        print(f"Using domain: https://eea.okx.com")
        
        balance = exchange.fetch_balance()
        
        if balance:
            print("✅ Successfully connected to OKX API!")
            print("Account type:", balance.get('info', {}).get('accountType', 'Unknown'))
            print(f"USDT Balance: {balance.get('USDT', {}).get('free', 0)}")
            return True
            
    except Exception as e:
        print("❌ Error connecting to OKX:")
        print(str(e))
        if "API key doesn't exist" in str(e):
            print("\nPossible solutions:")
            print("1. Verify your API key is correct")
            print("2. Make sure your API key is activated on the OKX platform")
            print("3. Check if you're using the correct environment (testnet vs mainnet)")
            print("4. Ensure your API key has the necessary permissions")
            print("5. Verify you're using the correct domain (https://eea.okx.com)")
        return False

if __name__ == "__main__":
    test_okx_connection()
