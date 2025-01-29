from src.assets.connection import Database
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


@Client.on_message(filters.command("start", ["/", ",", ".", ";"]))
async def StartFnction(client: Client, message: Message):
    user = message.from_user.username
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    name = first_name + " " + last_name
    chatID = message.chat.id
    userID = message.from_user.id

    with Database() as db:
        user_info = db.GetInfoUser(userID)

    msg = f"""                      .𝑩𝒚𝑪𝒉𝒆𝒄𝒌 ﷻ
━━━━━━━━━━━
┌   Usuario[TG] - @{user}
├   Telegram[ID] - <code>{userID}</code>
├   Creditos[CHK] - {user_info["CREDITS"]}
├   Estatus[CHK] - {user_info["MEMBERSHIP"].capitalize()}
└  Chat ID: <code>{chatID}</code>"""

    await message.reply_audio(
        audio="src/assets/start.mp3",
        title=f"Welcome {name}!",
        performer="Snoop Dog ft .byCheck",
        quote=True,
        caption=msg,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Commands", callback_data="initial_menu")]]
        ),
    )


@Client.on_message(filters.command("me", ["/", ",", ".", ";", "-"]))
async def getMe(client: Client, message: Message):
    user = message.from_user.username
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    name = first_name + " " + last_name
    chatID = message.chat.id
    userID = message.from_user.id
    with Database() as db:
        user_info = db.GetInfoUser(userID)

    msg = f""" 👤  User: @{user}
━━━━━━━━━━━
┌ <b>ID:</b> <code>{userID}</code>
├ <b>Name:</b> {name}
├ <b>Credits:</b> {user_info["CREDITS"]}
└ <b>Estatus:</b> {user_info["MEMBERSHIP"].capitalize()}
━━━━━━━━━━━
<b>Chat ID:</b> <code>{chatID}</code>"""
    await message.reply_photo("src/assets/dollar.jpeg", caption=msg)


@Client.on_message(filters.command(["cmds", "cmd"], ["/", ",", ".", ";", "-"]))
async def commands(client: Client, m: Message):
    await m.reply(
        "<b>Select an option:</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton("Gateways  💸", callback_data="gates"),
                    InlineKeyboardButton("Tools 🔨", callback_data="tools"),
                ],
                [InlineKeyboardButton("Close", callback_data="close")],  # Second row
            ],
        ),
    )


@Client.on_callback_query(filters.regex("gates"))
def gates_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Gateways | 0/3 💳
━━━━━━━━━━━━
Total Gates </b> <a href="https://t.me/ByDog3r">⊁</a> 6
<b>Auth</b> <a href="https://t.me/ByDog3r">⊁</a> 0
<b>Charged</b> <a href="https://t.me/ByDog3r">⊁</a> 5
<b>VBV</b> <a href="https://t.me/ByDog3r">⊁</a> 1

<b>Select one of the buttons bellow to check base on the gate that you want</b>""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Auth", callback_data="Auth"),
                    InlineKeyboardButton("Charged", callback_data="charged"),
                    InlineKeyboardButton("VBV", callback_data="vbvv"),
                ],
                [InlineKeyboardButton("Back", callback_data="initial_menu")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("Auth"))
def auth_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Gateways Auth | 1/3 🔄
━━━━━━━━━━━━
</b>┌ <b>Payeezy Auth (<a href='https://t.me/ByDog3r'>!yz</a>) ✅
</b>└ Payeezy Auth gateway.
""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Return", callback_data="gates"),
                    InlineKeyboardButton("ᗒ", callback_data="charged"),
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex("charged"))
def charged_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Gateways Charged | 2/3 🔄
━━━━━━━━━━━━
</b>┌ <b>Authorize_net AVS (<a href='https://t.me/ByDog3r'>!au</a>) ✅
</b>└ $16.95 Charged gateway.

</b>┌ <b>Payflow Charged (<a href='https://t.me/ByDog3r'>!pc</a>) ✅
</b>└ $60 Charged gateway.

</b>┌ <b>Paypal Charged (<a href='https://t.me/ByDog3r'>!pp</a>) ✅
</b>└ $0,1 Charged gateway

</b>┌ <b>Stripe Charged (<a href='https://t.me/ByDog3r'>!str</a>) ✅
</b>└ 10$ Charged gateway

</b>┌ <b>Recurly Charged (<a href='https://t.me/ByDog3r'>!rec</a>) ✅
</b>└ 60$ Charged gateway

