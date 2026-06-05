# src/config.py

"""
Global Configuration & Trading Watchlists
"""

# The Dhan API usually requires an exchange prefix or specific format. 
# We will use the standard NSE format we established in our Mock API.
NIFTY_50_SYMBOLS = [
    "RELIANCE.NS",    # Reliance Industries
    "HDFCBANK.NS",    # HDFC Bank
    "ICICIBANK.NS",   # ICICI Bank
    "INFY.NS",        # Infosys
    "ITC.NS",         # ITC
    "TCS.NS",         # Tata Consultancy Services
    "LT.NS",          # Larsen & Toubro
    "AXISBANK.NS",    # Axis Bank
    "KOTAKBANK.NS",   # Kotak Mahindra Bank
    "SBIN.NS"         # State Bank of India
]

def get_active_watchlist():
    """Returns the current active list of symbols for the WebSocket to track."""
    return NIFTY_50_SYMBOLS