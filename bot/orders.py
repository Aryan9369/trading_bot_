import time
from binance.exceptions import BinanceAPIException, BinanceOrderException
from .logging_config import setup_logging

logger = setup_logging()

def place_order(client, symbol, side, order_type, quantity, price=None):
    """
    Executes an order and then fetches the updated execution status.
    """
    try:
        logger.info(f"Step 1: Sending {order_type} {side} order for {symbol}...")

        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = str(price)
            params["timeInForce"] = "GTC"

        # 1. Place the order
        initial_response = client.futures_create_order(**params)
        order_id = initial_response.get("orderId")
        
        logger.info(f"Step 2: Order {order_id} received. Fetching execution details...")

        # 2. Wait a brief moment for the matching engine to process
        time.sleep(0.5) 

        # 3. THE UPGRADE: Fetch the updated status
        updated_order = client.futures_get_order(
            symbol=symbol,
            orderId=order_id
        )
        
        logger.info(f"Step 3: Execution Complete. Status: {updated_order.get('status')}")
        return updated_order

    except Exception as e:
        logger.error(f"Order Placement Failed: {str(e)}")
        raise