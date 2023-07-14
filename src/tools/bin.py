from requests import get
import json

API = "https://bins.antipublic.cc/bins/"

async def bin(update, BIN, ParseMode, ChatAction):

    await update.message.reply_chat_action(ChatAction.TYPING)
        
    try:
        BIN = BIN.args[0] if update.message.reply_to_message == None else update.message.reply_to_message.text 

        data = get(API+BIN).json()
        msg = f"""╔═══════════════════════╗
╟ • [ 鰲 ] 𝑽𝒂𝒍𝒊𝒅 𝑩𝑰𝑵.
╟═══════════════════════╝
╟ •「𖣘 」 𝑩𝑰𝑵 →  <code>{data['bin']}</code>
╟ •「𖣘 」 𝑩𝒂𝒏𝒌: <code>{data['bank']}</code>
╟ •「𖣘 」 𝑪𝒐𝒖𝒏𝒕𝒓𝒚: <code>{data['country_name']}</code> {data['country_flag']}
╟ •「𖣘 」 𝑰𝒏𝒇𝒐: <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
<b>╚═══════「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══════╝</b>"""

    except:
        msg = f"<b>Example to use:</b> /bin 411116"

    await update.message.reply_text(msg, reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
