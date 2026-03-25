import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

def get_binance_client():
    """
    Initializes the Binance Client for Futures Testnet.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ConnectionError("API Key and Secret must be set in .env file.")

    # Initialize client with testnet=True
    client = Client(api_key, api_secret, testnet=True)
    return client