import requests as r 
import string, random, time
from datetime import datetime


class makeGate():
    def load_proxies(filename):
        with open(filename, 'r') as file:
            proxies = [{'http': line.strip()} for line in file if line.strip()]
        return proxies

    def getIndex(response):
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(response.text)
            
    def getStr(text:str, a:str, b:str) -> str:
        return text.split(a)[1].split(b)[0]

    def email_generator():
        dominio = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
        leng = random.randint(8, 12) 
        user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(leng))
        email = user + '@' + random.choice(dominio)
        return email

    def open_files(file):
        with open(file, 'r') as f: return [line.strip() for line in f]

    def split_card(card):
        card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
        card_details = card.split("|")
        ccn = card_details[0]
        month = card_details[1]
        year = card_details[2]
        cvv = card_details[3]  

        if card[0] == '4':
            card_type = "Visa"
        elif card[0] == '5':
            card_type = 'MC'
        elif card[0] == '3':
            card_type = "AmEx"

        return ccn, month, year, cvv, card_type