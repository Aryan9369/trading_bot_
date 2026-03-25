def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    
    #Validates CLI inputs before sending to Binance
    #Validate Side
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")

    #Validate Type
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError(f"Invalid type: {order_type}. Must be MARKET or LIMIT.")

    #Validate Quantity
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    #Validate Price for LIMIT orders
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")
    
    #Symbol formatting
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., BTCUSDT).")

    return {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
        "price": price
    }
