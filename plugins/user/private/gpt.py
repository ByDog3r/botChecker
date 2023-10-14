from pyrogram.types import Message
from src.extras.hypergpt import gpt
from pyrogram.enums import ParseMode
from src.extras.hypergpt import fb_llama
from pyrogram import Client, filters, enums


@Client.on_message(filters.command(["gpt", "GPT"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    text = m.text.split(" ", 1)[1] if not m.reply_to_message.text else m.reply_to_message.text
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    msg = await m.reply("Generating...", quote=True)
    gpt_msg = await fb_llama(text)
    await msg.edit_text(gpt_msg, parse_mode=ParseMode.MARKDOWN)
