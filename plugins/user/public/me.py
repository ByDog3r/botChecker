from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.Db import Database

@Client.on_message(filters.command("me", ["/", ",", ".", ";"]))
async def getMe(client: Client, message: Message):
    user = message.from_user.username
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    name = first_name + " " + last_name
    chatID = message.chat.id
    userID = message.from_user.id
    with Database() as db:
        user_info= db.GetInfoUser(userID)
    
    msg = f"""╔═══════════════════════╗
╟ • [ 👤 ] User: @{user}
╟═══════════════════════╝
╟ •「火 」 ID: <code>{userID}</code>
╟ •「火 」 Name: {name}
╟ •「火 」 Credits: {user_info["CREDITS"]}
╟ •「火 」 Estatus: {user_info["MEMBERSHIP"].capitalize()}
╟━━━━━━━━━━━
╟ •「火 」 Chat ID: <code>{chatID}</code>
╚═══════「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══════╝"""
    await message.reply_text(msg,quote=True)