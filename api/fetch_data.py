from api.auth import establish_live_session
import requests
import os
from dotenv import load_dotenv
from api.security import decrypt_access_token

def get_fund_summary(token: str):
    b_URL = "https://api.dhan.co"
    endpoint = "/v2/fundlimit"
    URL = b_URL+endpoint
    headers = {
        'Content-Type':'application/json',
        'access-token': token
    }
    # response = requests.get(URL,headers = headers)
    print(headers)
    # print(response.json())
    # print(response.status_code)

if __name__=="__main__":
    access_token = establish_live_session()
    # print(access_token)
    # access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzgxMDAzMTIwLCJpYXQiOjE3ODA5MTY3MjAsInRva2VuQ29uc3VtZXJUeXBlIjoiQVBQIiwiZGhhbkNsaWVudElkIjoiMTExMTI4MzkxOSJ9.N2KyMIwZKjD43UcL0pNKcTHHsGHQlOfZF9Mr9bwJryIV1LVyxBX4N7SNsPf5SNpNhE0-R4vD8eSsR3FftetvcQ"
    get_fund_summary(decrypt_access_token())