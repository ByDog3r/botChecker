import os
from shutil import rmtree
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("delck", ["/", ",", ".", ";"]))
async def delck(client: Client, m: Message):
    result = await delcache(client, m)
    if result:
        await m.reply(
            "<b>Cache has been deleted successfully ✅</b>",
            quote=True,
        )
    else:
        pass


async def delcache(client, message) -> bool: 
    cache_borrada = False
    directorio = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    archivos_directorios = os.listdir(directorio)
    for elemento in archivos_directorios:
        if os.path.isdir(elemento):
            arch_dirs = os.listdir(elemento)
            if "__pycache__" in arch_dirs:
                rmtree(os.path.join(elemento, "__pycache__"))
            for i2 in arch_dirs:
                if os.path.isdir(os.path.join(elemento, i2)):
                    arch_dirs = os.listdir(os.path.join(elemento, i2))
                    if "__pycache__" in arch_dirs:
                        rmtree(os.path.join(os.path.join(elemento, i2), "__pycache__"))
    else:
        cache_borrada = True

    return cache_borrada