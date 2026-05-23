import requests
from dotenv import find_dotenv, dotenv_values

class DhanClient:
    def __init__(self):
        """Initializes the secure vault bypassing OS-level restrictions."""
        env_path = find_dotenv()
        
        # We bypass load_dotenv() and os.getenv() entirely.
        # We read the file directly into a Python dictionary.
        vault = dotenv_values(env_path)
        
        self.client_id = vault.get("DHAN_CLIENT_ID")
        self.access_token = vault.get("DHAN_ACCESS_TOKEN")
        self.base_url = "https://api.dhan.co"

        # Hard stop verification
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
        print(f"Target Egress URL: {url}")
        
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            print(f"HTTP Status Code: {response.status_code}")
            
            if response.status_code == 401:
                print("Status: Network Bridge Established. (401 Expected due to truncated token).")
            elif response.status_code == 200:
                print("Status: Network Bridge Established. Live keys authenticated.")
            else:
                print(f"Unexpected Brokerage Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"CRITICAL: Network Egress Failed: {e}")

if __name__ == "__main__":
    client = DhanClient()
    client.verify_network_bridge()