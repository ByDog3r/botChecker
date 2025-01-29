import re
import os
from urllib.parse import urlparse
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.enums import ParseMode
import asyncio
from pyrogram.errors import PeerIdInvalid


def remove_duplicates(messages):
    unique_messages = list(set(messages))
    duplicates_removed = len(messages) - len(unique_messages)
    return unique_messages, duplicates_removed


async def scrape_messages(user, channel_username, limit, keyword=None):
    messages = []
    offset = 0
    pattern = r"\d{16}\D*\d{2}\D*\d{2,4}\D*\d{3,4}"  # Expresión regular para números de tarjeta

    while len(messages) < limit:
        try:
            async for message in user.search_messages(
                channel_username, offset=offset, limit=100
            ):
                text = message.text if message.text else message.caption
                if text:
                    # Filtrar mensajes con la keyword (si se proporciona)
                    if keyword:
                        if keyword.replace(" ", "").isdigit():
                            # Si la keyword es un número (posiblemente un BIN), buscar como subcadena
                            if keyword.replace(" ", "") not in text.replace(" ", ""):
                                continue
                        elif keyword.lower() not in text.lower():
                            continue

                    # Buscar números de tarjeta en el mensaje
                    matched_messages = re.findall(pattern, text)
                    if matched_messages:
                        formatted_messages = []
                        for matched_message in matched_messages:
                            extracted_values = re.findall(r"\d+", matched_message)
                            if (
                                len(extracted_values) == 4
                            ):  # Validar estructura: tarjeta, mes, año, CVV
                                card_number, mo, year, cvv = extracted_values
                                year = year[-2:]
                                formatted_messages.append(
                                    f"{card_number}|{mo}|{year}|{cvv}"
                                )
                        messages.extend(formatted_messages)

                        if len(messages) >= limit:
                            return messages[:limit]

                offset = message.id
            if not message:
                break
        except PeerIdInvalid:
            print(f"Error: Invalid peer ID for channel {channel_username}. Skipping...")
            break
        except Exception as e:
            print(f"Error during message search: {str(e)}. Continuing...")
            await asyncio.sleep(1)  # Esperar un segundo antes de continuar

    return messages


allow_users = ["7500654993", "6503743826", "830207365"]


@Client.on_message(filters.command(["scr", "scraper"], ["/", ",", ".", ";", "-"]))
async def scr_cmd(client, Message):
    try:
        user = client.user_client
        args = Message.text.split(maxsplit=1)[1:]
        user_id = str(Message.from_user.id)

        if user_id not in allow_users:
            return await Message.reply(
                "<b>You are not authorized to use this command.</b>", quote=True
            )

        if not args:
            return await Message.reply(
                "<b>You need to provide a channel, amount of cards, and optionally a keyword.</b>",
                quote=True,
            )

        try:
            input_text = args[0]
            parsed_args = input_text.split(
                " ", 2
            )  # Dividir solo en 3 partes como máximo

            if len(parsed_args) < 2:
                raise ValueError("Invalid number of arguments.")

            channel_identifier = parsed_args[0]
            limit = int(parsed_args[1])
            keyword = " ".join(parsed_args[2:]) if len(parsed_args) > 2 else None

            # Imprimir la keyword
            print(f"Keyword used: {keyword}")

        except (ValueError, IndexError):
            return await Message.reply(
                '<b>Usage:</b> /scr <channel> <amount_of_cards> ["keyword"]', quote=True
            )

        try:
            parsed_url = urlparse(channel_identifier)
            channel_username = (
                parsed_url.path.lstrip("/") if parsed_url.scheme else channel_identifier
            )
            chat = await user.get_chat(channel_username)
            channel_name = chat.title
        except Exception as e:
            return await Message.reply(
                f"<b>Error:</b> Unable to access channel or chat. Please check if the bot is added to the channel or if the link is valid.\nError details: {str(e)}",
                quote=True,
            )

        progress_message = await Message.reply(
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
            with open(file_name, "w") as f:
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
                    f"<b>Generated by:</b> <a href='https://t.me/ByDog3r'>Leonel M.</a>\n"
                )
                await client.send_document(Message.chat.id, f, caption=caption)
            os.remove(file_name)
        else:
            await progress_message.edit(
                "<b>❌ No results found for the specified criteria.</b>"
            )

        if not unique_messages:
            await progress_message.edit(
                "<b>Scraping completed, but no valid messages were found.</b>"
            )
    except Exception as e:
        print(f"Unexpected error in scr_cmd: {str(e)}")
        await Message.reply(
            "<b>An unexpected error occurred. Please try again later.</b>", quote=True
        )
