from whois import whois
from requests import get
from requests import get
from bs4 import BeautifulSoup

def check_cloudflare(site:str):
    response = get(site)
    if 'cf-ray' in response.headers:
        return True
    else:
        return False
    
def check_captcha(url:str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        r = get(url, headers=headers, timeout=3)
        soup = BeautifulSoup(r.text, 'html.parser')
        if len(soup.select('form[action*="/captcha/"]')) > 0:
            return True
        else:
            return False
    except:
        return False      


def whois_lookup(page):
    req = whois(page)

    if check_cloudflare(page):
        cloud_msg = "This page has cloudflare"

    else:
        cloud_msg = "This page doesn't has cloudflare"

    if check_captcha(page):
        captcha_msg = "This page has captcha"

    else:
        captcha_msg = "This page doesn't has captcha"

    try:

        msg = f"""╔═══════════════════════╗
╟ • [ 鰲 ] 𝑽𝒂𝒍𝒊𝒅 𝒑𝒂𝒈𝒆.
╟═══════════════════════╝
╟ •「 夾 」𝑫𝒐𝒎𝒂𝒊𝒏 𝑵𝒂𝒎𝒆: {req.domain_name}
╟ •「 夾 」𝑶𝑹𝑮: {req.org}
╟ •「 夾 」𝑹𝒆𝒈𝒊𝒔𝒕𝒓𝒂𝒓: {req.registrar}
╟═══════════════════════╗
╟ • [ 鰲 ] 𝑨𝒅𝒅𝒓𝒆𝒔𝒔
╟═══════════════════════╝
╟ •「 夾 」𝑨𝒅𝒅𝒓𝒆𝒔𝒔: {req.address}
╟ •「 夾 」𝑪𝒊𝒕𝒚: {req.city}
╟ •「 夾 」𝑺𝒕𝒂𝒕𝒆: {req.state}
╟ •「 夾 」𝑹𝒆𝒈 𝑷𝒐𝒔𝒕𝑪𝒐𝒅𝒆: {req.registrant_postal_code}
╟ •「 夾 」𝑪𝒐𝒖𝒏𝒕𝒓𝒚: {req.country}
╟═══════════════════════╗
╟ • [ 鰲 ] 𝑰𝑵𝑭𝑶
╟═══════════════════════╝
╟ •「 夾 」𝑬𝑴𝑨𝑰𝑳𝑺: \n{req.emails}
╟ •「 夾 」Name server: \n{req.name_servers}
╟═══════════════════════╗
╟ • [ 鰲 ] 𝑫𝒂𝒕𝒆𝒔
╟═══════════════════════╝
╟ •「 夾 」𝑪𝒓𝒆𝒂𝒕𝒊𝒐𝒏 𝒅𝒂𝒕𝒆: {req.creation_date}
╟ •「 夾 」𝑬𝒙𝒑𝒊𝒓𝒂𝒕𝒊𝒐𝒏 𝒅𝒂𝒕𝒆: {req.expiration_date}
╟ •「 夾 」𝑳𝒂𝒔𝒕 𝑼𝒑𝒅𝒂𝒕𝒆: {req.updated_date}
{cloud_msg}
{captcha_msg}
<b>╚━━━━━━「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」━━━━━━╝</b>"""

    except:
        pass

    return msg
