async def getMe(update, ParseMode):
    user=str(update.message.from_user.username)
    name=str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name)
    chatID=str(update.message.chat.id)
    userID=str(update.message.from_user.id)
    msg = f"""╔═══════════════════════╗
╟ • [ 👤 ] User: @{user}
╟═══════════════════════╝
╟ •「火 」 ID: <code>{userID}</code>
╟ •「火 」 Name: {name}
╟ •「火 」 Credits: 0.
╟ •「火 」 Estatus: Not DB added yet.
╟━━━━━━━━━━━
╟ •「火 」 Chat ID: <code>{chatID}</code>
╚═══════「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══════╝"""
    await update.message.reply_text(msg, reply_to_message_id=update.message.message_id, parse_mode=ParseMode)



# Start Function
async def StartFnction(update, ParseMode):
    user=str(update.message.from_user.username)
    name=str(update.message.from_user.first_name) + " " + str(update.message.from_user.last_name)
    chatID=str(update.message.chat.id)
    userID=str(update.message.from_user.id)
    
    msg = f"""╔═════════════════╗
╟ • ⊂支⊃ {name}! ⊂支⊃
╟══════════════════
╟ •「夾 」 ID: <code>{userID}</code>
╟ •「夾 」 𝚄𝚂𝙴𝚁: @{user}
╟ •「夾 」 Chat ID: <code>{chatID}</code>
╟ •「夾 」 𝚆𝚛𝚒𝚝𝚎 /cmd 𝚝𝚘 𝚔𝚗𝚘𝚠 𝚖𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜.
╚═══「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」═══╝"""

    await update.message.reply_audio('src/assets/start.mp3', title='Welcome', 
       performer="Snoop Dog", 
        reply_to_message_id=update.message.message_id,
        caption=msg,
        parse_mode=ParseMode)
