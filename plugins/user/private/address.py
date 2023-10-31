import json, time
from requests import get
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatAction
from src.extras.rand_api import GenerateInformation
from src.assets.functions import antispam
from src.assets.Db import Database


@Client.on_message(filters.command(["faker", "fake"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    await client.send_chat_action(m.chat.id, action=ChatAction.TYPING)
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    try:
        name = m.from_user.first_name
        message = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
        address = await genAddress(message, user_id, name)
        await m.reply(
            address,
            quote=True,
            parse_mode=ParseMode.HTML,
        )
    except:
        msg = """<b>Countries available:</b>
\t└ <code>usa</code> - United States
\t└ <code>can</code> - Canada
\t└ <code>mx</code>  - Mexico
\t└ <code>fr</code>  - France
\t└ <code>ger</code> - Germany
\t└ <code>ru</code>  - Russia
\t└ <code>ja</code>  - Japan
\t└ <code>ge</code>  - Georgia
\t└ <code>it</code>  - Italy
\t└ <code>ko</code>  - Korea
\t└ <code>nl</code>  - Netherlands
\t└ <code>aus</code> - Australia
\t└ <code>br</code>  - Brazil
━━━━━━━━━━━
<b>Example to use:</b> /faker usa
"""
        message = await m.reply(msg, quote=True, parse_mode=ParseMode.HTML)
        return message
    

async def genAddress(AreaCode, user_id, u_name):

    initial_time = time.perf_counter()

    try:
        try:
            if AreaCode.lower() == "usa":
                AreaCode = "en"
                initial="USA"
                flag = "🇺🇸"
            elif AreaCode.lower() == "esp" or AreaCode.lower() == "es":
                AreaCode = "es"
                initial="SPAIN"
                flag = "🇪🇸"
            elif AreaCode.lower() == "ger":
                AreaCode = "de"
                initial="GER"
                flag = "🇩🇪"
            elif AreaCode.lower() == "can" or AreaCode.lower() == "ca":
                AreaCode = "fr_CA"
                initial="CAN"
                flag = "🇨🇦"
            elif AreaCode.lower() == "mx":
                AreaCode = "es_MX"
                initial="MEX"
                flag = "🇲🇽 "
            elif AreaCode.lower() == "aus":
                AreaCode = "en_AU"
                initial="AUS"
                flag = "🇦🇺"
            elif AreaCode.lower() == "br":
                AreaCode = "pt_BR"
                initial="BR"
                flag = "🇧🇷"
            elif AreaCode.lower() == "fr":
                AreaCode = "fr"
                initial="FRANCE"
                flag = "🇫🇷"
            elif AreaCode.lower() == "ru":
                AreaCode = "ru"
                initial="RUSSIA"
                flag = "🇷🇺"
            else: 
                AreaCode = AreaCode.lower()

            name, address = GenerateInformation().FakeIdentity(AreaCode)
            address = str(address[0]).split(", ")
            final_time = time.perf_counter() - initial_time
        
            try:
                int(address[3])
                msg = f"""Fake Data [{initial}] {flag}
━━━━━━━━━━━━
└ Name <code>{name}</code>
└ Street <code>{address[0]}</code>
└ City <code>{address[4]}</code>
└ State <code>{address[5]}</code>
└ Zipcode <code>{address[3]}</code>
━━━━━━━━━━━━
Time : {final_time:0.2}
Checked by: <a href='tg://user?id={user_id}'>{u_name}</a>"""

            except:
                msg = f"""Fake Data [{initial}] {flag}
━━━━━━━━━━━━
└ Name <code>{name}</code>
└ Street <code>{address[0]}</code>
└ City <code>{address[3]}</code>
└ State <code>{address[4]}</code>
└ Zipcode <code>{address[2]}</code>
━━━━━━━━━━━━
Time : {final_time:0.2}
Checked by: <a href='tg://user?id={user_id}'>{u_name}</a>"""

        except:
            msg = """<b>Countries available:</b>
\t<code>usa</code> - United States
\t<code>can</code> - Canada
\t<code>mx</code>  - Mexico
\t<code>fr</code>  - France
\t<code>ger</code> - Germany
\t<code>ru</code>  - Russia
\t<code>ja</code>  - Japan
\t<code>ge</code>  - Georgia
\t<code>it</code>  - Italy
\t<code>ko</code>  - Korea
\t<code>nl</code>  - Netherlands
\t<code>aus</code> - Australia
\t<code>br</code>  - Brazil
━━━━━━━━━━━
<b>Example to use:</b> /faker usa
"""

        return msg

    except:
        msg = "<b> Enter a valid Area code.</b>"
        return msg

