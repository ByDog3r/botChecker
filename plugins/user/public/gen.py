import json
import random
import datetime
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


@Client.on_message(filters.command("gen", ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    gen = m.text[len("/gen ") :] if not m.reply_to_message else m.reply_to_message.text
    generate = await GenerateCC(gen)
    message = await m.reply(
        generate,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Re-Gen", callback_data=f"regen|{gen}")]]
        ),
    )


@Client.on_callback_query(filters.regex(r"regen\|(.+)"))
async def regen_button_callback(client: Client, callback_query):
    gen = callback_query.data.split("|")[1]
    new_card = await GenerateCC(gen, is_regen=True)
    await callback_query.message.edit_text(
        new_card,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Re-Gen", callback_data=f"regen|{gen}")]]
        ),
    )


class GenerarTarjeta:
    def __init__(self, BIN, cantidad=10, solo_impresion=False):
        splitter = BIN.split("|")
        try:
            self.ccnum = re.sub("[^0-9a-z]", "", splitter[0].lower())
            if self.ccnum.isnumeric():
                if self.ccnum[0:1] == "3":
                    if len(self.ccnum) == 15:
                        self.ccnum = self.ccnum[0:15].replace(self.ccnum[-4:], "x")
                else:
                    if len(self.ccnum) == 16:
                        self.ccnum = self.ccnum[0:16].replace(self.ccnum[-4:], "x")
        except:
            return "INCOMPLETED DATA!"
        try:
            self.mes = splitter[1]
        except IndexError:
            self.mes = None
        try:
            self.ano = splitter[2]
        except IndexError:
            self.ano = None
        try:
            self.cvv = splitter[3]
        except IndexError:
            self.cvv = None

        self.localidad_bin = "Desconocida"
        self.RONDAS_GEN = 1000
        self.CANTIDAD_TARJETAS = cantidad
        self.lista_tarjetas = []
        self.dic_tarjetas = {}
        if self.CANTIDAD_TARJETAS >= 1:
            for i in range(10):
                tarj_creada = self.crear_tarjeta()
                self.lista_tarjetas.append(tarj_creada["datos_completos"])
                self.dic_tarjetas[i] = {
                    "numero": tarj_creada["numero_tarjeta"],
                    "fecha": tarj_creada["venc"],
                    "codigo_seg": tarj_creada["codigo_seg"],
                    "dato_completo": tarj_creada["datos_completos"],
                }
        else:
            self.crear_tarjeta()

    def __repr__(self):
        listcc = ""
        for n in self.lista_tarjetas:
            listcc += f"<code>{n}</code>\n"

        return f"{listcc}• {self.ccnum}"

    def json(self):
        return json.dumps(self.dic_tarjetas)

    def crear_tarjeta(self):
        tarjeta = {}
        tarjeta["numero_tarjeta"] = self.crear_numero(self.ccnum)
        tarjeta["codigo_seg"] = self.generar_codigo_seguridad()
        tarjeta["venc"] = self.generar_fecha_venc()
        self.string = ""
        self.string += tarjeta["numero_tarjeta"]
        self.string += "|" + tarjeta["venc"]["fecha_completa"]
        self.string += "|" + tarjeta["codigo_seg"]
        tarjeta["datos_completos"] = self.string
        return tarjeta

    def gen_aleatorio(self, BIN):
        self.ccnum = (
            self.ccnum.ljust(15, "x")
            if self.ccnum[0] == "3"
            else self.ccnum.ljust(16, "x")
        )
        numero = ""
        self.ccnum = re.sub("[^0-9]", "x", self.ccnum)
        for i in self.ccnum:
            numero += str(random.randint(0, 9)) if i.lower() == "x" else i
        return numero

    def checkear(self, cc):
        num = list(map(int, str(cc)))
        return sum(num[::-2] + [sum(divmod(d * 2, 10)) for d in num[-2::-2]]) % 10 == 0

    def crear_numero(self, BIN):
        numero = self.gen_aleatorio(BIN)
        for i in range(1, self.RONDAS_GEN):
            numero = self.gen_aleatorio(BIN)
            chk0 = self.checkear(numero)
            if chk0 and numero:
                return numero

    def generar_fecha_venc(self):
        fecha = {"anio": None, "mes": None, "fecha_completa": None}
        if self.mes and self.ano:
            fecha["mes"] = self.mes.zfill(2)
            fecha["anio"] = self.ano if len(self.ano) == 4 else f"20{self.ano}"
        else:
            fecha["mes"] = str(random.randint(1, 12)).zfill(2)
            fecha["anio"] = str(datetime.datetime.now().year + random.randint(1, 5))
        fecha["fecha_completa"] = fecha["mes"] + "|" + fecha["anio"]
        return fecha

    def generar_codigo_seguridad(self):
        if self.ccnum[0] == "3":
            return str(random.randint(1000, 9999))
        else:
            return str(random.randint(100, 999))


async def GenerateCC(extra, is_regen=False):
    if (
        extra.startswith("4")
        or extra.startswith("5")
        or extra.startswith("6")
        or extra.startswith("3")
    ):
        try:
            extra = extra.replace(":", "|").replace("/", "|").replace(" ", "|")
            gen_class = GenerarTarjeta(extra, 10, True)

            if is_regen and not ("|" in extra and len(extra.split("|")) > 2):
                gen_class.mes = None
                gen_class.ano = None

            gen = str(gen_class)
            ccs = gen.split("\n")

            msg = f"""<b>Card Generator</b>
━━━━━━━━━━━
{''.join([f'<code>{cc}</code>\n' for cc in ccs])}
━━━━━━━━━━━
<code>{extra[:6]}</code>"""

            return msg

        except Exception as e:
            return f"<b>Error:</b> {str(e)}\n<b>Example to use:</b> /gen 411116xxxx"

    else:
        return "<b>Please use a valid bin.</b>"
