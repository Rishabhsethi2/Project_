import asyncio
import websockets 
import json
import os
import sys 
from dotenv import load_dotenv
from api.security import *


load_dotenv()

CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
ACCESS_TOKEN = decrypt_access_token()

if not CLIENT_ID or not ACCESS_TOKEN:
    sys.exit("Details not found")

async def main():
    print("Inside main")

if __name__=="__main__":
    asyncio.run(main())
