import re
from pyrogram import Client, filters
from pyrogram.types import Message
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.enums import ParseMode

@Client.on_message(filters.command(["chota", "ch"], ["/", ",", ".", ";", "-"]))
async def chota_lookup(client: Client, m: Message):
    try:
        text = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    except:
        text = ""
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not text:
        return await m.reply("<b>Example to use:</b> .ch 37039", quote=True, parse_mode=ParseMode.HTML)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    buscando_chota = await buscar_dato_por_oni(text)
    await m.reply(
            buscando_chota,
            quote=True,
        )

async def buscar_dato_por_oni(oni):
    with open('src/extras/filtracionPNC.txt', 'r') as file:
        contenido = file.read()
        
    bloques = re.split(r'\n(?=ONI:)', contenido)
    datos = []
    for bloque in bloques:
        info = {}
        for linea in bloque.strip().split('\n'):
            if ':' in linea:
                clave, valor = re.split(r':\s*', linea, 1)
                info[clave.strip()] = valor.strip()
        datos.append(info)
    
    dato_encontrado = next((dato for dato in datos if dato.get('ONI') == oni), None)
    
    if dato_encontrado:
        resultado = "\n".join(f"{clave}: {valor}" for clave, valor in dato_encontrado.items())
    else:
        resultado = "ONI no encontrado."
    
    return resultado
