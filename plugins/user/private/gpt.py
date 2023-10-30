from pyrogram.types import Message
from src.extras.hypergpt import gpt
from pyrogram.enums import ParseMode
from src.extras.hypergpt import fb_llama
from pyrogram import Client, filters, enums
from src.assets.functions import antispam
from src.assets.Db import Database

@Client.on_message(filters.command(["gpt", "GPT"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    text = m.text[len("/gpt ") :] if m.reply_to_message == None else m.reply_to_message.text
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
    msg = await m.reply("Generating...", quote=True)
    gpt_msg = await fb_llama(text)
    await msg.edit_text(gpt_msg, parse_mode=ParseMode.MARKDOWN)
