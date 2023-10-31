import re
from requests import get
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from src.extras.ip_tracker import ip_dox as ip
from src.extras.sherlock import sherlock as shrlck
from src.extras.whois_script import whois_lookup as w
from src.assets.functions import antispam
from src.assets.Db import Database

@Client.on_message(filters.command([">>", ">"], ['>>', '>']))
async def start(client: Client, m: Message):
    try:
        target = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    except:
        target = ""
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not text:
        return await m.reply("You need to provide a text to generate", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    user_id = m.from_user.id
    name = m.from_user.first_name
    msg = await m.reply("Doxxing...", quote=True)
    doxed = await dox(target, name, user_id)
    await msg.edit_text(
            doxed,
            #quote=True,
            disable_web_page_preview=True
        )
    
async def verify_web(url: str) -> bool:
    try:
        url = "http://"+url if "https://" not in url and "http://" not in url else url
        status = get(url).status_code
        return True, url if status == 200 or status == 403 else False
    except:
        return False
    
async def is_a_valid_ip(ip:str) -> bool:
    ip_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                 r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                 r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                 r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ip_pattern, ip) is not None
    
async def dox(t:str, u, id):
    
    try:
        do_is_site = await verify_web(t)
        do_is_an_ip = await is_a_valid_ip(t)
        if do_is_an_ip:
            msg = ip(t)
        elif do_is_site:
            msg = w(do_is_site[1], u, id)
        else:
            msg = shrlck(t)

    except:
        msg = "<b>Example to use:</b> >>> host/user/ip"
    
    return msg
