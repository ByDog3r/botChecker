from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.connection import Database

@Client.on_message(filters.command("claim", ["/", ",", ".", ";"]))
async def claim(client: Client, m: Message):
    key = m.text[len(m.command[0]) + 2 :].strip()
    if not key or not key.startswith("bot-key"):
        return await m.reply("<b>Enter a valid key!</b>", quote=True)
    user_id = m.from_user.id
    with Database() as db:
        result = db.ClaimKey(key, user_id)
    if result is None:
        return await m.reply(
            "<b>The key <code>{}</code> has not been found!</b>".format(
                key
            ),
            quote=True,
        )
    await m.reply(f"""<b>Now you are premium</b>
━━━━━━━━━━━
┌ <b>Key successfully claimed!
└ Expiration:</b> <code>{result}</code>""",
        quote=True,
    )
    