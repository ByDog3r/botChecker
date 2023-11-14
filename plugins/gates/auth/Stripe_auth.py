import requests as r
import string, random, re, time
# from src.assets.functions import antispam
# from src.assets.Db import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

session = r.Session()
API = "https://snapmuse.com/auth/register"

def getIndex(response):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        
def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]

def email_generator():
    dominio = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    longitud = random.randint(8, 12)  # Longitud aleatoria del nombre de usuario
    usuario = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    correo = usuario + '@' + random.choice(dominio)
    return correo

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

email_req = email_generator()

headers = {
    'authority': 'api.snapmuse.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,es;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://snapmuse.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-cid': '1706079420.1699897880',
    'x-request-from': 'ssr-frontend',
    'x-transaction-hash': '65526213f9f0cf1ab80efe47-655262cd83f58630565bceba-6552638683f58630565bcf4e',
}

json_data = {
    'firstName': 'Leonel',
    'lastName': 'Molina',
    'email': email_req,
    'password': 'holkgold21',
    'acceptsTermsAndConditions': [
        True,
    ],
    'userName': email_req,
    'verificationUrl': 'https://snapmuse.com/account/verify',
}

response = session.post('https://api.snapmuse.com/user/register', headers=headers, json=json_data)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

headers = {
    'authority': 'snapmuse.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,es;q=0.9',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://snapmuse.com',
    'referer': 'https://snapmuse.com/auth/register',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-cid': '1706079420.1699897880',
    'x-request-from': 'ssr-frontend',
    'x-transaction-hash': '65526213f9f0cf1ab80efe47-655262cd83f58630565bceba-6552638683f58630565bcf4e',
}

data = {
    'username': email_req,
    'password': 'holkgold21',
}

response = session.post('https://snapmuse.com/i/session/login', headers=headers, data=data)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

headers = {
    'authority': 'snapmuse.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,es;q=0.9',
    'referer': 'https://snapmuse.com/auth/register',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

response = session.get('https://snapmuse.com/checkout/subscription/standart30R4', headers=headers)
getIndex(response)