from io import BytesIO
from requests import get
from random import randint
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from src.extras.hypergpt import image_gen
from pyrogram import Client, filters, enums

@Client.on_message(filters.command(["img", "image"], ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    img = m.text.split(" ", 1)[1] if not m.reply_to_message.text else m.reply_to_message.text
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    generate = await image_gen(img)
    pic = await rand_img(generate)
    await client.send_photo(
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