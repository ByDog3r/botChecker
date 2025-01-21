# Script made by @ByDog3r - All right reserved.
#          https://t.me/ByDog3r

import requests as r
from bs4 import BeautifulSoup
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.enums import ParseMode
from pyrogram import Client, filters, enums


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


class GatewayChecker:
    def __init__(self):
        self.gateways = {
            "Braintree": [
                "braintree",
                "braintreegateway",
                "btgateway",
                "braintreepayments",
                "braintree-api",
            ],
            "Amazon Pay": [
                "amazonpay",
                "amazon pay",
                "paywithamazon",
                "amazonpayments",
            ],
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
            "QuickBooks Payments": [
                "quickbooks payments",
                "quickbooks",
                "quickbooks.com",
            ],
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
            "PaymentExpress": [
                "paymentexpress",
                "payment express",
                "paymentexpress.com",
            ],
            "Realex": ["realex", "realexpayments", "realex.com"],
            "Payza": ["payza", "payza.com"],
            "Dlocal": ["dlocal", "dlocal.com"],
            "G2A Pay": ["g2a pay", "g2a.com"],
            "Vindi": ["vindi", "vindi.com.br"],
        }
        self.securities = ["Cloudflare", "Captcha", "ReCaptcha"]

    def check_site(self, site, headers):
        gateways_found, securities_found = [], []
        try:
            code = r.get(site, headers=headers, timeout=5)
            soup = BeautifulSoup(code.text, "html.parser")

            gateways_found = [
                gateway
                for gateway, keywords in self.gateways.items()
                if any(keyword in code.text for keyword in keywords)
            ]

            if "cf-ray" in code.headers:
                securities_found.append("Cloudflare")
            if soup.select('form[action*="/captcha/"]'):
                securities_found.append("Captcha")
            if any(
                keyword in code.text
                for keyword in [
                    "recaptcha/api.js",
                    "g-recaptcha",
                    "www.google.com/recaptcha",
                ]
            ):
                securities_found.append("ReCaptcha")

        except Exception as e:
            return [], [], f"Error: {e}"
        return gateways_found, securities_found, None


class GoogleSearcher:
    def __init__(self, headers):
        self.headers = headers

    def search(self, query, num_results=10):
        search_url = f"https://www.google.com/search?q={query}&num={num_results}"
        response = r.get(search_url, headers=self.headers)
        if response.status_code != 200:
            return [], f"Error: Received status code {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        links = [
            a_tag["href"]
            for g in soup.find_all("div", class_="g")
            if (a_tag := g.find("a")) and "href" in a_tag.attrs
        ]
        return links[:num_results], None


@Client.on_message(
    filters.command(["hunt", "ht"], ["/", ",", ".", ";", "-"], case_sensitive=False)
)
async def gateway(client: Client, m: Message):
    query = (
        " ".join(m.command[1:]) if not m.reply_to_message else m.reply_to_message.text
    )
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not query:
        return await m.reply(
            "You need to provide a dork or keyword to check sites", quote=True
        )
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    msgg = f"""<b>Checking... 🔎</b>
━━━━━━━━━━━
<b>Query:</b> {query}"""
    msg = await m.reply(msgg, quote=True)

    searcher = GoogleSearcher(headers)
    data, error = searcher.search(query)
    if error:
        await m.reply(error)
        return

    checker = GatewayChecker()
    excluded_sites = {
        "amazon",
        "walmart",
        "aliexpress",
        "homedepot",
        "alibaba",
        "pinterest",
        "tiktok",
        "youtube",
        "ebay",
    }
    results = []
    counter = 1

    for site in data:
        if not any(excluded_site in site for excluded_site in excluded_sites):
            gateways_found, securities_found, error = checker.check_site(site, headers)
            if error:
                results.append(error)
                continue

            gateways = " ".join(gateways_found) or "No gateways found."
            securities = " ".join(securities_found) or "No securities found."
            result = f"""↯ <b>Site [{counter}]:</b><br><a href='{site}'>{site}</a><br>"
Gateway:</b> {gateways}
<br>Securities:</b> {securities}<br>\n\n"""
            results.append(result)
            counter += 1
    if results:
        response = f"<b>{query}</b> 🔎\n<br>━━━━━━━━━━━━<br>\n{''.join(results)}"
        await msg.edit_text(
            response,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
    else:
        await msg.edit_text("No se encontraron resultados.")
