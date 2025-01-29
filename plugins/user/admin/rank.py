from pyrogram import Client, filters
from pyrogram.types import Message
from re import findall
from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.connection import Database
from re import findall


FORMAT_CMD = f"""<b>
xd
</b>"""


@Client.on_message(filters.command("rank", ["/", ",", ".", ";"]))
async def rol(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsAdmin(user_id) and not db.is_owner(user_id):
            return
        data = str(m.text[len(m.command[0]) + 2 :].strip())
        data_split = data.split(" ")

        if len(data_split) <= 1 or data_split[0].lower() not in [
            "seller",
            "admin",
            "owner",
        ]:
            return await m.reply(FORMAT_CMD)
        rank = data_split[0].lower()
        data = findall(r"\d+", data)
        if len(data) != 1:
            return await m.reply(FORMAT_CMD, quote=True)
        id = data[0]
        result = None
        if rank == "seller":
            result = db.promote_to_seller(id)
        elif rank == "admin":
            result = db.promote_to_admin(id)

        if result is None:
            return await m.reply(
                "<b>usuario no encontrado</b>",
                quote=True,
            )
        await m.reply(
            f"""<b>
Nuevo Rango
ID {user_id}
rango <code>{rank}</code>
</b>""",
            quote=True,
        )
