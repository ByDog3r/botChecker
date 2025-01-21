from enum import Enum
from requests import get
from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.connection import Database

@Client.on_message(filters.command(["tr", "tra"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    try:
        text = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    except:
        text = ""
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not text:
        return await m.reply("You need to provide a text to translate", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
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

    msg = f"""<b>Translator [🇪🇸]</b>
━━━━━━━━━━━━
<b>Traduction:</b> <code>{traduction}</code>
━━━━━━━━━━━━
Checked by @ByDog3r
"""

    return msg
