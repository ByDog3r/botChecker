import requests as r
import json
from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.Db import Database


@Client.on_message(filters.command(["zip", "zipcode"], ["/", ",", ".", ";", "-"]))
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
        return await m.reply("You need to provide a zipcode.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    zipcode = await zipcode_lookup(text)
    await m.reply(
            zipcode,
            quote=True,
        )

api = "https://api.zippopotam.us/us/"


async def zipcode_lookup(zipcode):

    data = r.get(api + zipcode).json()
    msg = f"""𝐙𝐢𝐩𝐜𝐨𝐝𝐞 𝐋𝐨𝐨𝐤𝐮𝐩
━━━━━━━━━━━━
┌ 𝒁𝒊𝒑𝒄𝒐𝒅𝒆: {data['post code']}
├ 𝑪𝒐𝒖𝒏𝒕𝒓𝒚: {data['country']} - {data['country abbreviation']}
└ 𝑪𝒊𝒕𝒚: {data['places'][0]['place name']} - {data['places'][0]['state abbreviation']}"""

    return msg