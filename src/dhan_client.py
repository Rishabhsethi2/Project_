import requests
import base64
import json
from dotenv import find_dotenv, dotenv_values

class DhanClient:
    def __init__(self):
        """Initializes the secure vault and decodes the JWT signature."""
        env_path = find_dotenv()
        vault = dotenv_values(env_path)
        
        raw_id = vault.get("DHAN_CLIENT_ID", "")
        raw_token = vault.get("DHAN_ACCESS_TOKEN", "")
        
        # NUCLEAR SANITIZATION: Strip all invisible characters and line breaks
        self.client_id = str(raw_id).replace(" ", "").replace("\n", "").replace("\r", "").strip().strip("'").strip('"')
        self.access_token = str(raw_token).replace(" ", "").replace("\n", "").replace("\r", "").strip().strip("'").strip('"')
        
        # --- CRYPTOGRAPHIC DECODER PROBE ---
        print("\n--- CRYPTOGRAPHIC IDENTITY SYNC ---")
        print(f"Vault Client ID: '{self.client_id}'")
        try:
            parts = self.access_token.split('.')
            if len(parts) >= 2:
                payload_b64 = parts[1]
                payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
                jwt_data = json.loads(base64.urlsafe_b64decode(payload_b64).decode('utf-8'))
                
                token_id = jwt_data.get('dhanClientId', 'UNKNOWN')
                print(f"Token Client ID: '{token_id}'")
                
                if self.client_id == token_id:
                    print("Analysis: Identity MATCH. (If this fails, the token was revoked).")
                else:
                    print("Analysis: CRITICAL MISMATCH. The Vault ID does not match the Token ID.")
        except Exception as e:
            print(f"Analysis: Failed to crack JWT payload: {e}")
        print("-----------------------------------\n")
        
        self.base_url = "https://api.dhan.co"

        if not self.client_id or not self.access_token:
            raise ValueError(f"FATAL: Python dictionary read failed. Vault keys found: {list(vault.keys())}")

    def _get_headers(self):
        """Constructs the institutional HTTP headers required by Dhan."""
        return {
            "client-id": self.client_id,
            "access-token": self.access_token,
            "Content-type": "application/json",
            "Accept": "application/json"
        }

    def verify_network_bridge(self):
        """Pings the Dhan servers to verify network egress from the container."""
        print("\n--- Initiating Brokerage Network Ping ---")
        url = f"{self.base_url}/fundlimit"
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            
            if response.status_code == 200:
                print("Status: Network Bridge Established. Live keys authenticated.")
            else:
                print(f"Unexpected Brokerage Response: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"CRITICAL: Network Egress Failed: {e}")

    def get_historical_data(self, security_id, from_date, to_date):
        """
        Fetches daily historical data for a given NSE Equity security.
        Dates must be in 'YYYY-MM-DD' format.
        """
        # CRITICAL FIX: The endpoint is exactly /charts/historical. 
        # (Removing the /v2/ prevents misrouting to the Order Engine).
        url = f"{self.base_url}/charts/historical"
        
        # Pure Equity Payload
        payload = {
            "securityId": str(security_id),
            "exchangeSegment": "NSE_EQ",
            "instrument": "EQUITY",
            "expiryCode": 0,
            "fromDate": from_date,
            "toDate": to_date
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload, timeout=10)
        
        print(f"[Telemetry] Brokerage HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                if not response.text.strip():
                    raise ValueError("Broker returned 200 OK, but the response body is completely empty.")
                return response.json()
            except ValueError as e:
                raise Exception(f"Ingestion Error: {e} | Raw Body: '{response.text}'")
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")