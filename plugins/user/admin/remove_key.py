from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.connection import Database

@Client.on_message(filters.command("delk", ["/", ",", ".", ";"]))
async def removekey(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsAdmin(user_id):
            return
    key = m.text[len(m.command[0]) + 2 :].strip()
    if not key or not key.startswith("bot-key"):
        return await m.reply("<b>Enter a valid key!</b>", quote=True)
    with Database() as db:
        result = db.RemoveKey(key)
    if result is None:
        return await m.reply(
            "<b>The key <code>{}</code> has not been found!</b>".format(
                key
            ),
            quote=True,
        )
    await m.reply(
        f"""<b>
Key successfully removed!
</b>""",
        quote=True,
    )
    