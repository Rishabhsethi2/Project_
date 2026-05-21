import os
import sys
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    print("--- RISHABH: CLOUD ENVIRONMENT VERIFICATION ---")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {sys.platform}")
    dhan_id = os.getenv('DHAN_CLIENT_ID')
    if dhan_id:
        print("Dhan API Secret: [CONFIGURED]")
    else:
        print("Dhan API Secret: [MISSING]")
    print("Status: System Ready for Phase 1 (May 8th)")
    print("---------------------------------------------")

if __name__ == "__main__":
    test_environment()