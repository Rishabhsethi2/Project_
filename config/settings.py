import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
REQUIRED_KEYS=["DHAN_CLIENT_ID","DHAN_ACCESS_TOKEN"]
for key in REQUIRED_KEYS:
    if os.getenv(key) is None:
        raise EnvironmentError(f"{key} not found!!")
