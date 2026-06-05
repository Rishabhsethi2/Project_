from utils import epoch_ms_to_ist
import json
from pydantic import ValidationError
from logger import logger
from models import MarketTick

def validate_and_quarantine(raw_json_data):
    clean_ticks = []
    quarantined_ticks = []
    
    # State Tracker: Remembers the last known good price
    last_valid_close = None 

    for index, raw_tick in enumerate(raw_json_data):
        try:
            mapped_tick = {
                "symbol": raw_tick.get("symbol"),
                # Intercept the raw epoch and convert it to IST instantly
                "trade_date": epoch_ms_to_ist(raw_tick.get("date")) if isinstance(raw_tick.get("date"), int) else raw_tick.get("date"),
                "open_price": raw_tick.get("open"),
                "high_price": raw_tick.get("high"),
                "low_price": raw_tick.get("low"),
                "close_price": raw_tick.get("close"),
                "volume": raw_tick.get("volume")
            }
            # Step 1: Structural Defense (Pydantic)
            validated_tick = MarketTick(**mapped_tick)
            
            # Step 2: The Volume Filter (Drop useless heartbeat ticks)
            if getattr(validated_tick, 'volume', None) == 0:
                # We simply 'continue' to skip to the next tick. 
                # We do not log an error because this is expected market behavior.
                continue 
            
           # Step 2: Mathematical Defense (The Circuit Breaker)
            if last_valid_close is not None:
                # Calculate absolute percentage change
                price_change_pct = abs((validated_tick.close_price - last_valid_close) / last_valid_close)
                
                if price_change_pct > 0.05: # The 5% Threshold
                    logger.critical(f"⚡ CIRCUIT BREAKER TRIPPED | Tick Index [{index}] | {price_change_pct:.2%} price spike detected. Quarantining False Trade.")
                    quarantined_ticks.append(raw_tick)
                    continue # Skip to the next tick, do not update last_valid_close!

            # If it passes both defenses, lock it in
            clean_ticks.append(validated_tick)
            
            # Update the state tracker for the next loop
            last_valid_close = validated_tick.close_price
            
        except ValidationError as e:
            error_details = e.errors()[0]
            field = error_details.get('loc', ['Unknown'])[0]
            msg = error_details.get('msg', 'Unknown error')
            logger.warning(f"🛡️ MALFORMED DATA CAUGHT | Tick Index [{index}] | Field: '{field}' -> {msg}")
            quarantined_ticks.append(raw_tick)
            
        except Exception as e:
            logger.warning(f"🛡️ SEVERE DATA CORRUPTION | Tick Index [{index}] | Error: {e}")
            quarantined_ticks.append(raw_tick)

    logger.info(f"Validation Complete: {len(clean_ticks)} Clean | {len(quarantined_ticks)} Quarantined.")
    return clean_ticks