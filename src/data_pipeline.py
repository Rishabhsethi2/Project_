import yfinance as yf
import pandas as pd
import requests
import os
import csv
from models import MarketTick
from database import save_ticks_to_db
from logger import logger  # Injecting our new telemetry engine

def fallback_csv_dump(validated_ticks):
    """CSV Fail-safe: Dumps data locally if Postgres is unreachable."""
    os.makedirs("data", exist_ok=True)
    csv_file = "data/fallback_ticks.csv"
    
    logger.warning(f"Triggering CSV Fail-safe. Writing {len(validated_ticks)} records to {csv_file}")
    
    file_exists = os.path.isfile(csv_file)
    
    try:
        with open(csv_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            # Write header if creating a new file
            if not file_exists:
                writer.writerow(MarketTick.model_fields.keys())
            
            # Write the Pydantic data rows
            for tick in validated_ticks:
                writer.writerow([getattr(tick, field) for field in MarketTick.model_fields.keys()])
        logger.info("CSV Fail-safe execution successful. Data secured on local disk.")
    except Exception as e:
        logger.critical(f"FATAL: CSV Fail-safe also failed: {e}")

def fetch_and_validate_data():
    logger.info("Initiating Quant Data Pipeline...")
    symbol = "RELIANCE.NS"
    
    try:
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        logger.info(f"Extracting Yahoo Finance data for {symbol}")
        df = yf.download(symbol, start="2026-05-01", end="2026-05-20", session=session)
        
        if df.empty:
            logger.warning("No data found for the given date range.")
            return

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel('Ticker')
        df = df.reset_index()
        
        validated_ticks = []
        for index, row in df.iterrows():
            try:
                tick = MarketTick(
                    symbol=symbol,
                    trade_date=row['Date'].date(),
                    open_price=float(row['Open']),
                    high_price=float(row['High']),
                    low_price=float(row['Low']),
                    close_price=float(row['Close']),
                    volume=int(row['Volume'])
                )
                validated_ticks.append(tick)
            except Exception as ve:
                logger.error(f"Validation Error on {row['Date']}: {ve}")
                
        logger.info(f"{len(validated_ticks)} records successfully validated against MarketTick Contract.")
        
        # --- THE RESILIENCE FORK ---
        try:
            logger.info("Attempting to save to PostgreSQL...")
            save_ticks_to_db(validated_ticks)
            logger.info("Database insertion successful.")
        except Exception as db_err:
            logger.error(f"Database network drop detected: {db_err}")
            # Trigger the fail-safe immediately
            fallback_csv_dump(validated_ticks)
            
    except Exception as e:
        logger.critical(f"Pipeline Failed: {e}", exc_info=True)

if __name__ == "__main__":
    fetch_and_validate_data()