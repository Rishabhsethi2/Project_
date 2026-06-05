from datetime import datetime
from zoneinfo import ZoneInfo
from logger import logger

# Hardcode the IST timezone object once so we don't recreate it millions of times
IST_ZONE = ZoneInfo("Asia/Kolkata")

def epoch_ms_to_ist(epoch_ms: int) -> datetime:
    """
    Lightning-fast conversion of a 13-digit epoch millisecond integer 
    into an IST-aware Python datetime object.
    """
    try:
        # Convert milliseconds to seconds (float)
        epoch_sec = epoch_ms / 1000.0
        
        # Generate the datetime object natively in IST
        ist_time = datetime.fromtimestamp(epoch_sec, tz=IST_ZONE)
        return ist_time
    except Exception as e:
        logger.error(f"Time Conversion Error for epoch {epoch_ms}: {e}")
        return None