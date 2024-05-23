from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.connection import Database
from re import findall


FORMAT_CMD = "<b>Example: <code>/antispam ID ANTISPAM</code></b>"


@Client.on_message(filters.command("antispam",  ["/", ",", ".", ";"]))
async def spam(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsAdmin(user_id):
            return
        text = m.text[len(m.command[0]) + 2 :].strip()
        data_nums = findall(r"\d+", text)
        if len(data_nums) != 2:
            return await m.reply(FORMAT_CMD, quote=True)
        id = data_nums[0]
        antispam = data_nums[1]
        result = db.SetAntispam(id, antispam)
        if result is None:
            return await m.reply(
                "<b>The user has not started a conversation with the bot!</b>",
                quote=True,
            )
        await m.reply(
            f"""<b>
<code>{id}</code> now he is <code>{antispam}</code> antispam
</b>""",
            quote=True,
        )
