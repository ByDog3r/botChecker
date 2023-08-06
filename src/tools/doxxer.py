from src.tools.ip_tracker import ip_dox as ip
from src.tools.address import genAddress as faker
from src.tools.sherlock import sherlock as shrlck
from src.tools.whois_script import whois_lookup as w
from requests import get


async def verify_web(site: str):

    try:
    
        if "http://" in site or "https://" in site:
            pass
        else:
            try:
                site = "http://"+site
            except:
                site = "https://"+site

        status = get(site).status_code

        if status == 200 or status == 403:
            return True, site
        else:
            return False

    except:
        return False


async def dox(t:str):
    # update.message.reply_chat_action(ChatAction.TYPING)
      
    
    try:
        #arget = target.args[0] if update.message.reply_to_message == None else update.message.reply_to_message.text 

        #msg = await update.message.reply_text("Doxxing...")
 
        if verify_web(t):
            await t.reply(w(verify_web(t)[1]), quote=True)
            #await msg.edit_text(w(verify_web(target)[1]), parse_mode=ParseMode.HTML)

        elif len(t.split('.')) == 4:
            await t.reply(ip(t), quote=True)
            #await msg.edit_text(ip(target), parse_mode=ParseMode.HTML)

        else:
            await t.reply(shrlck(t), quote=True)
            #await msg.edit_text(shrlck(target), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    except:
        await t.reply("<b>Example to use:</b> >>> host/user/ip", quote=True)
        #await update.message.reply_text("<b>Example to use:</b> >>> host/user/ip", reply_to_message_id=update.message.message_id, parse_mode=ParseMode.HTML)
