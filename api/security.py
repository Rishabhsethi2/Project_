from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

def encrypt_access_token(token : str):
    load_dotenv()
    key = Fernet(os.getenv("ENCRYPTION_KEY"))
    encrypted_data = key.encrypt(token.encode())
    file_path = os.path.join(os.getenv("ROOT_FOLDER_PROJECT_"),".cache","dhan_token.enc")
    with open(file_path,"wb") as f:
        f.write(encrypted_data)
    print("Data written successfully")

def decrypt_access_token() -> str:
    load_dotenv()
    file_path = os.path.join(os.getenv("ROOT_FOLDER_PROJECT_"),".cache","dhan_token.enc")
    with open(file_path,"rb") as f:
        enc_data = f.read()
    key = Fernet(os.getenv("ENCRYPTION_KEY"))
    decrypted_data = key.decrypt(enc_data).decode()
    return decrypted_data

if __name__=="__main__":
    encrypt_access_token("Rishabh")
    token = decrypt_access_token()
    print(token)
