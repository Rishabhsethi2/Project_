import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv

def verify_pipeline():
    print("\n--- Pipeline Dependency & Security Check ---")
    
    # 1. Verify Institutional Libraries
    print(f"Pandas Version: {pd.__version__}")
    print(f"NumPy Version: {np.__version__}")
    
    # 2. Verify the Security Vault (.env)
    load_dotenv()
    client_id = os.getenv("DHAN_CLIENT_ID")
    
    if client_id:
        print(f"Security: Vault Accessed. Client ID prefix: {client_id[:4]}***")
    else:
        print("Security: FATAL ERROR - Cannot read .env file.")
        
    print("Status: Ingestion Engine Ready.\n")

if __name__ == "__main__":
    verify_pipeline()