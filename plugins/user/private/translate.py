from enum import Enum
from requests import get
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["tr", "tra"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    text = m.text.split(" ", 1)[1] if not m.reply_to_message.text else m.reply_to_message.text
    traduction = await translate(text)
    await m.reply(
            traduction,
            quote=True,
        )
    
class Languages(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    PORTUGES = "pt"
    SIMPLIFIED_CHINESE = "zh-CN"
    RUSSIAN = "ru"
    GERMAN = "de"
    JAPANESE = "ja"
    French = "fr"
    # you can add more.


async def translate(text: str, translate_to: Languages=Languages.SPANISH) -> str:
    if len(text) <= 1:
        raise ValueError("No puedes ingresar una cadena menor a 3 caracteres")
    assert isinstance(translate_to, Languages), "El lenguaje debe pertenecer a la clase Languages"
    params = {
        "client": "dict-chrome-ex",
        "sl": "auto",
        "tl": translate_to.value,
        "q": str(text),
        "tbb": "1",
        "ie": "UTF-8",
        "oe": "UTF-8",
    }
    traduction = get("https://translate.google.com/translate_a/t?", params=params).json()[0][0]

    msg = f""" Translator [🇪🇸]
━━━━━━━━━━━━
Traduction: <code>{traduction}</code>
━━━━━━━━━━━━
Checked by @ByDog3r
"""

    return msg