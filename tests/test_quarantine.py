import requests
import sys
import os

# Ensure Python can find the src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from validator import validate_and_quarantine

def run_quarantine_test():
    print("Fetching data from Mock Dhan API...")
    try:
        # Hitting the new secure port
        response = requests.get("http://host.docker.internal:8085/charts/historical")
        
        # Safety Check: Print exactly what the server returned!
        if response.status_code != 200 or not response.text.strip():
            print(f"CRITICAL HTTP ERROR: Server returned Status {response.status_code}")
            print(f"RAW SERVER RESPONSE: '{response.text}'")
            return
            
        raw_data = response.json().get("data", [])
        print(f"Received {len(raw_data)} total ticks. Pushing through Quarantine Engine...\n")
        
        clean_data = validate_and_quarantine(raw_data)
        print(f"\nFinal output ready for database insertion: {len(clean_data)} ticks.")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Mock API is not running. Please start it on Port 8085 first.")
if __name__ == "__main__":
    run_quarantine_test()
