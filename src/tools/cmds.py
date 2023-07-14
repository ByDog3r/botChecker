async def CommandsFunction(update, context, key, markup, ParseMode):
    user=str(update.message.from_user.username)
    name=str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name)
    chatID=str(update.message.chat.id)
    userID=str(update.message.from_user.id)
    

    keyboard = [

        [

            key("Gates", callback_data="gates"),

            key("Tools", callback_data="cmds"),

        ],

        [key("Close Menu", callback_data="close")]

    ]


    buttons = markup(keyboard)
   
    msg = f"⊂支⊃ ByCheck! ⊂支⊃\n━━━━━━━━━━━━━━━━━━"
    await update.message.reply_text(msg, reply_markup=buttons)




async def cmd_buttons(update, context, key, markup, ParseMode) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "cmds":

        msg = f"<b>Check our commands</b>"
        keyboard = [

        [

            key("Carding Toolkit", callback_data="carding"),

            key("Doxxing Toolkit", callback_data="doxxing"),

        ],

        [key("Close Menu", callback_data="close")]

    ]

        buttons = markup(keyboard)
        await query.edit_message_text(msg, reply_markup=buttons, parse_mode=ParseMode)


    elif query.data == "carding":

        msg = f"""╔═══════════════════════╗
╟ • [ 鰲  ] <b>Tools.</b>
╟═══════════════════════╝
╟ • [  宏 ] Name: <b>Bin Lookup</b>
╟ •「 夾 」Use: <code>/bin 411116</code>
╟━━━━━━━━━━━
╟ • [  宏 ] Name: <b>Gen CC</b>
╟ •「 夾 」Use: <code>/gen 411116xxxx</code>
╟━━━━━━━━━━━
╟ • [  宏 ] Name: <b>Fake Address generator</b>
╟ •「 夾 」Use: <code>/faker mx</code>
╚═══════「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══════╝""" 

        keyboard = [

        [key("Go back", callback_data="cmds")],

        [key("Close Menu", callback_data="close")]

    ]

        buttons = markup(keyboard)
        await query.edit_message_text(msg, reply_markup=buttons, parse_mode=ParseMode)



    elif query.data == "doxxing":

        msg = f"""╔═══════════════════════╗
╟ • [ 鰲  ] <b>Tools.</b>
╟═══════════════════════╝
╟ • [  宏 ] Name: <b>Sherlock</b>
╟ •「 夾 」Use: <code>>>> ByDog3r</code>
╟━━━━━━━━━━━
╟ • [  宏 ] Name: <b>IP Tracker</b>
╟ •「 夾 」Use: <code>>>> 1.1.1.1</code>
╟━━━━━━━━━━━
╟ • [  宏 ] Name: <b>Whois Lookup</b>
╟ •「 夾 」Use: <code>>>> https://motherfuckingwebsite.com/</code>
╚═══════「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══════╝""" 

        keyboard = [

        [key("Go back", callback_data="cmds")],

        [key("Close Menu", callback_data="close")]

    ]

        buttons = markup(keyboard)
        await query.edit_message_text(msg, reply_markup=buttons, parse_mode=ParseMode)



    elif query.data == "close":
        msg = f"<b>Thanks for using :)</b>"
        await query.edit_message_text(msg, parse_mode=ParseMode)

    elif query.data == "gates":
        msg = "No gate available."
        keyboard = [

            [key("Go back", callback_data="menu")],

            [key("Close Menu", callback_data="close")]

    ]

        buttons = markup(keyboard)
        await query.edit_message_text(msg, reply_markup=buttons, parse_mode=ParseMode)

    elif query.data == "menu":
        keyboard = [

        [

            key("Gates", callback_data="gates"),

            key("Tools", callback_data="cmds"),

        ],

        [key("Close Menu", callback_data="close")]

    ]


        buttons = markup(keyboard)
   
        msg = f"⊂支⊃ ByCheck! ⊂支⊃\n━━━━━━━━━━━━━━━━━━"
        await query.edit_message_text(msg, reply_markup=buttons, parse_mode=ParseMode)

