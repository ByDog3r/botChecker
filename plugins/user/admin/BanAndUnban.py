from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.connection import Database


@Client.on_message(filters.command(["ban", "unban"], ["/", ",", ".", ";"]))
async def ban_unban(client: Client, m: Message):
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsAdmin(user_id):
            return
        if len(m.command) != 2 or not m.command[1].isdigit():
            return await m.reply("<b>Enter a valid id</b>", quote=True)
        command, id = m.command
        ban_user = True if command == "ban" else False
        text = (
            "<b><code>{}</code> succesfull banned!</b>"
            if ban_user
            else "<b><code>{}</code> succesfull unbaned!</b>"
        )
        result = db.UnbanOrBanUser(id, ban_user)
        if result is None:
            return await m.reply(
                "<b>ID not founded in DB!</b>".format(
                    id
                ),
                quote=True,
            )
        await m.reply(text.format(id), quote=True)
