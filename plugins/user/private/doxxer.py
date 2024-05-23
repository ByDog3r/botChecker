import re, sys
from requests import get
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from src.extras.ip_tracker import ip_dox as ip
from src.extras.sherlock import sherlock as shrlck
from src.extras.whois_script import whois_lookup as w
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.enums import ParseMode

@Client.on_message(filters.command([">>", ">"], ['>>', '>']))
async def start(client: Client, m: Message):
    
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True, 
        )
    
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    name = m.from_user.first_name
    msg = await m.reply("<b>Doxxing...</b>", quote=True, parse_mode=ParseMode.HTML)
    target = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    sys.stdout.reconfigure(encoding="utf-8")
    doxed = await dox(target, name, user_id)
    await msg.edit_text(
            doxed,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
    )
    return msg
    
async def evaluate_objective(target: str) -> bool:

    ip_regex = r'^\b(?:\d{1,3}\.){3}\d{1,3}\b$'
    url_regex = r'^(https?://)?([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})(/[a-zA-Z0-9.-]*)*$'
    url = None

    target_response = "IP" if re.match(ip_regex, target) else "SITE" if re.match(url_regex, target) else "user"
    if target_response == "user":
        try:
            get(target)
            target_response = "SITE"
        except:
            pass

    if target_response == "SITE":
        if not target.startswith('http://') and not target.startswith('https://'):
            try: url = "http://"+target, get(url, timeout=3)
            except: url = "https://"+target
        else: url=target
    return target_response, url
    
async def dox(t:str, u, id):
    check_target = await evaluate_objective(t)
    if check_target[0] == "SITE": msg = w(check_target[1], u, id)
    elif check_target[0] == "IP": msg = ip(t)
    elif check_target[0] == "user": msg = shrlck(t)
    else: msg = "<b>Example to use:</b> >>> host/user/ip"
    return msg