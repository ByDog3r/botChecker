from pyrogram import Client, filters, enums
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.connection import Database
import os
import sqlite3
import asyncio

async def buscar_nombre(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía nombres y apellidos después del comando.')
            return

        terminos = terminos.split()
        condiciones = []
        parametros = []

        for termino in terminos:
            condicion = "(primer_nombre LIKE ? OR segundo_nombre LIKE ? OR tercer_nombre LIKE ? OR primer_apellido LIKE ? OR segundo_apellido LIKE ? OR apellidos LIKE ? OR nombres LIKE ?)"
            condiciones.append(condicion)
            parametros.extend([f'%{termino}%'] * 7)

        consulta_sql = "SELECT * FROM pepe WHERE " + " AND ".join(condiciones)

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute(consulta_sql, parametros)
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                detalle_mensaje = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += detalle_mensaje
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(detalle_mensaje)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por nombre.")
        print(f"Error al buscar por nombre: {e}")

async def buscar_telefono(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía un número de teléfono después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM numeros WHERE telefono LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:5]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
            await message.reply_text(mensaje.strip("\n---\n"))
        else:
            await message.reply_text("No se encontraron registros con ese número de teléfono.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por teléfono.")
        print(f"Error al buscar por teléfono: {e}")

async def buscar_dui(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía un número de DUI después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pepe WHERE numero_dui LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con ese número de DUI.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por DUI.")
        print(f"Error al buscar por DUI: {e}")

async def buscar_correo(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía un correo electrónico después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pepe WHERE correo LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con ese correo electrónico.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por correo electrónico.")
        print(f"Error al buscar por correo: {e}")

async def buscar_direccion(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía una dirección después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pepe WHERE direccion LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con esa dirección.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por dirección.")
        print(f"Error al buscar por dirección: {e}")

async def buscar_direccion2(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía una dirección aproximada después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pepe WHERE direccion2 LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con esa dirección aproximada.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por dirección aproximada.")
        print(f"Error al buscar por dirección aproximada: {e}")

async def buscar_telefono2(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía un número de teléfono alternativo después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM pepe WHERE telefono2 LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con ese número de teléfono alternativo.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar por teléfono alternativo.")
        print(f"Error al buscar por teléfono alternativo: {e}")

async def buscar_oni(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía un término de búsqueda después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM oni WHERE oni LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con ese término.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar en la tabla onis.")
        print(f"Error al buscar en onis: {e}")

async def buscar_placa(client, message, terminos):
    try:
        if not terminos:
            await message.reply_text('Por favor, envía una placa después del comando.')
            return

        conn = sqlite3.connect('src/extras/ciberinteligencia.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM placas WHERE placa LIKE ?", (f'%{terminos}%',))
        resultados = cur.fetchall()

        if resultados:
            mensaje = "Resultados encontrados:\n"
            for resultado in resultados[:50]:
                mensaje_detalle = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(cur.description, resultado) if val]) + "\n---\n"
                mensaje += mensaje_detalle
                numero_dui = resultado[1]
                foto_path = os.path.join('fotos', f"{numero_dui}.jpg")
                if os.path.exists(foto_path):
                    await client.send_photo(chat_id=message.chat.id, photo=open(foto_path, 'rb'))
                    await asyncio.sleep(2)  # Delay to avoid flood error
                await message.reply_text(mensaje_detalle)
                await asyncio.sleep(2)  # Delay to avoid flood error
        else:
            await message.reply_text("No se encontraron registros con esa placa.")

        cur.close()
        conn.close()
    except Exception as e:
        await message.reply_text("Ocurrió un error al buscar en las placas.")
        print(f"Error al buscar placas: {e}")

# Define command handlers
@Client.on_message(filters.command(["nombre"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_nombre_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar un nombre o apellido para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_nombre(client, message, query)

@Client.on_message(filters.command(["telefono"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_telefono_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar un número de teléfono para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_telefono(client, message, query)

@Client.on_message(filters.command(["dui"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_dui_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar un número de DUI para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_dui(client, message, query)

@Client.on_message(filters.command(["email"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_correo_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar un correo electrónico para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_correo(client, message, query)

@Client.on_message(filters.command(["direccion"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_direccion_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar una dirección para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_direccion(client, message, query)

@Client.on_message(filters.command(["direccion2"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_direccion2_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar una dirección aproximada para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_direccion2(client, message, query)

@Client.on_message(filters.command(["telefono2"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_telefono2_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar un número de teléfono alternativo para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_telefono2(client, message, query)

@Client.on_message(filters.command(["oni"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_oni_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar un término para buscar en la tabla onis.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_oni(client, message, query)

@Client.on_message(filters.command(["placa"], ["/", ",", ".", ";", "-"], case_sensitive=False))
async def buscar_placa_handler(client: Client, message: Message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await message.reply("<b>No eres usuario premium</b>", quote=True)
        user_info = db.GetInfoUser(user_id)
    if not query:
        return await message.reply("Debes proporcionar una placa para buscar.", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await message.reply(f"Por favor espera <code>{antispam_result}</code>", quote=True)
    await client.send_chat_action(message.chat.id, action=enums.ChatAction.TYPING)
    await buscar_placa(client, message, query)
