import os
from shutil import rmtree


def delcache() -> bool:  # Mejorar usando while y no varios bucles
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


async def delckc(update, ParseMode):
    result = delcache()
    if result:
        await update.message.reply_text(
            "<b>Cache has been deleted successfully ✅</b>",
            reply_to_message_id=update.message.message_id,
            parse_mode=ParseMode,
        )
    else:
        await update.message.reply_text(
            "<b>IDK XD aun no se manejan excepciones</b>",
            reply_to_message_id=update.message.message_id,
            parse_mode=ParseMode,
        )

