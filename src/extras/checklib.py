import requests as r
import random, re, names


class ScrapInfo:
    def getStr(self, text: str, a: str, b: str) -> str:
        return text.split(a)[1].split(b)[0]

    def getIndex(self, response: str):
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(response.text)

    def load_proxies(self, filename: str):
        with open(filename, "r") as file:
            proxies = [{"http": line.strip()} for line in file if line.strip()]
        return proxies

    def open_files(self, file: str):
        with open(file, "r") as f:
            return [line.strip() for line in f]

    def email_generator(self):
        user = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}"
        dominio = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "hotmail.com",
            "example.com",
        ]
        email = f"{user}@{random.choice(dominio)}"
        return email

    def session(self):
        session = r.Session()
        proxies = self.load_proxies("src/extras/proxies.txt")
        proxy = random.choice(proxies)
        session.proxies = proxy
        return session


class MakeGate:

    def __init__(self, card):
        self.api = "https://bins.antipublic.cc/bins/"
        self.card = card
        self.ccn = None
        self.month = None
        self.year = None
        self.cvv = None
        self.card_type = None

        try:
            self._process_card()
        except:
            self.ccn = self.card

    def _process_card(self):
        regex = r"(\d{13,16}\|\d{2}\|\d{2,4}\|\d{3,4})"
        clean_card = self.card.replace(":", "|").replace("/", "|").replace(" ", "|")
        rex = re.search(regex, clean_card)

        if not rex:
            raise ValueError("El formato de la tarjeta no es válido.")

        self.card = rex.group(1)
        card_details = self.card.split("|")
        self.ccn = card_details[0]
        self.month = card_details[1]
        self.year = card_details[2]
        self.cvv = card_details[3]

        if self.ccn[0] == "4":
            self.card_type = "Visa"
        elif self.ccn[0] == "5":
            self.card_type = "MC"
        elif self.ccn[0] == "3":
            self.card_type = "AmEx"
        elif self.ccn[0] == "6":
            self.card_type = "DS"
        else:
            self.card_type = "Unknown"

    def get_card_details(self):
        return self.ccn, self.month, self.year, self.cvv, self.card_type

    def bin_lookup(self):
        bin = self.ccn[:6]
        try:
            data = r.get(self.api + bin).json()
            return (
                data["brand"],
                data["type"],
                data["level"],
                data["bank"],
                data["country_name"],
                data["country_flag"],
            )
        except:
            return "Please enter a valid bin."
