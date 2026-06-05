import asyncpg
import asyncio
from logger import logger

DB_CONFIG = {
    "user": "quant_user",
    "password": "quant_password",
    "database": "quant_db",
    "host": "host.docker.internal",
    "port": "5432"
}

class DatabasePool:
    def __init__(self):
        self.pool = None

    async def initialize(self):
        """Spins up a persistent pool of connections to PostgreSQL."""
        try:
            self.pool = await asyncpg.create_pool(
                **DB_CONFIG,
                min_size=5,   # Keep 5 connections permanently open
                max_size=20,  # Scale up to 20 during extreme market volatility
                command_timeout=60
            )
            logger.info("🟢 asyncpg Connection Pool Initialized. Ready for high-speed ingestion.")
        except Exception as e:
            logger.critical(f"FATAL: Failed to initialize asyncpg pool: {e}")

    async def close(self):
        """Gracefully closes all connections during system shutdown."""
        if self.pool:
            await self.pool.close()
            logger.info("🔴 asyncpg Connection Pool Closed.")

# Create a global instance to be imported by other modules
db = DatabasePool()

# --- Quick Test Block ---
async def test_pool():
    await db.initialize()
    # If the pool initialized correctly, we can borrow a connection to run a simple test query
    if db.pool:
        async with db.pool.acquire() as conn:
            result = await conn.fetchval("SELECT version();")
            print(f"\n✅ Connected via asyncpg! Database Engine: {result[:40]}...\n")
    await db.close()

if __name__ == "__main__":
    # Standard way to run an async function in Python
    asyncio.run(test_pool())