import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

def get_binance_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API keys not found. Check your .env file.")

    client = Client(api_key, api_secret, testnet=True)
    return client
