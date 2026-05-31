from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    f = Fernet(key)
    with open("secret.keys","wb") as key_file:
        key_file.write(key)
    return f

def encrypt_data(text,key):
    enc_data= key.encrypt(text)
    print(enc_data.decode())
    return enc_data
    
def decrypt_data(ciphertext,key):
    dec_data= key.decrypt(ciphertext)
    print(dec_data.decode())

if __name__ == "__main__":
    key= generate_key()
    enc=encrypt_data(input("Enter data:").encode(),key)
    decrypt_data(enc,key)