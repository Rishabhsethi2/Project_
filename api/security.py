from cryptography.fernet import Fernet
from dotenv import load_dotenv
from api.auth import establish_live_session
import os
import time

def is_token_valid(path: str) -> bool:
    generation_time = os.path.getmtime(path)
    current_time = time.time()
    if (current_time - generation_time)>=86400:
        return False
    else:
        return True

def encrypt_access_token(token : str):
    load_dotenv()
    

def decrypt_access_token() -> str:
    load_dotenv()
    file_path = os.path.join(os.getenv("ROOT_FOLDER_PROJECT_"),".cache","dhan_token.enc")
    if is_token_valid(file_path):
        with open(file_path,"rb") as f:
            enc_data = f.read()
        key = Fernet(os.getenv("ENCRYPTION_KEY"))
        decrypted_data = key.decrypt(enc_data).decode()
        return decrypted_data
    else:
        # print("token expired...regenerating token..")
        establish_live_session()
        # print("regeneration successful")
        with open(file_path,"rb") as f:
            enc_data = f.read()
        key = Fernet(os.getenv("ENCRYPTION_KEY"))
        decrypted_data = key.decrypt(enc_data).decode()
        return decrypted_data

if __name__=="__main__":
    # encrypt_access_token("Rishabh")
    # token = decrypt_access_token()
    # print(token)
    pass
