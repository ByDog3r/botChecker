from pyrogram import Client
from json import load


# Reemplaza con tus credenciales de Telegram
config_bot = load(open("src/assets/cfgbot.json"))
API_ID = config_bot["API_ID"]
API_HASH = config_bot["API_HASH"]


async def main():
    async with Client("user_session", api_id=API_ID, api_hash=API_HASH) as app:
        session_string = await app.export_session_string()
        print("Tu SESSION_STRING es:")
        print(session_string)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
