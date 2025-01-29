import os
from shutil import rmtree
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("delck", ["/", ",", ".", ";"]))
async def delck(client: Client, m: Message):
    result = await delcache()
    if result:
        await m.reply(
            "<b>Cache has been deleted successfully ✅</b>",
            quote=True,
        )


async def delcache() -> bool:
    main_directory = os.getcwd()
    for root, dirs, files in os.walk(main_directory, topdown=False):
        for subdirectory in dirs:
            if subdirectory == "__pycache__" or subdirectory == "__pycache__ 2":
                dir_path = os.path.join(root, subdirectory)
                rmtree(dir_path)
    return True
