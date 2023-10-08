import os
import logging
from pyrogram import Client
from pyrogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

if __name__ == "__main__":
    os.system('clear')
    app = Client(
        "bot",
        api_id=int(os.getenv('API_ID')),
        api_hash=os.getenv('API_HASH'),
        bot_token=os.getenv('BOT_TOKEN'),
        plugins=dict(
          root="plugins"
          ),
        parse_mode=ParseMode.HTML,
    )
    logging.basicConfig(level=logging.INFO)
    app.run()
