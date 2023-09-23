import logging
from json import load
from pyrogram import Client
from pyrogram.enums import ParseMode
from src.assets.banner import banner


config_bot = load(open("src/assets/cfgbot.json"))
API_ID = config_bot["API_ID"]
API_HASH = config_bot["API_HASH"]
BOT_TOKEN = config_bot["BOT_TOKEN"]

if __name__ == "__main__":
    banner()
    app = Client(
        "bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins"),
        parse_mode=ParseMode.HTML,
    )
    logging.basicConfig(level=logging.ERROR)
    app.run()
