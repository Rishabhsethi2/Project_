import asyncio
from datetime import datetime
from db_pool import db
from logger import logger
from models import MarketTick

async def bulk_insert_ticks(ticks: list[MarketTick]):
    """
    Takes a list of validated MarketTick Pydantic objects and bulk-inserts 
    them into the PostgreSQL database in a single network transaction.
    """
    if not ticks:
        return

    # 1. Convert Pydantic objects into raw tuples for the database driver
    # The order of these variables MUST perfectly match the SQL $1, $2, $3 variables below
    records = [
        (
            t.symbol,
            t.trade_date,
            t.open_price,
            t.high_price,
            t.low_price,
            t.close_price,
            t.volume
        )
        for t in ticks
    ]

    # 2. The Bulk SQL Query
    query = """
    INSERT INTO ticks (symbol, trade_time, open_price, high_price, low_price, close_price, volume)
    VALUES ($1, $2, $3, $4, $5, $6, $7)
    """

    # 3. Fire the Payload
    try:
        # Borrow a connection from the async pool we built yesterday
        async with db.pool.acquire() as conn:
            # executemany is the high-speed C-optimized bulk insert function
            await conn.executemany(query, records)
            logger.info(f"💾 BULK INSERT: Successfully saved {len(records)} ticks to database.")
            
    except Exception as e:
        logger.error(f"❌ DB INSERT FAILED: {e}")
        # Note: In the future, this is exactly where we will trigger the 
        # CSV Fail-safe (Day 12) if the database goes down!

# --- Quick Test Block ---
async def test_bulk_insert():
    from utils import epoch_ms_to_ist
    
    # 1. Boot up the connection pool
    await db.initialize()
    
    print("Generating synthetic batch of 1,000 ticks for DB insertion...")
    
    # 2. Generate 1,000 clean Pydantic ticks
    mock_ticks = []
    base_epoch = 1717571625000
    for i in range(1000):
        mock_ticks.append(MarketTick(
            symbol="RELIANCE.NS",
            trade_date=epoch_ms_to_ist(base_epoch + i),
            open_price=1500.0,
            high_price=1510.0,
            low_price=1490.0,
            close_price=1500.5,
            volume=500
        ))
        
    # 3. Fire them into the database
    await bulk_insert_ticks(mock_ticks)
    
    # 4. Shut down the pool
    await db.close()

if __name__ == "__main__":
    asyncio.run(test_bulk_insert())