import re
from src.assets.Db import Database
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("key", ["/", ",", ".", ";"]))
async def gkey(client: Client, m: Message):
    with Database() as db:
        if not db.IsAdmin(m.from_user.id):
            return await m.reply("<b>You are not admin</b>", quote=True)
        days = re.search(r"\d+", m.text)
        if not days:
            return await m.reply("<b>Invalid days\nExample: /key 30</b>", quote=True)
        days = int(days.group())
        generated_key = db.GenKey(days)
        await m.reply(
            f"<b>Key generated successfully\nKey: {generated_key[0]}\nDays: {days}</b>\nExpiration:{generated_key[1]}",
            quote=True,
        )