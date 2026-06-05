import logging
import os
import requests
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv, find_dotenv

# Ensure environment variables are loaded to read the Webhook URL
load_dotenv(find_dotenv())

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Pull the Webhook URL from the secure vault
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

class DiscordWebhookHandler(logging.Handler):
    """Custom handler that intercepts high-severity logs and pushes them to Discord."""
    def emit(self, record):
        # If no URL is configured, quietly skip
        if not WEBHOOK_URL or WEBHOOK_URL.startswith("your_"):
            return
            
        log_entry = self.format(record)
        
        # Color coding: Red for CRITICAL, Orange for ERROR
        color = 16711680 if record.levelno == logging.CRITICAL else 16753920
        
        payload = {
            "username": "Quant Pipeline Alert",
            "embeds": [{
                "title": f"🚨 SYSTEM {record.levelname} 🚨",
                "description": f"**Module:** `{record.module}.py`\n**Line:** `{record.lineno}`\n\n**Details:**\n```{log_entry}```",
                "color": color
            }]
        }
        
        try:
            # Fire and forget. Timeout set to 2s so a slow Discord API doesn't hang our trading loop.
            requests.post(WEBHOOK_URL, json=payload, timeout=2)
        except Exception:
            # NEVER let a webhook failure crash the main application
            pass

def setup_logger(name="quant_pipeline"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    standard_formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s')
    webhook_formatter = logging.Formatter('%(message)s')

    # 1. Console Handler (Terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(standard_formatter)

    # 2. Rotating File Handler (Disk)
    log_file = os.path.join(LOG_DIR, "system.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(standard_formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        # 3. Discord Webhook Handler (STRICTLY for Errors and Criticals)
        discord_handler = DiscordWebhookHandler()
        discord_handler.setLevel(logging.ERROR) 
        discord_handler.setFormatter(webhook_formatter)
        logger.addHandler(discord_handler)

    return logger

logger = setup_logger()