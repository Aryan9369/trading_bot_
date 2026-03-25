import argparse
import sys
from bot.client import get_binance_client
from bot.validators import validate_order_inputs
from bot.orders import place_order
from bot.logging_config import setup_logging

# Initialize Logger
logger = setup_logging()

def main():
    # Setup CLI Argument Parser with a cleaner description
    parser = argparse.ArgumentParser(
        description="🚀 Trading Bot CLI - Binance Futures Testnet (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, help="Order side (BUY/SELL)")
    parser.add_argument("--type", type=str, required=True, help="Order type (MARKET/LIMIT)")
    parser.add_argument("--quantity", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Target price (Required only for LIMIT orders)")

    args = parser.parse_args()

    try:
        # 1. Validate User Inputs
        valid_data = validate_order_inputs(
            args.symbol, args.side, args.type, args.quantity, args.price
        )

        # 2. Initialize the Binance Client
        client = get_binance_client()

        # 3. Print Request Header (UX Improvement)
        print("\n" + "═" * 45)
        print(" 🛰️  ESTABLISHING ORDER REQUEST")
        print("═" * 45)
        print(f" Symbol:    {valid_data['symbol']}")
        print(f" Side:      {valid_data['side']}")
        print(f" Type:      {valid_data['type']}")
        print(f" Quantity:  {valid_data['quantity']}")
        if valid_data['price']:
            print(f" Price:     {valid_data['price']}")
        print("═" * 45 + "\n")

        # 4. Place Order and Fetch Updated Execution Details
        # This function now includes the professional 'poll-for-update' logic
        response = place_order(
            client, 
            valid_data['symbol'], 
            valid_data['side'], 
            valid_data['type'], 
            valid_data['quantity'], 
            valid_data['price']
        )

        # 5. Extract Execution Details
        order_id = response.get('orderId')
        status = response.get('status')
        exe_qty = float(response.get('executedQty', 0))
        req_qty = float(valid_data['quantity'])
        avg_price = response.get('avgPrice', '0.00')

        # Logic: Calculate Fill Percentage
        fill_pct = (exe_qty / req_qty) * 100 if req_qty > 0 else 0

        # 6. Final Professional Execution Summary
        print(" ✅ ORDER EXECUTED SUCCESSFULLY")
        print("─" * 45)
        print(f" Order ID:       {order_id}")
        print(f" Final Status:   {status}")
        print(f" Avg Fill Price: {avg_price} USDT")
        print(f" Executed Qty:   {exe_qty} / {req_qty}")
        
        # ASCII Progress Bar for Fill Percentage
        bar_length = 20
        filled_blocks = int(round(bar_length * fill_pct / 100))
        bar = "█" * filled_blocks + "-" * (bar_length - filled_blocks)
        print(f" Fill Progress:  [{bar}] {fill_pct:.1f}%")
        
        print("─" * 45 + "\n")

    except ValueError as ve:
        logger.error(f"Input Validation Error: {ve}")
        print(f" ❌ INPUT ERROR: {ve}")
        sys.exit(1)
    except ConnectionError as ce:
        logger.error(f"Authentication/Connection Error: {ce}")
        print(f" ❌ CONNECTION ERROR: {ce}")
        sys.exit(1)
    except Exception as e:
        # Errors from Binance API are already logged in orders.py
        print(f" ❌ EXECUTION FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()