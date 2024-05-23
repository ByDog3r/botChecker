from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.connection import Database
from re import findall


@Client.on_message(filters.command("add", ["/", ",", ".", ";"]))
async def add_premium(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsAdmin(user_id):
            return
        data = m.text[len(m.command[0]) + 2 :].strip()
        data = findall(r"\d+", data)

        if len(data) != 3:
            return await m.reply("<b>Example: /add ID DAYS CREDITS</b>", quote=True)

        id = data[0]
        days = data[1]

        credits = data[2]
        result = db.AddPremiumMembership(id, days, credits)
        info_user = db.GetInfoUser(user_id)
        if result is None:
            return await m.reply(
                "<b>The ID is not found in the database, you must start a conversation with the bot</b>",
                quote=True,
            )
        await m.reply(f"""<code>{id}</code> <b>promoted to premium</b>
━━━━━━━━━━━
└ <b>Days:</b> <code>{days}</code>
└ <b>Credits:</b> <code>{credits}</code>
└ <b>Expiration:</b> <code>{result}</code>""",
            quote=True,
        )
        