</b>┌ <b>Braintree Charged (<a href='https://t.me/ByDog3r'>!bra</a>) ✅
</b>└ 30$ Charged gateway""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᗕ", callback_data="Auth"),
                    InlineKeyboardButton("Return", callback_data="gates"),
                    InlineKeyboardButton("ᗒ", callback_data="vbvv"),
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex("vbvv"))
def vbvv_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Gateways Auth | 1/3 🔄
━━━━━━━━━━━━
</b>┌ <b>Braintree VBV (<a href='https://t.me/ByDog3r'>!vbv</a>) ✅
</b>└ Braintree 3D.""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᗕ", callback_data="charged"),
                    InlineKeyboardButton("Return", callback_data="gates"),
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex("tools"))
def tools_button_callback(client, callback_query):
    callback_query.edit_message_text(
        """<b> Checker Tools | 0/3 🛠️ </b>
━━━━━━━━━━━━
<b>Total Tools </b> <a href="https://t.me/ByDog3r">⊁</a> 20
<b>Bining Tools</b>  <a href="https://t.me/ByDog3r">⊁</a> 5
<b>Artificial Intelligence Tools</b>  <a href="https://t.me/ByDog3r">⊁</a> 2
<b>Hacking Tools</b>  <a href="https://t.me/ByDog3r">⊁</a> 5
<b>CiberInteligenciaSV Leak</b>  <a href="https://t.me/ByDog3r">⊁</a> 9

<b>Select one of the buttons bellow to check base on the tool that you want</b>""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton("Bining", callback_data="bining"),
                    InlineKeyboardButton("IA", callback_data="iartificial"),
                    InlineKeyboardButton("Hacking", callback_data="quacking"),
                ],
                [  # Second row
                    InlineKeyboardButton(
                        "CiberInteligenciaSV", callback_data="CiberInteligenciaSV"
                    )
                ],
                [  # Third row
                    InlineKeyboardButton("Back", callback_data="initial_menu")
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("bining"))
def bining_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""Commands | 1/4 🔄 </b>
━━━━━━━━━━━━
┌ <b>Faker</b> (<a href='https://t.me/ByDog3r'>!faker</a>) ❌
└ Fake address generator.

┌ <b>BIN</b> (<a href='https://t.me/ByDog3r'>!bin</a>) ✅
└ Bin lookup tool.

┌ <b>GEN</b> (<a href='https://t.me/ByDog3r'>!gen</a>) ✅
└ CC generator.

┌ <b>Zipcode Lookup</b> (<a href='https://t.me/ByDog3r'>!zip</a>) ✅
└ Zipcode lookup.

┌ <b>Translator</b> (<a href='https://t.me/ByDog3r'>!tr</a>) ✅
└ Translate to spanish""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Return", callback_data="tools"),
                    InlineKeyboardButton("ᗒ", callback_data="iartificial"),
                ]
            ],
        ),
    )


@Client.on_callback_query(filters.regex("CiberInteligenciaSV"))
def CiberInteligenciaSV_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Leaks by <a href='https://t.me/guacamayal'>CiberInteligenciaSv</a> | 4/4 🔄 </b>
━━━━━━━━━━━━
┌ <b>Name</b> (<a href='https://t.me/ByDog3r'>!nombre</a>) ✅
└ Doxxing by name.

┌ <b>Email</b> (<a href='https://t.me/ByDog3r'>!email</a>) ✅
└ Doxxing by email.

┌ <b>Phone Number</b> (<a href='https://t.me/ByDog3r'>!telefono</a>) ✅
└ Doxxing by phone number.

┌ <b>ID</b> (<a href='https://t.me/ByDog3r'>!dui</a>) ✅
└ Doxxing by ID.

┌ <b>Address</b> (<a href='https://t.me/ByDog3r'>!direccion</a>) ✅
└ Doxxing by address.

┌ <b>Car Plate</b> (<a href='https://t.me/ByDog3r'>!placa</a>) ✅
└ Doxxing by car plate.

┌ <b>Chota Lookup</b> (<a href='https://t.me/ByDog3r'>!oni</a>) ✅
└ Doxxing by ONI.

┌ <b>Second address</b> (<a href='https://t.me/ByDog3r'>!direccion2</a>) ✅
└ Doxxing by a possible address.

┌ <b>Second phone #</b> (<a href='https://t.me/ByDog3r'>!telefono2</a>) ✅
└ Doxxing by a possible phone number.""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᗕ", callback_data="quacking"),
                    InlineKeyboardButton("Return", callback_data="tools"),
                ]
            ]
        ),
    )


@Client.on_callback_query(filters.regex("iartificial"))
def iartificial_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Artificial Intelligence | 2/4 🔄 </b>
━━━━━━━━━━━━
┌ <b>GPT</b> (<a href='https://t.me/ByDog3r'>!gpt</a>) ❌
└ Llama IA chat.

┌ <b>IMG</b> (<a href='https://t.me/ByDog3r'>!img</a>) ❌
└ IA img generator.""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᗕ", callback_data="bining"),
                    InlineKeyboardButton("Return", callback_data="tools"),
                    InlineKeyboardButton("ᗒ", callback_data="quacking"),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("quacking"))
def quackingtools_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"""<b> Hacking Tools | 3/4 🔄 </b>
━━━━━━━━━━━━
┌ <b>DoxToolkit</b> (<a href='https://t.me/ByDog3r'>>>></a>) ✅
└ Dox a specific target.

┌ <b>Auto Hunter</b> (<a href='https://t.me/ByDog3r'>!ht</a>) ✅
└ Hunter system.

┌ <b>Imei checker</b> (<a href='https://t.me/ByDog3r'>!imei</a>) ❌
└ Check Apple Imei.

┌ <b>Scraper CC</b> (<a href='https://t.me/ByDog3r'>!scr</a>) ✅
└ Telegram Scraper CC's.""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᗕ", callback_data="iartificial"),
                    InlineKeyboardButton("Return", callback_data="tools"),
                    InlineKeyboardButton("ᗒ", callback_data="CiberInteligenciaSV"),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("close"))
def close(client, callback_query):
    callback_query.edit_message_text(
        "<b><a href='https://t.me/ByDog3r'>...</b></a>", disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("initial_menu"))
def initial_menu_button_callback(client, callback_query):
    callback_query.edit_message_text(
        f"<b>Select an option:</b>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [  # First row
                    InlineKeyboardButton("Gateways  💸", callback_data="gates"),
                    InlineKeyboardButton("Tools 🔨", callback_data="tools"),
                ],
                [InlineKeyboardButton("Close", callback_data="close")],
            ]
        ),
    )
