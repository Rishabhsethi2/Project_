import psutil
import time
import threading
from logger import logger

def _heartbeat_loop(interval_seconds):
    """The infinite loop that measures system vitals."""
    while True:
        try:
            # Measure CPU and RAM
            cpu_usage = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            
            # Format RAM to Gigabytes
            ram_used_gb = ram.used / (1024 ** 3)
            ram_total_gb = ram.total / (1024 ** 3)
            
            logger.info(
                f"❤️ SYSTEM HEARTBEAT | CPU: {cpu_usage}% | "
                f"RAM: {ram.percent}% ({ram_used_gb:.2f}GB / {ram_total_gb:.2f}GB)"
            )
        except Exception as e:
            logger.error(f"Heartbeat telemetry failed: {e}")
            
        # Sleep until the next tick
        time.sleep(interval_seconds)

def start_heartbeat(interval_seconds=600):
    """Spins up the heartbeat loop on a background thread."""
    thread = threading.Thread(target=_heartbeat_loop, args=(interval_seconds,), daemon=True)
    thread.start()
    logger.info(f"System Heartbeat initialized. Ticking every {interval_seconds} seconds.")