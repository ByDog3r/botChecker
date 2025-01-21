from src.extras.py_adyenenc import encrypt as encryptor

def encrypter(ccs, key):
    splitter = ccs.split('|')
    ccnum    = splitter[0]
    mes      = splitter[1]
    ano      = splitter[2]
    cvv      = splitter[3] 
    ADYEN_KEY = f"10001|{key}"

    # changing adyen version, default is set to _0_1_18
    enc = encryptor(ADYEN_KEY)
    enc.adyen_version = '_0_1_25'
    # or set adyen version when creating the object:
    enc = encryptor(adyen_public_key=ADYEN_KEY, adyen_version='_0_1_25')

    # changing adyen key after creating encryptor
    enc = encryptor(ADYEN_KEY)
    # do some stuff with that adyen key...
    enc.adyen_public_key = f"10001|{key}"
    # do some stuff with new adyen key...
    # generating card data
    enc = encryptor(ADYEN_KEY)
    card = enc.encrypt_card(card=ccnum, cvv=cvv, month=mes, year=ano)
    return card['card'], card['month'], card['year'], card['cvv']