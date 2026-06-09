import pyotp
import requests
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import time

def establish_live_session():
    # print("Inside establish_live_session")
    load_dotenv()
    b_URL = "https://auth.dhan.co"
    endpoint = "/app/generateAccessToken"
    url = b_URL + endpoint
    load = {'dhanClientId': os.getenv("DHAN_CLIENT_ID") ,'pin': os.getenv("DHAN_PIN") ,'totp': generate_totp(os.getenv("DHAN_SECRET_KEY")) }
    # print(load)
    # print("Sending new api request..")
    response = requests.post(url,data = load)
    # print(response.json())
    # return response.json()

    #Encrypting the token key and saving in cache
    fetched_data = response.json()
    key = Fernet(os.getenv("ENCRYPTION_KEY"))
    encrypted_data = key.encrypt(fetched_data.get("accessToken").encode())
    file_path = os.path.join(os.getenv("ROOT_FOLDER_PROJECT_"),".cache","dhan_token.enc")
    with open(file_path,"wb") as f:
        f.write(encrypted_data)
    print(f"Data written successfully at {time.time()}")


def generate_totp(secret_key: str) -> str:
    totp = pyotp.TOTP(secret_key)
    return totp.now()

#test
if __name__=="__main__":
    # load_dotenv()
    # sk = os.getenv("DHAN_SECRET_KEY")
    # a = generate_totp(sk)
    # print(a)
    establish_live_session()
