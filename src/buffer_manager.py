import asyncio
from ingestion import bulk_insert_ticks
from logger import logger
from models import MarketTick
from db_pool import db

class TickBuffer:
    def __init__(self, batch_size=50):
        self.buffer = []
        self.batch_size = batch_size
        self.lock = asyncio.Lock() # Prevents data corruption if multiple ticks arrive simultaneously

    async def add_tick(self, tick: MarketTick):
        """
        Adds a single tick to the buffer. 
        If the buffer reaches the batch size, it flushes automatically.
        """
        async with self.lock:
            self.buffer.append(tick)
            
            # Check if it's time to flush
            if len(self.buffer) >= self.batch_size:
                await self.flush()

    async def flush(self):
        """
        Safely extracts all ticks, clears the holding area, 
        and sends them to the database in a non-blocking background task.
        """
        if not self.buffer:
            return
            
        # Duplicate the data so we can clear the main buffer instantly
        ticks_to_insert = self.buffer[:]
        self.buffer.clear()
        
        # Fire the bulk insert in the background (fire-and-forget)
        # This is critical: It means the WebSocket doesn't have to wait for the DB!
        asyncio.create_task(bulk_insert_ticks(ticks_to_insert))
        logger.info(f"🌊 BUFFER FLUSHED: {len(ticks_to_insert)} ticks sent to async ingestion.")

# --- Quick Test Block ---
async def test_buffer():
    from utils import epoch_ms_to_ist
    await db.initialize()
    
    # Initialize a buffer that flushes every 50 ticks
    stream_buffer = TickBuffer(batch_size=50)
    
    print("Simulating high-speed WebSocket stream of 120 ticks...")
    base_epoch = 1717571625000
    
    for i in range(120):
        mock_tick = MarketTick(
            symbol="RELIANCE.NS",
            trade_date=epoch_ms_to_ist(base_epoch + i),
            open_price=1500.0,
            high_price=1510.0,
            low_price=1490.0,
            close_price=1500.5,
            volume=500
        )
        # Add ticks one-by-one, exactly how the live WebSocket will do it
        await stream_buffer.add_tick(mock_tick)
    
    # We pushed 120 ticks. We expect 2 flushes of 50, leaving 20 stranded in the buffer.
    # We must manually flush the remainder (useful for End-of-Day shutdown).
    print(f"Ticks left in buffer before manual flush: {len(stream_buffer.buffer)}")
    await stream_buffer.flush()
    
    # Give the background tasks a fraction of a second to finish saving to the DB
    await asyncio.sleep(1)
    await db.close()

if __name__ == "__main__":
    asyncio.run(test_buffer())