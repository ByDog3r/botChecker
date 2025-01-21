from requests import get
from lxml import html
import json

API = ["http://ip-api.com/json/", "https://scamalytics.com/ip/"]

def ip_dox(ip):
  
    head = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"
    }

    data = get(API[0]+ip).json()
    fraud_parser = html.fromstring(get(API[1]+ip, headers=head).text)
      
    risk_lvl = fraud_parser.xpath("""//div[@class="panel_title high_risk"]/text()""")
    fraud_score = fraud_parser.xpath("""//div[@class="score"]/text()""")
    
    msg = f""" <b>𝑰𝑷-»</b> <code>{ip}</code>
━━━━━━━━━━━
┌ 𝑪𝒊𝒕𝒚: {data['city']}
├ 𝑹𝒆𝒈𝒊𝒐𝒏: {data['region']}
├ 𝑪𝒐𝒖𝒏𝒕𝒓𝒚: {data['country']}
└ 𝒁𝒊𝒑 𝑪𝒐𝒅𝒆: {data['zip']}

┌ 𝑹𝒊𝒔𝒌 𝒍𝒆𝒗𝒆𝒍: {risk_lvl[0]}
└ <b>{fraud_score[0]}</b>

├ 𝑰𝑺𝑷: {data['isp']}
├ 𝑨𝑺𝑵: {data['as']}
└ <a href='https://maps.google.com/?q={str(data['lat'])},{str(data['lon'])}'> 𝑮𝒐𝒐𝒈𝒍𝒆 𝑴𝒂𝒑𝒔 </a>"""

    return msg