import logging, asyncio
from json import load
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.enums import ParseMode
from src.assets.banner import banner
from src.assets.connection import Database


config_bot = load(open("src/assets/cfgbot.json"))
API_ID = config_bot["API_ID"]
API_HASH = config_bot["API_HASH"]
BOT_TOKEN = config_bot["BOT_TOKEN"]
SESSION_STRING = config_bot["SESSION_STRING"]
# BOT_TOKEN = "6388281047:AAFf-30F-CgfN55Fk19Oo0oh1ae749MnpSY"  # is for test


async def handle_text(client: Client, m: Message):
    if not m.from_user:
        return
    with Database() as db:
        user_id = m.from_user.id
        username = m.from_user.username
        db.RemoveExpiredsUsers()
        banned = db.IsBan(user_id)
        if banned:
            return
        db.RegisterUser(user_id, username)
        await m.continue_propagation()


async def main():
    banner()

    app = Client(
        "ByCheckerBot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins"),
        parse_mode=ParseMode.HTML,
        workers=1000,
    )

    user = Client("user_session", session_string=SESSION_STRING, workers=1000)

    await app.start()
    await user.start()

    app.add_handler(MessageHandler(handle_text, filters.text))
    logging.basicConfig(level=logging.ERROR)

    try:
        await asyncio.Future()
    finally:
        await user.stop()
        await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
