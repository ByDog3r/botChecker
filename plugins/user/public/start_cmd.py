from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("start", ["/", ",", ".", ";"]))
async def StartFnction(client: Client, message: Message):
    user = message.from_user.username
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    name = first_name + " " + last_name
    chatID = message.chat.id
    userID = message.from_user.id

    msg = f"""╔═════════════════╗
╟ • ⊂支⊃ {name}! ⊂支⊃
╟══════════════════
╟ •「夾 」 ID: <code>{userID}</code>
╟ •「夾 」 𝚄𝚂𝙴𝚁: @{user}
╟ •「夾 」 Chat ID: <code>{chatID}</code>
╟ •「夾 」 𝚆𝚛𝚒𝚝𝚎 /cmd 𝚝𝚘 𝚔𝚗𝚘𝚠 𝚖𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜.
╚═══「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══╝"""

    await message.reply_audio(
        audio="src/assets/start.mp3",
        title="Welcome",
        performer="Snoop Dog",
        quote=True,
        caption=msg,
    )
