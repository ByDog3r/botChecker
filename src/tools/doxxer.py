from src.tools.ip_tracker import ip_dox as ip
from src.tools.address import genAddress as faker
from src.tools.sherlock import sherlock as shrlck
from src.tools.whois_script import whois_lookup as w

async def dox(update, target, ParseMode, ChatAction):
    await update.message.reply_chat_action(ChatAction.TYPING)
      
    try:
        target = target.args[0] if update.message.reply_to_message == None else update.message.reply_to_message.text 

        msg = await update.message.reply_text("Doxxing...")
        
        if  '.com' in target or '.org' in target or '.net' in target:
            await msg.edit_text(w(target), parse_mode=ParseMode.HTML)

        elif len(target.split('.')) == 4:
            await msg.edit_text(ip(target), parse_mode=ParseMode.HTML)

        else:
            await msg.edit_text(shrlck(target), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    except:
        await update.message.reply_text("<b>Example to use:</b> >>> host/user/ip", reply_to_message_id=update.message.message_id, parse_mode=ParseMode.HTML)
