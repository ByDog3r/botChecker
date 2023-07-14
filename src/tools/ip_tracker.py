from requests import get
from lxml import html
import json

API = ["http://ip-api.com/json/", "https://scamalytics.com/ip/"]


def ip_dox(ip):
    IP=ip
  
    head = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"
    }
    
  
    try:
        data = get(API[0]+IP).json()
        fraud_parser = html.fromstring(get(API[1]+IP, headers=head).text)
      
        risk_lvl = fraud_parser.xpath("""//div[@class="panel_title high_risk"]/text()""")
        fraud_score = fraud_parser.xpath("""//div[@class="score"]/text()""")
    
        msg = f"""╔═══════════════════════╗
╟ • [ 📍 ] 𝑰𝑷-» {IP}
╟═══════════════════════╝
╟ •「火」𝑹𝒊𝒔𝒌 𝒍𝒆𝒗𝒆𝒍: {risk_lvl[0]}
╟ •「点」<b>{fraud_score[0]}</b>
╟ •「德」𝑪𝒊𝒕𝒚: {data['city']}
╟ •「点」𝑹𝒆𝒈𝒊𝒐𝒏: {data['region']}
╟ •「火」𝑪𝒐𝒖𝒏𝒕𝒓𝒚: {data['country']}
╟ •「德」𝒁𝒊𝒑 𝑪𝒐𝒅𝒆: {data['zip']}
╟ •「点」𝑰𝑺𝑷: {data['isp']}
╟ •「点」𝑨𝑺𝑵:{data['as']}
╟════════════════════════
╟ •「德」𝑮𝒐𝒐𝒈𝒍𝒆 𝑴𝒂𝒑𝒔: https://maps.google.com/?q={str(data['lat'])},{str(data['lon'])}
<b>╚━━━━━━「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」━━━━━━╝</b>"""


    except:
        msg = f"""╔═══════════════════════╗
╟ •「火」𝑰𝒏𝒗𝒂𝒍𝒊𝒅 𝑰𝑷 -» {IP}
╟═════════「 𝒖𝒔𝒐 」═════════╝
╟ •「点」<code>.ip xxx.xx.xxx.xxx</code>
<b>╚━━━━━━「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」━━━━━━╝</b>"""
        
    return msg