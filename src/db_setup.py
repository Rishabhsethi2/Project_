import psycopg2
from logger import logger

# Using the local Docker credentials we mapped in the compose file
DB_CONFIG = {
    "dbname": "quant_db",
    "user": "quant_user",
    "password": "quant_password",
    "host": "host.docker.internal", # Reaching out to the host network mapping
    "port": "5432"
}

def init_database():
    """
    Connects to the PostgreSQL container and builds the time-series optimized schema.
    """
    logger.info("Connecting to PostgreSQL to initialize schema...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # Enable autocommit so we don't have to manually run conn.commit() for table creation
        conn.autocommit = True
        cursor = conn.cursor()

        # 1. Create the Ticks Table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ticks (
            id BIGSERIAL PRIMARY KEY,
            symbol VARCHAR(20) NOT NULL,
            trade_time TIMESTAMPTZ NOT NULL,
            open_price DOUBLE PRECISION NOT NULL,
            high_price DOUBLE PRECISION NOT NULL,
            low_price DOUBLE PRECISION NOT NULL,
            close_price DOUBLE PRECISION NOT NULL,
            volume INTEGER NOT NULL
        );
        """
        cursor.execute(create_table_query)
        logger.info("✅ Table 'ticks' created (or already exists).")

        # 2. Build the Composite B-Tree Index for Lightning-Fast ML Queries
        create_index_query = """
        CREATE INDEX IF NOT EXISTS idx_symbol_time 
        ON ticks (symbol, trade_time DESC);
        """
        cursor.execute(create_index_query)
        logger.info("⚡ Time-Series Composite Index created.")

        cursor.close()
        conn.close()
        logger.info("Database Initialization Complete.")

    except psycopg2.Error as e:
        logger.critical(f"FATAL DATABASE ERROR: {e}")

if __name__ == "__main__":
    init_database()