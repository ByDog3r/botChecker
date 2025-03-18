import random, re, names, aiohttp, json
from twocaptcha import TwoCaptcha as captcha


class ScrapInfo:
    def getStr(self, text: str, a: str, b: str) -> str:
        return text.split(a)[1].split(b)[0]

    def getIndex(self, response: str):
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(response)

    def load_proxies(self, filename: str):
        with open(filename, "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
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

    def proxy_session(self):
        # proxies = self.load_proxies("src/extras/proxies.txt")
        proxy_host = "rp.scrapegw.com"
        proxy_port = 6060
        proxy_user = "nv5mtihnt38gypv"
        proxy_pass = "1bqbj8fcwit8yyt"
        return f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    async def captcha_solver(self, url: str, site_key: str):
        solver = captcha("59d78851f5181c59c1e5d0ec6d2a7ed2")

        try:
            captcha_response = solver.recaptcha(site_key, url)
        except Exception as e:
            return f"Captcha Error: {e}"
        else:
            g_captcha = json.dumps(captcha_response["code"])
            g_captcha = self.getStr(g_captcha, '"', '"')
            captcha_id = json.dumps(captcha_response["captchaId"])
            return g_captcha, captcha_id


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

    async def bin_lookup(self):
        bin = self.ccn[:6]
        try:
            async with aiohttp.ClientSession() as r:
                async with r.get(self.api + bin) as data:
                    data = await data.json()
                    return (
                        data["brand"],
                        data["type"],
                        data["level"],
                        data["bank"],
                        data["country_name"],
                        data["country_flag"],
                    )
        except Exception as e:
            return f"Error: {str(e)}"
