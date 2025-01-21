import re
from time import perf_counter
from requests import get, Session
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

class dox_site:

    def __init__(self, url:str) -> None:
        self.url = url
        self.sesion = Session()
        self.code = self.sesion.get(self.url, headers=headers, timeout=5) 
        self.soup = BeautifulSoup(self.code.text, 'html.parser')

    def cloudflare(self):
        return True if "cf-ray" in self.code.headers else False

    def captcha(self):
        return True if len(self.soup.select('form[action*="/captcha/"]')) > 0 else False
   
    def recaptcha(self):
        return True if 'recaptcha/api.js' in self.code.text or 'g-recaptcha' in self.code.text or 'recaptcha/api.js' in self.code.text or 'www.google.com/recaptcha' in self.code.text else False
        
    def server(self):
        try: return self.code.headers['Server'] if self.code.headers else False
        except: return False

    def gateway(self):

        gateways = []

        try:
            if 'stripe' in self.code.text:
                gateways.append("Stripe")

            if 'braintree' in self.code.text:
                gateways.append("Braintree (B3)")

            if 'paypal' in self.code.text:
                gateways.append("Paypal")

            if 'squareup' in self.code.text or 'square' in self.code.text:
                gateways.append("Square")

            if 'shopify' in self.code.text:
                gateways.append("Shopify")

            if 'dlocal' in self.code.text:
                gateways.append("Dlocal")

            if 'recurly' in self.code.text:
                gateways.append("Recurly")

            if 'adyen' in self.code.text:
                gateways.append("Adyen")

            if 'payeezy' in self.code.text:
                gateways.append("Payeezy")

            if 'wix' in self.code.text:
                gateways.append("Wix")

            if 'bluepay' in self.code.text:
                gateways.append("bluepay")

            if 'authorize.net' in self.code.text or 'authorize net' in self.code.text:
                gateways.append("Authorize")

            if 'cybersource' in self.code.text:
                gateways.append("Cybersource")

            if 'woocommerce' in self.code.text:
                gateways.append("WooCommerce")

            if 'moneris' in self.code.text:
                gateways.append("Moneris")

            if 'skrill' in self.code.text:
                gateways.append("Skrill")

            if 'eway' in self.code.text:
                gateways.append("Eway")

            if 'magento' in self.code.text:
                gateways.append("Magento")

            if '2checkout' in self.code.text or '2co' in self.code.text:
                gateways.append("2Checkout")

            if 'klarna' in self.code.text:
                gateways.append("Klarna")
            
            if 'worldpay' in self.code.text:
                gateways.append("Worldpay")

            if 'amazon pay' in self.code.text or 'amazonpay' in self.code.text:
                gateways.append("Amazon Pay")

            if 'google pay' in self.code.text or 'googlepay' in self.code.text:
                gateways.append("Google Pay")

            if 'apple pay' in self.code.text or 'applepay' in self.code.text:
                gateways.append("Apple Pay")

            if 'bitpay' in self.code.text:
                gateways.append("BitPay")

            if 'coinbase' in self.code.text:
                gateways.append("Coinbase")

            if 'alipay' in self.code.text:
                gateways.append("Alipay")

            if 'afterpay' in self.code.text:
                gateways.append("Afterpay")

            gates = ""

            for gate in gateways:
                gates += gate + " "

            if gates == "":
                gates = "Gateway not found."
            else: pass

            return gates
        except:
            pass

    
def whois_lookup(site:str, name, user_id):
    init_time = perf_counter() 
    web = dox_site(site)
    final_time = perf_counter() - init_time

    msg = f"""<b>Information found [ ☁️ ]</b>
━━━━━━━━━━━━
<b>Security:</b>
<a href="https://t.me/ByDog3r">↯</a> <b>Cloudflare :</b> <code>{web.cloudflare()}</code>
<a href="https://t.me/ByDog3r">↯</a> <b>Captcha :</b> <code>{web.captcha()}</code>
<a href="https://t.me/ByDog3r">↯</a> <b>reCaptcha :</b> <code>{web.recaptcha()}</code>
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway :</b> <code>{web.gateway()}</code>
<a href="https://t.me/ByDog3r">↯</a> <b>Server :</b> <code>{web.server()}</code>

━━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>Site :</b> <code>{site}</code>
<a href="https://t.me/ByDog3r">↯</a> <b>Time :</b> {final_time:0.2}
<a href="https://t.me/ByDog3r">↯</a> <b>Checked by :</b> <a href='tg://user?id={user_id}'>{name}</a>"""
    return msg
