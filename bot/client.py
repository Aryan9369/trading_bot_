import os
from binance.client import Client
from dotenv import load_dotenv


def get_client():
    # Load environment variables from .env
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("API keys not found. Please check your .env file.")

    # Initialize Binance client for Futures Testnet
    client = Client(api_key, api_secret, testnet=True)

    return client
