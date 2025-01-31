import aiohttp, asyncio
import json
from twocaptcha import TwoCaptcha as captcha
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.enums import ParseMode
from time import perf_counter


def getStr(text: str, a: str, b: str) -> str:
    return text.split(a)[1].split(b)[0]


api_key = "59d78851f5181c59c1e5d0ec6d2a7ed2"


@Client.on_message(filters.command(["check", "imei"], ["/", ",", ".", ";", "-"]))
async def start(client: Client, m: Message):
    try:
        text = (
            m.text.split(" ", 1)[1]
            if not m.reply_to_message
            else m.reply_to_message.text
        )
    except:
        text = ""
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not text:
        return await m.reply("You need to provide an imei.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    name = m.from_user.first_name
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    msg = await m.reply("checking...", parse_mode=ParseMode.HTML)

    asyncio.gather(check_imei(text, msg, name, user_id))
    #imei_checker = await check_imei(text, msg, name, user_id)


async def check_imei(imei, msg, name, user_id):

    init_time = perf_counter()

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en,es;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        # Primera solicitud
        async with session.get(
            "https://www.imeipro.info/", headers=headers
        ) as response:
            response_text = await response.text()
            sitekey = getStr(response_text, "'sitekey' : '", "',")

        await msg.edit_text(
            "We are checking in Apple data base the info... please wait.",
            parse_mode=ParseMode.MARKDOWN,
        )

        # Resolver el captcha
        solver = captcha(api_key)

        try:
            captcha_response = solver.recaptcha(sitekey, "https://www.imeipro.info/")
        except Exception as e:
            await msg.edit_text(f"Captcha Error: {e}", parse_mode=ParseMode.MARKDOWN)
            return
        else:
            g_captcha = json.dumps(captcha_response["code"])
            g_captcha = getStr(g_captcha, '"', '"')
            captcha_id = json.dumps(captcha_response["captchaId"])
            captchaId = getStr(captcha_id, '"', '"')
            await msg.edit_text("We checked, is done.", parse_mode=ParseMode.MARKDOWN)

        headers = {
            "Accept": "*/*",
            "Accept-Language": "en,es;q=0.9",
            "Connection": "keep-alive",
            "Referer": "https://www.imeipro.info/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        params = {
            "imei": imei,
            "grecaptcharesponse": g_captcha,
            "_": captchaId,
        }

        async with session.get(
            "https://www.imeipro.info/check_imei_number", params=params, headers=headers
        ) as response:
            response_text = await response.text()
            phone = getStr(response_text, '"phoneModel":"', '",')
            blacklisted = getStr(response_text, '"blacklisted":', ",")

        final_time = perf_counter() - init_time
        msgg = f"""𝑰𝑴𝑬𝑰 𝑪𝒉𝒆𝒄𝒌𝒆𝒓 ✅
━━━━━━━━━━━━
┌ <b>IMEI:</b> <code>{imei}</code>
├ <b>Model:</b> {phone}
├ <b>Blacklisted:</b> {blacklisted}
└ <b>Checked by :</b> <a href='tg://user?id={user_id}'>{name}</a>"""

        await msg.edit_text(msgg, parse_mode=ParseMode.HTML)
