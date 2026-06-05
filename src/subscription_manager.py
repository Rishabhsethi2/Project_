# src/subscription_manager.py

import json
from config import get_active_watchlist
from logger import logger

def generate_subscription_payload():
    """
    Constructs the exact JSON payload required to tell the Dhan WebSocket 
    to start streaming live data for our selected symbols.
    """
    symbols_to_track = get_active_watchlist()
    
    # This is the standard subscription structure for institutional broker WebSockets
    payload = {
        "RequestCode": 15, # Code for "Subscribe"
        "InstrumentCount": len(symbols_to_track),
        "SymbolList": symbols_to_track
    }
    
    logger.info(f"📡 SUBSCRIPTION GENERATED | Tracking {len(symbols_to_track)} highly liquid assets.")
    
    # We use standard json here because this is sent ONCE at startup, not thousands of times a second.
    return json.dumps(payload)

if __name__ == "__main__":
    # Quick visual test to prove the payload generates correctly
    print("Testing Subscription Generator...")
    test_payload = generate_subscription_payload()
    print(f"Payload Output: \n{test_payload}")
    