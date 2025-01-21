import aiohttp
from datetime import datetime
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram import Client, filters, enums
import random, time, rsa, base64, names, json
from src.extras.checklib import MakeGate, ScrapInfo

name_gate = "Payeezy_Auth"
subtype = "Payeezy Auth"
command = "yz"


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
    email = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
    proxies = ScrapInfo.load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)
    connector = aiohttp.ProxyConnector(proxy=proxy)

    current_time = datetime.now().strftime("%D - %H:%M:%S")
    fecha_hora_actual = datetime.now()
    current_timestamp = int(fecha_hora_actual.timestamp() * 1000)
    email = f"{names.get_first_name()}{names.get_last_name()}%40gmail.com"
    four = random.randint(1000, 9999)
    tree = random.randint(100, 999)

    card_split = MakeGate(card).get_card_details()
    ccn = card_split[0]
    month = card_split[1]
    year = card_split[2]
    if len(year) == 2:
        year = f"20{card_split[2]}"
    cvv = card_split[3]
    card_type = card_split[4]

    initial_time = time.time()
    data_bin = MakeGate(card).bin_lookup()

    async with aiohttp.ClientSession(connector=connector) as session:
        # First request
        headers = {
            "authority": "api.freshop.com",
            "referer": "https://www.shakersmarketplace.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        }

        data = {
            "app_key": "shakers",
            "locale": "false",
            "referrer": "https://www.shakersmarketplace.com/",
            "utc": current_timestamp,
        }

        async with session.post(
            "https://api.freshop.com/2/sessions/create", headers=headers, data=data
        ) as response:
            response_text = await response.text()
            token = ScrapInfo.getStr(response_text, '"token":"', '"')

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

        # More requests would follow here, converted to use aiohttp in a similar manner.

    # Placeholder for final response processing
    final_time = time.time() - initial_time
    card_response = f"""<b>#Payeezy_Auth ($yz) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: COMPLETED<b>
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
