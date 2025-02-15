import re
import asyncio
import os
from urllib.parse import urlparse
from pyrogram import filters, Client
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.enums import ParseMode
from json import load
from pyrogram.errors import PeerIdInvalid
from main import SESSION_STRING


def remove_duplicates(messages):
    unique_messages = list(set(messages))
    duplicates_removed = len(messages) - len(unique_messages)
    return unique_messages, duplicates_removed


# Función para scrapear mensajes usando search_messages sobre el chat_id
async def scrape_messages(user, chat_id, limit, keyword=None):
    messages = []
    offset = 0
    pattern = r"\d{16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}"

    async def process_message(message):
        text = message.text if message.text else message.caption
        if text:
            if keyword:
                if keyword.replace(" ", "").isdigit():
                    if keyword.replace(" ", "") not in text.replace(" ", ""):
                        return
                elif keyword.lower() not in text.lower():
                    return

            matched_messages = re.findall(pattern, text)
            if matched_messages:
                formatted_messages = []
                for matched_message in matched_messages:
                    extracted_values = re.findall(r"\d+", matched_message)
                    if len(extracted_values) == 4:
                        card_number, mo, year, cvv = extracted_values
                        year = year[-2:]
                        formatted_messages.append(f"{card_number}|{mo}|{year}|{cvv}")
                messages.extend(formatted_messages)

    tasks = []
    try:
        async for message in user.search_messages(chat_id, offset=offset, limit=100000):
            tasks.append(asyncio.create_task(process_message(message)))
            if len(tasks) >= 100:
                await asyncio.gather(*tasks)
                tasks.clear()

            if len(messages) >= limit:
                break

            offset = message.id

        if tasks:
            await asyncio.gather(*tasks)

    except PeerIdInvalid:
        print(f"Error: Invalid peer ID for chat {chat_id}. Skipping...")
    except Exception as e:
        print(f"Error during message search: {str(e)}. Continuing...")
        await asyncio.sleep(1)

    return messages[:limit]


@Client.on_message(filters.command(["scr", "scraper"], ["/", ",", ".", ";", "-"]))
async def scr_cmd(client, message: Message):
    user = Client("user_session", session_string=SESSION_STRING)
    try:
        await user.start()
        args = message.text.split(maxsplit=1)[1:]
        user_id = int(message.from_user.id)

        with Database() as db:
            if not db.IsPremium(user_id):
                return await message.reply("<b>You are not premium</b>", quote=True)
            user_info = db.GetInfoUser(message.from_user.id)
        if not args:
            return await message.reply(
                "<b>You need to provide a channel/chat_id, amount of cards, and optionally a keyword.</b>",
                quote=True,
            )
        antispam_result = antispam(user_id, user_info["ANTISPAM"])
        if antispam_result != False:
            return await message.reply(
                f"Please wait <code>{antispam_result}'s</code>", quote=True
            )

        try:
            input_text = args[0]
            parsed_args = input_text.split(" ", 2)
            if len(parsed_args) < 2:
                raise ValueError("Invalid number of arguments.")

            channel_identifier = parsed_args[0]
            limit = int(parsed_args[1])
            keyword = " ".join(parsed_args[2:]) if len(parsed_args) > 2 else None
        except (ValueError, IndexError):
            return await message.reply(
                '<b>Usage:</b> /scr <channel/chat_id> <amount_of_cards> ["keyword"]',
                quote=True,
            )

        # Determinar si se pasó un chat_id numérico o un username/URL
        try:
            if channel_identifier.lstrip("-").isdigit():
                # Se asume que es un chat_id numérico (privado o grupo)
                chat_id_int = int(channel_identifier)
                try:
                    chat = await user.get_chat(chat_id_int)
                except PeerIdInvalid as e:
                    # Si es numérico y falla, probablemente la cuenta no es miembro.
                    return await message.reply(
                        f"<b>Error:</b> Unable to access channel or chat. It seems you are not a member of this chat.\nError details: {str(e)}",
                        quote=True,
                    )
            else:
                # Se asume que es un username o URL (canal público)
                parsed_url = urlparse(channel_identifier)
                username = (
                    parsed_url.path.lstrip("/")
                    if parsed_url.scheme
                    else channel_identifier
                )
                try:
                    chat = await user.get_chat(username)
                except PeerIdInvalid:
                    # Si falla, se intenta unirse al chat (solo funciona en canales públicos)
                    chat = await user.join_chat(username)
            channel_name = (
                chat.title
                if hasattr(chat, "title") and chat.title
                else (chat.first_name or "Chat")
            )
        except Exception as e:
            return await message.reply(
                f"<b>Error:</b> Unable to access channel or chat. Please check if you have access to it.\nError details: {str(e)}",
                quote=True,
            )

        progress_message = await message.reply(
            "<b>Scraping in progress, please wait...</b>", quote=True
        )

        try:
            scrapped_results = await scrape_messages(
                user, chat.id, limit, keyword=keyword
            )
        except Exception as e:
            await progress_message.edit(f"<b>Error during scraping:</b> {str(e)}")
            return

        unique_messages, duplicates_removed = remove_duplicates(scrapped_results)

        if unique_messages:
            file_name = f"x{len(unique_messages)}_{channel_name.replace(' ', '_')}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(unique_messages))

            with open(file_name, "rb") as f:
                caption = (
                    f"<b>✅ Scraping completed successfully!</b>\n"
                    f"<b>━━━━━━━━━━</b>\n"
                    f"<b>Source:</b> <code>{channel_name}</code>\n"
                    f"<b>Amount:</b> <code>{len(unique_messages)}</code>\n"
                    f"<b>Duplicates Removed:</b> <code>{duplicates_removed}</code>\n"
                    f"<b>Keyword Used:</b> <code>{keyword or 'None'}</code>\n"
                    f"<b>━━━━━━━━━━</b>\n"
                    f"<b>Generated by:</b>\n"
                )
                await client.send_document(message.chat.id, f, caption=caption)
            os.remove(file_name)
        else:
            await progress_message.edit(
                "<b>❌ No results found for the specified criteria.</b>"
            )

    except Exception as e:
        print(f"Unexpected error in scr_cmd: {str(e)}")
        await message.reply(
            "<b>An unexpected error occurred. Please try again later.</b>", quote=True
        )
    finally:
        await user.stop()
