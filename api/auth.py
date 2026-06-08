import pyotp
import requests
import os
from dotenv import load_dotenv
from api.security import encrypt_access_token

def establish_live_session():
    load_dotenv()
    b_URL = "https://auth.dhan.co"
    endpoint = "/app/generateAccessToken"
    url = b_URL + endpoint
    load = {'dhanClientId': os.getenv("DHAN_CLIENT_ID") ,'pin': os.getenv("DHAN_PIN") ,'totp': generate_totp(os.getenv("DHAN_SECRET_KEY")) }
    # print(load)
    # response = requests.post(url,data = load)
    # print(response.json())
    # return response.json()
    # encrypt_access_token(response.json().get("accessToken"))
    encrypt_access_token("Yashika")

def generate_totp(secret_key: str) -> str:
    totp = pyotp.TOTP(secret_key)
    return totp.now()

#test
if __name__=="__main__":
    load_dotenv()
    sk = os.getenv("DHAN_SECRET_KEY")
    a = generate_totp(sk)
    print(a)
    establish_live_session()
