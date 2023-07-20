from requests import get
from enum import Enum


class Languages(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    PORTUGES = "pt"
    SIMPLIFIED_CHINESE = "zh-CN"
    RUSSIAN = "ru"
    GERMAN = "de"
    JAPANESE = "ja"
    French = "fr"
    # Se pueden agregar mas


async def translate(update, text: str, ParseMode, translate_to: Languages=Languages.SPANISH) -> str:
    text = text.args[0] if update.message.reply_to_message == None else update.message.reply_to_message.text 
    if len(text) <= 2:
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

    msg = f"""╔═══════════════════════╗
╟ • [ 鰲 ] Translator →  <b>ByCheckerBot</b>.
╟═══════════════════════╝
╟ • Input: <code>{text}</code>
╟ ━━━━━━━━━━━
╟ • Traduction: <code>{traduction}</code>
<b>╚═══════「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══════╝</b>"""

    await update.message.reply_text(msg, reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
