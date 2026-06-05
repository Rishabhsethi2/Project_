import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class MockDhanBroker(BaseHTTPRequestHandler):
    # Suppress default server logging to keep the terminal clean
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        """Intercepts GET requests and returns fake market data."""
        
        # Route 1: The Health Check (To prove the server is online)
        if self.path == '/ping':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "online", "broker": "Mock Dhan API"}).encode('utf-8'))
            
        # Route 2: The Data Endpoint (Simulating the historical data pull)
        elif self.path == '/charts/historical':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # The Exact JSON structure the Dhan API returns
            # The Exact JSON structure the Dhan API returns (Plus one corrupted tick!)
            mock_payload = {
                "status": "success",
                "remarks": "Mock data generated locally",
                "data": [
                    {
                        "symbol": "RELIANCE.NS",
                        "date": "2026-06-05",
                        "open": 1500.50,
                        "high": 1515.00,
                        "low": 1495.25,
                        "close": 1510.75,
                        "volume": 250400
                    },
                    {
                        "symbol": "RELIANCE.NS",
                        "date": "2026-06-04",
                        "open": 1490.00,
                        "high": 1505.50,
                        "low": 1485.00,
                        "close": 1500.50,
                        "volume": 198000
                    },
                    # 🚨 THE MALFORMED TICK 🚨
                    {
                        "symbol": "RELIANCE.NS",
                        "date": "2026-06-03",
                        "open": 1480.00,
                        "high": "ERROR",  # Wrong data type! Should be float.
                        "low": 1475.00,
                        "close": 1485.00
                        # Missing 'volume' key entirely!
                    },
                    {
                        "symbol": "RELIANCE.NS",
                        "date": "2026-06-02",
                        "open": 1600.00,
                        "high": 1650.00,
                        "low": 1600.00,
                        "close": 1633.50, # Massive jump from ~1485!
                        "volume": 300000
                    }
                ]
            }
            self.wfile.write(json.dumps(mock_payload).encode('utf-8'))
            print(f"📡 [MOCK API] Served 2 market ticks to local client.")
            
        # Route 3: Handle bad URLs
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))

def run_mock_server():
    port = 8085
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockDhanBroker)
    print(f"\n🟢 Mock Dhan API Online.")
    print(f"Listening on http://localhost:{port}")
    print("Press Ctrl+C to shut down.\n-----------------------------------")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🔴 Mock API Shutting Down.")
        httpd.server_close()

if __name__ == '__main__':
    run_mock_server()