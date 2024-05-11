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
        self.code = self.sesion.get(self.url, headers=headers, timeout=3) 
        self.soup = BeautifulSoup(self.code.text, 'html.parser')

    def cloudflare(self):
        return True if "cf-ray" in self.code.headers else False

    def captcha(self):
        soup = BeautifulSoup(self.code.text, 'html.parser')
        return True if len(soup.select('form[action*="/captcha/"]')) > 0 else False
   
    def recaptcha(self):
        return True if 'recaptcha/api.js' in self.code.text or 'g-recaptcha' in self.code.text or 'recaptcha/api.js' in self.code.text or 'www.google.com/recaptcha' in self.code.text else False
        
    def server(self):
        try: return self.code.headers['Server'] if self.code.headers else False
        except: return False

    def gateway(self):
        try:
            if 'stripe.com' in self.code.text:
                gate = "Stripe"

            elif 'braintreegateway.com' in self.code.text:
                gate = "B3"

            elif 'paypalobjects.com' in self.code.text:
                gate = "Paypal"

            else:
                gate = "none"

            return gate
        except:
            pass

    
def whois_lookup(site:str, name, user_id):
    init_time = perf_counter() 
    web = dox_site(site)
    final_time = perf_counter() - init_time

    msg = f"""<b>𝑽𝒂𝒍𝒊𝒅 𝒑𝒂𝒈𝒆</b>
━━━━━━━━━━━━
<b>Security:</b>
┌ <b>Cloudflare :</b> <code>{web.cloudflare()}</code>
├ <b>Captcha :</b> <code>{web.captcha()}</code>
├ <b>reCaptcha :</b> <code>{web.recaptcha()}</code>
└ <b>Server :</b> <code>{web.server()}</code>

━━━━━━━━━━━━
┌ <b>Site :</b> <code>{site}</code>
├ <b>Time :</b> {final_time:0.2}
└ <b>Checked by :</b> <a href='tg://user?id={user_id}'>{name}</a>"""

    return msg
