import json
from pydantic import ValidationError
from logger import logger
from models import MarketTick

def validate_and_quarantine(raw_json_data):
    """
    Parses a list of raw API dictionaries. 
    Returns a list of validated MarketTick objects and logs any malformed data.
    """
    clean_ticks = []
    quarantined_ticks = []

    for index, raw_tick in enumerate(raw_json_data):
        try:
            # Attempt to map the Dhan API keys to our internal Data Contract
            # (Adjust these dictionary keys if your MarketTick model expects different names)
            mapped_tick = {
                "symbol": raw_tick.get("symbol"),
                "trade_date": raw_tick.get("date"),
                "open_price": raw_tick.get("open"),
                "high_price": raw_tick.get("high"),
                "low_price": raw_tick.get("low"),
                "close_price": raw_tick.get("close"),
                "volume": raw_tick.get("volume")
            }
            
            # Pydantic validates the types mathematically here
            validated_tick = MarketTick(**mapped_tick)
            clean_ticks.append(validated_tick)
            
        except ValidationError as e:
            # If Pydantic catches a bad type or missing field, it throws a ValidationError
            error_details = e.errors()[0]
            field = error_details.get('loc', ['Unknown'])[0]
            msg = error_details.get('msg', 'Unknown error')
            
            logger.warning(f"🛡️ MALFORMED DATA CAUGHT | Tick Index [{index}] | Field: '{field}' -> {msg}")
            quarantined_ticks.append(raw_tick)
            
        except Exception as e:
            # Catch-all for extreme structural corruption
            logger.warning(f"🛡️ SEVERE DATA CORRUPTION | Tick Index [{index}] | Error: {e}")
            quarantined_ticks.append(raw_tick)

    # Log the final batch summary
    logger.info(f"Validation Complete: {len(clean_ticks)} Clean | {len(quarantined_ticks)} Quarantined.")
    
    return clean_ticks