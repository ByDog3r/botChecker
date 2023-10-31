from io import BytesIO
from requests import get
from random import randint
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from src.extras.hypergpt import image_gen
from pyrogram import Client, filters, enums
from src.assets.functions import antispam
from src.assets.Db import Database


@Client.on_message(filters.command(["img", "image"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    try:
        img = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    except:
        img = ""
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not text:
        return await m.reply("You need to provide a text to generate", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    generate = await image_gen(img)
    pic = await rand_img(generate)
    send_pic = await client.send_photo(
        chat_id=m.chat.id,
        photo=pic,
        caption=f"{img}"
    )
    


async def rand_img(image):
    rand_img = randint(0, len(image))
    img_url = image[rand_img]
    response = get(img_url)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        image_bytes.name = "image.jpg"
    
    return image_bytes