import json
import random
import datetime
import re
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("gen", ["/", ",", ".", ";"]))
async def start(client: Client, m: Message):
    gen = m.text[len("/gen ") :] if m.reply_to_message.text == None else m.reply_to_message.text
    generate = await GenerateCC(gen)
    await m.reply(
            generate,
            quote=True,
        )
    
class Generar_tarjeta():
	def __init__(self,BIN, cantidad=1, solo_impresion=False):
		splitter = BIN.split('|')
		try :
			self.ccnum = re.sub("[^0-9a-z]", "", splitter[0].lower())
			if self.ccnum.isnumeric() :
				if self.ccnum[0:1] == '3':
					if len(self.ccnum) == 15 :
						self.ccnum = self.ccnum[0:15].replace(self.ccnum[-4:], 'x')
				else :
					if len(self.ccnum) == 16 :
						self.ccnum = self.ccnum[0:16].replace(self.ccnum[-4:], 'x')
		except :
			return "INCOMPLETED DATA!"
		try :
			self.mes    = splitter[1]
		except IndexError :
			self.mes = None
		try :
			self.ano    = splitter[2]
		except IndexError :
			self.ano = None
		try :
			self.cvv    = splitter[3]
		except IndexError :
			self.cvv = None

		self.localidad_bin = "Desconocida"
		self.RONDAS_GEN = 1000
		self.CANTIDAD_TARJETAS = cantidad
		self.lista_tarjetas = []
		self.dic_tarjetas = {}
		if self.CANTIDAD_TARJETAS >= 1:
			for i in range(0, 10):
				tarj_creada = self.crear_tarjeta()
				self.lista_tarjetas.append(tarj_creada["datos_completos"])
				#Plantilla dato
				self.dic_tarjetas[i] = {
						"numero":tarj_creada["numero_tarjeta"],
						"fecha":tarj_creada["venc"],
                        "codigo_seg":tarj_creada["codigo_seg"],
						"dato_completo":tarj_creada["datos_completos"]
				}
		else:
			self.crear_tarjeta()

	def __repr__(self) :
		listcc = ""
		for n in self.lista_tarjetas:
			listcc+=f"<code>{n}</code>\n"

		return f"{listcc}• {self.ccnum}"

	def json(self):
		return json.dumps(self.dic_tarjetas)

	def crear_tarjeta(self):
		tarjeta = {}
		tarjeta["numero_tarjeta"] = self.crear_numero(self.ccnum)
		tarjeta["codigo_seg"] 	  = self.generar_codigo_seguridad()
		tarjeta["venc"]			  = self.generar_fecha_venc()
		self.string = ""
		self.string += tarjeta["numero_tarjeta"]
		self.string += "|" + tarjeta["venc"]["fecha_completa"]
		self.string += "|" + tarjeta["codigo_seg"]
		tarjeta["datos_completos"] = self.string
		return tarjeta
		
	def gen_aleatorio(self, BIN):
		self.ccnum = self.ccnum.ljust(15, 'x') if self.ccnum[0] == '3' else self.ccnum.ljust(16, 'x')
		numero = ""
		self.ccnum = re.sub("[^0-9]", "x", self.ccnum)
		for i in self.ccnum:
			numero+=str(random.randint(0,9)) if i.lower() == "x" else i
		return numero
		
	def checkear(self, cc):
		num = list((map(int, str(cc))))
		return sum(num[::-2] + [sum(divmod(d * 2, 10)) for d in num[-2::-2]]) % 10 == 0

	def crear_numero(self, BIN):
		numero = self.gen_aleatorio(BIN)
		for i in range(1,self.RONDAS_GEN):
			numero = self.gen_aleatorio(BIN)
			chk0 = self.checkear(numero)
			if(chk0 and numero):
				return numero
		
	def generar_fecha_venc(self):
		fecha = {
			"anio": None,
			"mes": None,
			"fecha_completa": None
		}
		def gen_anio():
			try:
				self.ano = re.sub("[^0-9]", " ", self.ano)
				BinCheck = int(self.ccnum[0:1])
				if 3 <= int(BinCheck) <= 6 :
					if 4 <= int(BinCheck) <= 6 :
						matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", self.ano)
						ano = matchano[0]
						if len(ano) == 2 :
							ano = f'20{ano}'
						return ano
					elif int(BinCheck) == 3 :
						matchano = re.findall(r"\b(3[0-1]|2[2-9]|202[2-9]|203[0-1])\b", self.ano)
						ano = matchano[0]
						if len(ano) == 2 :
							ano = f'20{ano}'
						return ano
			except :
					anio_actual = datetime.datetime.now().year
					return anio_actual + random.randint(1,9)

		fecha["anio"] = str(gen_anio())

		def gen_mes():
			try:
				self.mes = re.sub("[^0-9]", " ", self.mes)
				BinCheck = int(self.ccnum[0:1])
				if 3 <= int(BinCheck) <= 6 :
					if 4 <= int(BinCheck) <= 6 :
						matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", self.mes)
						mes = matchmes[0]
						return mes
					elif int(BinCheck) == 3 :
						matchmes = re.findall(r"\b(0[1-9]|1[0-2])\b", self.mes)
						mes = matchmes[0]
						return mes
			except :
				mes = random.randint(1,12)
				if (mes > 9):
					return str(mes)
				else:
					return "0"+str(mes)	
		
		fecha["mes"] = gen_mes()
		fecha["fecha_completa"] = fecha["mes"] + "|" + fecha["anio"]
		return fecha
		
	def generar_codigo_seguridad(self):
		if self.ccnum[0] == '3':
			if self.cvv != None :
				if re.search(r'[0-9x]', self.cvv.lower()) :
					if self.cvv.lower().find("x") >= 0:
						self.cvv = re.sub("[^0-9a-z]", "x", self.cvv.lower())
						self.cvv = re.sub(r'[a-z]', "x", self.cvv.lower())
						self.cvv = self.cvv.ljust(3, 'x')
						numero = ""
						for i in self.cvv:
							numero+=str(random.randint(0,9)) if i.lower() == "x" else i
						return numero[0:4]
					else :
						self.cvv = re.sub("[^0-9a-z]", "x", self.cvv.lower())
						self.cvv = re.sub(r'[a-z]', "x", self.cvv.lower())
						self.cvv = self.cvv.ljust(3, 'x')
						numero = ""
						for i in self.cvv:
							numero+=str(random.randint(0,9)) if i.lower() == "x" else i
						return numero[0:4]
			return str(random.randint(1001,9998))

		else:
			if self.cvv != None :
				if re.search(r'[0-9x]', self.cvv.lower()) :
					if self.cvv.lower().find("x") >= 0:
						self.cvv = re.sub("[^0-9a-z]", "x", self.cvv.lower())
						self.cvv = re.sub(r'[a-z]', "x", self.cvv.lower())
						self.cvv = self.cvv.ljust(3, 'x')
						numero = ""
						for i in self.cvv:
							numero+=str(random.randint(0,9)) if i.lower() == "x" else i
						return numero[0:3]
					else :
						self.cvv = re.sub("[^0-9a-z]", "x", self.cvv.lower())
						self.cvv = re.sub(r'[a-z]', "x", self.cvv.lower())
						self.cvv = self.cvv.ljust(3, 'x')
						numero = ""
						for i in self.cvv:
							numero+=str(random.randint(0,9)) if i.lower() == "x" else i
						return numero[0:3]
			return str(random.randint(101,998))

		

async def GenerateCC(extra):
    try:
        extra = extra.replace(":", "|").replace("/", "|").replace(" ", "|")
        if int(extra[0])==3:
            cant = 15
        else:
            cant = 16

        gen = str(Generar_tarjeta(extra, cant, True))
        ccs = gen.split("\n")
        msg = f"""Card Generator
━━━━━━━━━━━
<code>{ccs[0]}</code>
<code>{ccs[1]}</code>
<code>{ccs[2]}</code>
<code>{ccs[3]}</code>
<code>{ccs[4]}</code>
<code>{ccs[5]}</code>
<code>{ccs[6]}</code>
<code>{ccs[7]}</code>
<code>{ccs[8]}</code>
<code>{ccs[9]}</code>
━━━━━━━━━━━
{extra[:6]}"""

        return msg


    except:
        return "<b>Example to use:</b> /gen 411116xxxx"