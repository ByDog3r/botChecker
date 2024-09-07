# Script made by @ByDog3r - All right reserved. 
#          https://t.me/ByDog3r

import requests as r
from bs4 import BeautifulSoup
from huepy import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

class GatewayChecker:
    def __init__(self):
        self.gateways = {
            "Braintree": ["braintree", "braintreegateway", "btgateway", "braintreepayments", "braintree-api"],
            "Amazon Pay": ["amazonpay", "amazon pay", "paywithamazon", "amazonpayments"],
            "PayPal": ["paypal", "paypalobjects", "paypal.com"],
            "Stripe": ["stripe", "stripe.com", "checkout.stripe.com"],
            "Shopify": ["shopify", "shopify.com", "payments.shopify.com"],
            "Square": ["squareup", "square", "square.com", "squareup.com"],
            "Adyen": ["adyen", "adyen.com"],
            "Authorize.Net": ["authorize.net", "authorize net", "authnet", "authorize"],
            "2Checkout": ["2checkout", "2co.com"],
            "Worldpay": ["worldpay", "worldpay.com"],
            "Skrill": ["skrill", "skrill.com", "moneybookers"],
            "Alipay": ["alipay", "alipay.com"],
            "WePay": ["wepay", "wepay.com"],
            "BlueSnap": ["bluesnap", "bluesnap.com"],
            "Klarna": ["klarna", "klarna.com"],
            "Afterpay": ["afterpay", "afterpay.com"],
            "Mollie": ["mollie", "mollie.com"],
            "Paysafe": ["paysafe", "paysafe.com"],
            "BitPay": ["bitpay", "bitpay.com"],
            "Coinbase Commerce": ["coinbase commerce", "coinbase", "coinbase.com"],
            "Revolut": ["revolut", "revolut.com"],
            "TransferWise": ["transferwise", "wise.com"],
            "Payoneer": ["payoneer", "payoneer.com"],
            "QuickBooks Payments": ["quickbooks payments", "quickbooks", "quickbooks.com"],
            "Venmo": ["venmo", "venmo.com"],
            "Zelle": ["zelle", "zellepay", "zelle.com"],
            "Google Pay": ["google pay", "googlepay", "pay.google.com"],
            "Apple Pay": ["apple pay", "applepay", "apple.com"],
            "Samsung Pay": ["samsung pay", "samsungpay", "samsung.com"],
            "Verifone": ["verifone", "verifone.com"],
            "PagSeguro": ["pagseguro", "pagseguro.com"],
            "MercadoPago": ["mercadopago", "mercadopago.com"],
            "Conekta": ["conekta", "conekta.io"],
            "Openpay": ["openpay", "openpay.mx"],
            "Yandex.Money": ["yandex money", "yandexmoney", "yandex.money"],
            "PayU": ["payu", "payu.com"],
            "Razorpay": ["razorpay", "razorpay.com"],
            "Instamojo": ["instamojo", "instamojo.com"],
            "Paytm": ["paytm", "paytm.com"],
            "PhonePe": ["phonepe", "phonepe.com"],
            "Freecharge": ["freecharge", "freecharge.com"],
            "BillDesk": ["billdesk", "billdesk.com"],
            "CCAvenue": ["ccavenue", "ccavenue.com"],
            "FirstData": ["firstdata", "first data", "firstdata.com"],
            "Zuora": ["zuora", "zuora.com"],
            "BluePay": ["bluepay", "bluepay.com"],
            "Moneris": ["moneris", "moneris.com"],
            "Magento": ["magento", "magento.com"],
            "WooCommerce": ["woocommerce", "woocommerce.com"],
            "CyberSource": ["cybersource", "cybersource.com"],
            "Neteller": ["neteller", "neteller.com"],
            "Barclaycard": ["barclaycard", "barclaycard.com"],
            "Eway": ["eway", "eway.com"],
            "Sezzle": ["sezzle", "sezzle.com"],
            "Zip": ["zip.co", "zip money", "zip", "zip.co"],
            "Affirm": ["affirm", "affirm.com"],
            "Fattmerchant": ["fattmerchant", "fattmerchant.com"],
            "SecurionPay": ["securionpay", "securionpay.com"],
            "Paysimple": ["paysimple", "paysimple.com"],
            "Dwolla": ["dwolla", "dwolla.com"],
            "PayTrace": ["paytrace", "paytrace.com"],
            "PaymentExpress": ["paymentexpress", "payment express", "paymentexpress.com"],
            "Realex": ["realex", "realexpayments", "realex.com"],
            "Payza": ["payza", "payza.com"],
            "Dlocal": ["dlocal", "dlocal.com"],
            "G2A Pay": ["g2a pay", "g2a.com"],
            "Vindi": ["vindi", "vindi.com.br"]
        }
        self.securities = ["Cloudflare", "Captcha", "ReCaptcha"]
    
    def check_site(self, site, headers):
        gateways_found, securities_found = [], []
        try:
            code = r.get(site, headers=headers, timeout=5)
            soup = BeautifulSoup(code.text, 'html.parser')
            
            gateways_found = [gateway for gateway, keywords in self.gateways.items() if any(keyword in code.text for keyword in keywords)]
            
            if 'cf-ray' in code.headers:
                securities_found.append("Cloudflare")
            if soup.select('form[action*="/captcha/"]'):
                securities_found.append("Captcha")
            if any(keyword in code.text for keyword in ['recaptcha/api.js', 'g-recaptcha', 'www.google.com/recaptcha']):
                securities_found.append("ReCaptcha")
            
        except Exception as e:
            print("\n\t"+info(f" {e}"))
        return gateways_found, securities_found

