import json, time
from requests import get
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatAction
from src.extras.rand_api import GenerateInformation


@Client.on_message(filters.command(["faker", "fake"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    await client.send_chat_action(m.chat.id, action=ChatAction.TYPING)
    message = m.text[len("/faker ") :]
    user_id = m.from_user.id
    name = m.from_user.first_name
    address = await genAddress(message, user_id, name)
    await m.reply(
            address,
            quote=True,
            parse_mode=ParseMode.HTML,
        )

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

