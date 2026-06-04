import pyotp

def generate_totp(secret_key: str) -> str:
    totp = pyotp.TOTP(secret_key)
    return totp.now()

#test
if __name__=="__main__":
    sk = 'BHE3HSYG5HSBW2D4'
    a = generate_totp(sk)
    print(a)
