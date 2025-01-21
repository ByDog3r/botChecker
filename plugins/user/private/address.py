import cloudscraper
from bs4 import BeautifulSoup
from time import perf_counter
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatAction
from src.assets.functions import antispam
from src.assets.connection import Database

@Client.on_message(filters.command(["faker", "fake"], ["/", ",", ".", ";", "-"]))
async def start(client: Client, m: Message):
    await client.send_chat_action(m.chat.id, action=ChatAction.TYPING)
    user_id = m.from_user.id
    with Database() as db:
        if not db.IsPremium(user_id):
            return await m.reply("<b>You are not premium</b>", quote=True)
        user_info = db.GetInfoUser(m.from_user.id)
    antispam_result = antispam(user_id, user_info["ANTISPAM"])
    if antispam_result != False:
        return await m.reply(
            f"Please wait <code>{antispam_result}'s</code>", quote=True
        )
    try:
        name = m.from_user.first_name
        country_code = m.text.split(" ", 1)[1] if not m.reply_to_message else m.reply_to_message.text
        address = await get_fake_data(country_code, user_id, name)
        await m.reply(
            address,
            parse_mode=ParseMode.HTML,
        )
    except:
        msg = """<b>Countries available:</b>
\t┌  <code>AR</code> - Argentina
\t├ <code>AU</code> - Australia
\t├ <code>CA</code>  - Canada
\t├ <code>MX</code>  - Mexico
\t├ <code>US</code> - United States
\t├ <code>FR</code>  - France
\t├ <code>JP</code>  - Japan
\t├ <code>DE</code>  - Germany
\t├ <code>IT</code>  - Italy
\t├ <code>PE</code>  - Peru
\t├ <code>RU</code>  - Russia
\t├ <code>UK</code> - United Kingdom
\t└ <code>ES</code>  - Spain
━━━━━━━━━━━
<b>Example to use:</b> /faker usa
"""
    await m.reply(msg)


async def get_fake_data(country_code, user_id, u_name):


    init_time = perf_counter()
    url = f'https://www.fakexy.com/fake-address-generator-{country_code}'
    scraper = cloudscraper.create_scraper()
    req = scraper.get(url)
    req.encoding = 'utf-8'

    soup = BeautifulSoup(req.text, 'html.parser')

    title_tag = soup.find('h1', class_='titleh')
    title = title_tag.text.strip() if title_tag else 'Title not found'


    address_table = soup.find('table', class_='table')
    address_data = {}
    if address_table:
        for row in address_table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].text.strip()
                value = cols[1].text.strip()
                address_data[key] = value
    else:
        address_data = {}

    profile_section = soup.find('h1', string='Matched person profile')
    profile_data = {}
    if profile_section:
        profile_table = profile_section.find_next('table', class_='table')
        if profile_table:
            for row in profile_table.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    profile_data[key] = value
        else:
            profile_data = {}
    else:
        profile_data = {}

    data = {
        'title': title,
        'address': address_data,
        'profile': profile_data
    }

    street = data['address'].get('Street', 'N/A')
    city = data['address'].get('City/Town', 'N/A')
    state = data['address'].get('State/Province/Region', 'N/A')
    zip_code = data['address'].get('Zip/Postal Code', 'N/A')
    phone_number = data['address'].get('Phone Number', 'N/A')
    latitude = data['address'].get('Latitude', 'N/A')
    longitude = data['address'].get('Longitude', 'N/A')

    full_name = data['profile'].get('Full Name', 'N/A')
    gender = data['profile'].get('Gender', 'N/A')
    birthday = data['profile'].get('Birthday', 'N/A')
    ssn = data['profile'].get('Social Security Number', 'N/A')

    final_time = perf_counter() - init_time

    msg = f"""<b>Fake Data [{country_code}]</b>
━━━━━━━━━━━━
┌ <b>Name</b> <code>{full_name}</code>
├ <b>Gender</b> <code>{gender}</code>
├ <b>Birthday</b> <code>{birthday}</code>
├  <b>Social Security Number</b> <code>{ssn}</code>
└ <b>Phone Number</b> <code>{phone_number}</code>

┌ <b>Street</b> <code>{street}</code>
├ <b>City</b> <code>{city}</code>
├ <b>State</b> <code>{state}</code>
└ <b>Zipcode</b> <code>{zip_code}</code>
━━━━━━━━━━━━
Time : {final_time:0.2}
Checked by: <a href='tg://user?id={user_id}'>{u_name}</a>"""
    return msg
