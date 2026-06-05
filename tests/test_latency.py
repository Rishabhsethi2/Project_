import os
import sys
import time
import orjson

# Ensure Python can find the src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from stream_parser import on_message

def run_stress_test():
    total_ticks = 10000
    print(f"⚙️ Generating {total_ticks} synthetic ticks for stress test...")
    
    # 1. Generate massive synthetic payload
    mock_ticks = []
    base_epoch = 1717571625000  # Base timestamp
    
    for i in range(total_ticks):
        mock_ticks.append({
            "symbol": "RELIANCE.NS",
            "date": base_epoch + i, # Increment time by 1ms per tick
            "open": 1500.0,
            "high": 1510.0,
            "low": 1490.0,
            "close": 1500.0 + (i % 10), # Slight price variance to avoid circuit breaker
            "volume": 1000 # Non-zero volume so it passes the filter
        })

    # 2. Compress into raw bytes exactly like a WebSocket transmission
    raw_payload = orjson.dumps({"data": mock_ticks})
    payload_size_kb = len(raw_payload) / 1024
    
    print(f"📦 Payload Size: {payload_size_kb:.2f} KB of raw byte data.")
    print("🔥 FIRING PAYLOAD INTO GATEWAY...\n")

    # --- START HIGH-PRECISION TIMER ---
    start_time = time.perf_counter()

    # 3. Push through the high-frequency parser and the entire defense grid
    processed_ticks = on_message(raw_payload)

    # --- STOP HIGH-PRECISION TIMER ---
    end_time = time.perf_counter()

    # 4. Calculate Latency Metrics
    total_time_ms = (end_time - start_time) * 1000
    avg_tick_ms = total_time_ms / total_ticks

    # 5. Output Results
    print("==================================================")
    print(f"✅ Processed {len(processed_ticks)} clean ticks successfully.")
    print(f"⏱️ Total Batch Execution Time: {total_time_ms:.2f} ms")
    print(f"⚡ Average Latency Per Tick: {avg_tick_ms:.4f} ms")
    print("==================================================")

    if avg_tick_ms < 2.0:
        print("\n🟢 PERFORMANCE PASS: System is operating well under the 2.0ms threshold!")
        print("Your gateway is ready for live institutional data streams.")
    else:
        print("\n🔴 PERFORMANCE FAIL: System is too slow for high-frequency trading.")

if __name__ == "__main__":
    run_stress_test()