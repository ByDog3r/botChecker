INCORRECT_CARD = 'Invalid card details: CC Number'
EMPTY_CARD = 'Invalid card details: Empty card'
SHORT_CARD = 'Invalid card details: CC length is not valid'
INCORRECT_MONTH = 'Invalid card details: MONTH'
INCORRECT_YEAR = 'Invalid card details: YEAR'
INCORRECT_CVV = 'Invalid card details: CVV'
import re
import datetime
from luhn import verify

def getstr(text:str, izq:str, der:str) -> str:
    return text.split(izq)[1].split(der)[0]

def get_cc(data):#Falta arreglar cosas
    input = re.findall(r"[0-9]+", data)
    try:
        if len(input) == 0:
            raise UnicodeError
        cc = input[0]
        mes = input[1]
        ano = input[2]
        ano1 = input[2]
        cvv = input[3]
        if len(input) == 3:
            cc = input[0]
            mes = input[1][:2]
            ano = input[1][2:]
            ano1 = input[1][2:]
            cvv = input[2]
        if len(mes) > 2:
            ano = cvv
            cvv = mes
            mes = ano1
    except UnicodeError:
        print(input)
        return EMPTY_CARD
    except Exception:
        return EMPTY_CARD
    else:
        if int(cc[0]) not in [3, 4, 5, 6]:
            return INCORRECT_CARD
        cc = cc.strip()
        if int(cc[0]) == 3 and len(cc) != 15:
            return SHORT_CARD
        elif int(cc[0]) in [4, 5, 6] and len(cc) != 16:
            return SHORT_CARD
        elif not verify(cc):
            return INCORRECT_CARD
        elif not mes.isdigit() or (len(mes) not in [1, 2] or (len(mes) == 2 and (int(mes) > 12 or int(mes) < 1)) or (len(mes) == 1 and (int(mes) < 1 or int(mes) > 12))):
            return INCORRECT_MONTH
        elif int(len(ano)) not in [2, 4] or len(ano) < 2 or len(ano) == 2 and ano < '23' or len(ano) == 4 and ano < '2023' or len(ano) == 2 and ano > '30' or len(ano) == 4 and ano > '2030' or len(ano) > 4 or len(ano) == 3:
            return INCORRECT_YEAR
        elif int(cc[0]) == 3 and len(cvv) != 4 or len(cvv) < 3 or len(cvv) > 4:
            return INCORRECT_CVV
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        year = int(ano) 
        month = int(mes)
        if year == current_year and month < current_month:
            return INCORRECT_MONTH

        else:
            if len(mes) == 1:
                mes = '0' + str(mes)
            if len(ano) == 2:
                ano = '20' + str(ano)
            return [cc, mes, ano, cvv]
        
