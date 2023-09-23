import json, time
from requests import get
from pyrogram import Client, filters
from pyrogram.types import Message

API = "https://bins.antipublic.cc/bins/"

@Client.on_message(filters.command("bin", ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    bin = m.text[len("/bin ") :] if m.reply_to_message.text == None else m.reply_to_message.text
    user_id = m.from_user.id
    name = m.from_user.first_name
    lookup = await bin_lookup(bin, user_id, name)
    await m.reply(
            lookup,
            quote=True,
        )


async def bin_lookup(BIN, user_id, u_name):

    initial_time = time.perf_counter() 
    try:
        data = get(API+BIN).json()
        final_time = time.perf_counter() - initial_time
        msg = f"""Bin Information
━━━━━━━━━━━━
└ Bin <code>{data['bin']}</code>
└ Info <code>{data['brand']}</code> - <code>{data['type']}</code> - <code>{data['level']}</code>
└ <code>{data['bank']}</code>
└ Country <code>{data['country_name']}</code> {data['country_flag']}
━━━━━━━━━━━━
Time : {final_time:0.2}
Checked by: <a href='tg://user?id={user_id}'>{u_name}</a> """

    except:
        msg = f"<b>Example to use:</b> /bin 411116"

    return msg
