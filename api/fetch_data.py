import requests
import os
from dotenv import load_dotenv
from api.security import *

def get_fund_summary(token: str):
    b_URL = "https://api.dhan.co"
    endpoint = "/v2/fundlimit"
    URL = b_URL+endpoint
    headers = {
        'Content-Type':'application/json',
        'access-token': token
    }
    response = requests.get(URL,headers = headers)
    # # print(headers)
    print(response.json())
    print(response.status_code)

if __name__=="__main__":
    get_fund_summary(decrypt_access_token())
    # pass