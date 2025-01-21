import time
from requests import get
from pyrogram import Client, filters
from pyrogram.types import Message
from src.extras.checklib import MakeGate


@Client.on_message(filters.command("bin", ["/", ",", ".", ";", "-"]))
async def start(client: Client, m: Message):
    bin = (
        m.text[len("/bin ") :]
        if m.reply_to_message == None
        else m.reply_to_message.text
    )
    user_id = m.from_user.id
    name = m.from_user.first_name
    lookup = await bin_lookup(bin, user_id, name)
    await m.reply(
        lookup,
        disable_web_page_preview=True,
    )


async def bin_lookup(BIN, user_id, u_name):

    initial_time = time.perf_counter()
    try:
        data_bin = MakeGate(BIN).bin_lookup()
        final_time = time.perf_counter() - initial_time
        msg = f"""<b>[⛈️] #{BIN} FOUND</b>
━━━━━━━━━━━━
<a href="https://t.me/ByDog3r">[↯]</a> <b>Information Found</b>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[0]}</code> - <code>{data_bin[1]}</code> - <code>{data_bin[2]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[3]}</code>
<a href="https://t.me/ByDog3r">⊁</a> <code>{data_bin[4]} {data_bin[5]}
━━━━━━━━━━━━
<b>Time</b> : {final_time:0.2}
<b>Checked by:</b> <a href='tg://user?id={user_id}'>{u_name}</a>

<code>bot by : @ByDog3r</code>"""

    except:
        msg = f"<b>Example to use:</b> /bin 411116"

    return msg
