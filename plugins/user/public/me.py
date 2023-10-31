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
    
    msg = f""" 👤  User: @{user}
━━━━━━━━━━━
└ ID: <code>{userID}</code>
└ Name: {name}
└ Credits: {user_info["CREDITS"]}
└ Estatus: {user_info["MEMBERSHIP"].capitalize()}
━━━━━━━━━━━
Chat ID: <code>{chatID}</code>"""
    await message.reply_text(msg,quote=True)