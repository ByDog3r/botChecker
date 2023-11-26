from src.assets.Db import Database
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton, Message)


@Client.on_message(filters.command("start", ["/", ",", ".", ";"]))
async def StartFnction(client: Client, message: Message):
    user = message.from_user.username
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    name = first_name + " " + last_name
    chatID = message.chat.id
    userID = message.from_user.id

    with Database() as db:
        user_info= db.GetInfoUser(userID)

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
                [
                    [  
                        InlineKeyboardButton( 
                            "Commands",
                            callback_data="initial_menu"
                        )
                    ]
                ]
            )
        )



@Client.on_message(filters.command("me", ["/", ",", ".", ";"]))
async def getMe(client: Client, message: Message):
    user = message.from_user.username
    first_name = message.from_user.first_name if message.from_user.first_name else ""
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    name = first_name + " " + last_name
    chatID = message.chat.id
    userID = message.from_user.id
    with Database() as db:
        user_info= db.GetInfoUser(userID)
    
    msg = f""" 👤  User: @{user}
━━━━━━━━━━━
└ <b>ID:</b> <code>{userID}</code>
└ <b>Name:</b> {name}
└ <b>Credits:</b> {user_info["CREDITS"]}
└ <b>Estatus:</b> {user_info["MEMBERSHIP"].capitalize()}
━━━━━━━━━━━
<b>Chat ID:</b> <code>{chatID}</code>"""
    await message.reply_text(msg,quote=True)
    


@Client.on_message(filters.command(["cmds", "cmd"], ["/", ",", ".", ";"]))
async def commands(client: Client, m: Message):
    await m.reply(
            "<b>Select an option:</b>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton( 
                            "Gates",
                            callback_data="gates"
                        ),
                        InlineKeyboardButton(
                            "Tools",
                            callback_data="tools"
                        ),
                    ],
                    [  # Second row
                        InlineKeyboardButton( 
                            "Close",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )


@Client.on_callback_query(filters.regex("gates"))
def gates_button_callback(client, callback_query):
    callback_query.edit_message_text("┌ <b>Jeico (!jk)</b> ✅\n└ payflow auth gateway.",
                                     reply_markup=InlineKeyboardMarkup(
                [
                    
                    [  
                        InlineKeyboardButton( 
                            "Go back",
                            callback_data="initial_menu"
                        )
                    ],
                    [
                        InlineKeyboardButton( 
                            "Close",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )
                                     

@Client.on_callback_query(filters.regex("tools"))
def tools_button_callback(client, callback_query):
    callback_query.edit_message_text("""<b> Commands | 1/3 🔄 </b>
━━━━━━━━━━━━
┌ <b>Faker</b> (!faker) ✅
└ Fake address generator.

┌ <b>BIN</b> (!bin) ✅
└ Bin lookup tool.

┌ <b>Gen</b> (!gen) ✅
└ CC generator

┌ <b>Translator</b> (!tr) ✅
└ Translate to spanish""",
reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton( 
                            "Go back",
                            callback_data="initial_menu"
                        ),
                        InlineKeyboardButton(
                            "Next",
                            callback_data="ia"
                        ),
                    ],
                    [  # Second row
                        InlineKeyboardButton( 
                            "Close",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )
    
@Client.on_callback_query(filters.regex("close"))
def close_button_callback(client, callback_query):
    callback_query.edit_message_text("<b>Closed</b>")

@Client.on_callback_query(filters.regex("initial_menu"))
def intial_menu_button_callback(client, callback_query):
    callback_query.edit_message_text("<b>Select an option:</b>", 
    reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton( 
                            "Gates",
                            callback_data="gates"
                        ),
                        InlineKeyboardButton(
                            "Tools",
                            callback_data="tools"
                        ),
                    ],
                    [  # Second row
                        InlineKeyboardButton( 
                            "Close",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )
    

@Client.on_callback_query(filters.regex("ia"))
def ia_button_callback(client, callback_query):
    callback_query.edit_message_text("""<b> Artificial Intelligence | 2/3 🔄 </b>
━━━━━━━━━━━━
┌ <b>GPT</b> (!gpt) ✅
└ Llama IA chat.

┌ <b>IMG</b> (!img) ✅
└ IA img generator.""",
reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton( 
                            "Go back",
                            callback_data="tools"
                        ),
                        InlineKeyboardButton(
                            "Next",
                            callback_data="quacking"
                        )
                    ],
                    [  # Second row
                        InlineKeyboardButton( 
                            "Close",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )


@Client.on_callback_query(filters.regex("quacking"))
def quackingtools_button_callback(client, callback_query):
    callback_query.edit_message_text("""<b> Hacking Tools | 3/3 🔄 </b>
━━━━━━━━━━━━
┌ <b>DoxToolkit</b> (>>>) ✅
└ Dox a specific target.""",
reply_markup=InlineKeyboardMarkup(
                [
                    [  # First row
                        InlineKeyboardButton( 
                            "Go back",
                            callback_data="ia"
                        )
                    ],
                    [  # Second row
                        InlineKeyboardButton( 
                            "Close",
                            callback_data="close"
                        )
                    ]
                ]
            )
        )