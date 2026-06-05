import orjson
from logger import logger
from validator import validate_and_quarantine

def on_message(raw_ws_message):
    """
    Lightning-fast parser for live WebSocket ticks.
    Catches raw network bytes and converts them using C-optimized orjson.
    """
    try:
        # WebSockets naturally transmit data as raw bytes. 
        # orjson is natively optimized to read bytes directly without decoding to strings first!
        parsed_data = orjson.loads(raw_ws_message)
        
        # Dhan might send a single tick, or a batch inside a 'data' array.
        # We normalize everything into a list so our validator can process it seamlessly.
        if isinstance(parsed_data, dict):
            if "data" in parsed_data:
                ticks_to_process = parsed_data["data"]
            else:
                ticks_to_process = [parsed_data]
        elif isinstance(parsed_data, list):
            ticks_to_process = parsed_data
        else:
            logger.error("Unrecognized WebSocket payload format. Dropping frame.")
            return []

        # Push the lightning-fast parsed data straight into your defensive grid
        clean_ticks = validate_and_quarantine(ticks_to_process)
        
        # In the next sprint, we will route these clean ticks to the PostgreSQL Bulk Insert Buffer
        return clean_ticks

    except orjson.JSONDecodeError as e:
        logger.error(f"⚡ FRAME DROPPED | Failed to parse raw WebSocket bytes: {e}")
        return []
    except Exception as e:
        logger.critical(f"FATAL ERROR in Stream Parser: {e}")
        return []