class GoogleSearcher:
    def __init__(self, headers):
        self.headers = headers
    
    def search(self, query, num_results=1000):
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        response = r.get(search_url, headers=self.headers)
        if response.status_code != 200:
            return f"Error: Received status code {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a_tag['href'] for g in soup.find_all('div', class_='g') if (a_tag := g.find('a')) and 'href' in a_tag.attrs]
        return links[:num_results]

def main():
    print(red("""
  /$$$$$$              /$$               /$$   /$$                       /$$                        
 /$$__  $$            | $$              | $$  | $$                      | $$                        
| $$  \ $$ /$$   /$$ /$$$$$$    /$$$$$$ | $$  | $$ /$$   /$$ /$$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
| $$$$$$$$| $$  | $$|_  $$_/   /$$__  $$| $$$$$$$$| $$  | $$| $$__  $$|_  $$_/   /$$__  $$ /$$__  $$
| $$__  $$| $$  | $$  | $$    | $$  \ $$| $$__  $$| $$  | $$| $$  \ $$  | $$    | $$$$$$$$| $$  \__/
| $$  | $$| $$  | $$  | $$ /$$| $$  | $$| $$  | $$| $$  | $$| $$  | $$  | $$ /$$| $$_____/| $$      
| $$  | $$|  $$$$$$/  |  $$$$/|  $$$$$$/| $$  | $$|  $$$$$$/| $$  | $$  |  $$$$/|  $$$$$$$| $$      
|__/  |__/ \______/    \___/   \______/ |__/  |__/ \______/ |__/  |__/   \___/   \_______/|__/      
                                    Made by @ByDog3r
              """))

    kw = input(info(lightgreen("Enter your keyword or dork: ")))
    searcher = GoogleSearcher(headers)
    data = searcher.search(kw)
    
    checker = GatewayChecker()
    excluded_sites = {"amazon", "walmart", "aliexpress", "homedepot", "alibaba", "pinterest", "tiktok", "youtube", "ebay"}
    counter = 1

    for site in data:
        if not any(excluded_site in site for excluded_site in excluded_sites):
            gateways_found, securities_found = checker.check_site(site, headers)
            gateways = ' '.join(gateways_found) or "No gateways found."
            securities = ' '.join(securities_found) or "No securities found."
            if gateways_found:
                print("\n\t" + white(f"┌ [{counter}] Site Found: ") + yellow(f"{site}") + white(f" Gateways found: ") + red(f"{gateways} \n\t└ ") + white(f"Securities: {securities}"))
                counter += 1

if __name__ == "__main__":
    main()

