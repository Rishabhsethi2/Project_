import os
import sys
import csv
import pytest
from datetime import date

# This line forces Python to look inside your 'src' folder for the code
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from models import MarketTick
from data_pipeline import fallback_csv_dump
from logger import LOG_DIR

def test_telemetry_file_creation():
    """PROVES: The logger successfully creates the persistent system.log file."""
    log_file = os.path.join(LOG_DIR, "system.log")
    
    # Assert that the file actually exists on the hard drive
    assert os.path.exists(log_file), "FATAL: system.log was not created by the logger."

def test_csv_failsafe_execution():
    """PROVES: The fallback engine writes validated data to a CSV if the DB drops."""
    
    # 1. Create a fake MarketTick object (Mock Data)
    mock_tick = MarketTick(
        symbol="TEST_RELIANCE",
        trade_date=date(2026, 6, 5),
        open_price=1500.0,
        high_price=1510.0,
        low_price=1490.0,
        close_price=1505.0,
        volume=10000
    )
    
    # Define the emergency file path
    csv_file = "data/fallback_ticks.csv"
    
    # To ensure a clean test, delete the test file if it already exists from a previous run
    if os.path.exists(csv_file):
        os.remove(csv_file)
        
    # 2. TRIGGER THE FAIL-SAFE manually
    fallback_csv_dump([mock_tick])
    
    # 3. VERIFY: Did it create the file?
    assert os.path.exists(csv_file), "FATAL: CSV Fail-safe failed to create the file."
    
    # 4. VERIFY: Did it write the correct data?
    with open(csv_file, mode='r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Row 0 is the Header, Row 1 is our mock data
        assert len(rows) == 2, "FATAL: Incorrect number of rows written to CSV."
        assert rows[1][0] == "TEST_RELIANCE", "FATAL: Data corruption during CSV write."
        assert rows[1][5] == "1505.0", "FATAL: Close price corrupted during CSV write."

    # 5. Clean up the test file so it doesn't pollute production
    os.remove(csv_file)