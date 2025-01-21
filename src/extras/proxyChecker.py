#       Script made by @ByDog3r 
# All rights reserver -- https://t.me/ByDog3r

import requests as r 

APIS = {
    "carbon_proxies": ["http://sslproxies.org/", "https://free-proxy-list.net/", "https://us-proxy.org/", "https://socks-proxy.net/"],
}
        
def getStr(text:str, a:str, b:str) -> str:
    return text.split(a)[1].split(b)[0]

for site in APIS["carbon_proxies"]:
    response = r.get(site)
    clean_proxies = getStr(response.text, '<textarea class="form-control" readonly="readonly" rows="12" onclick="select(this)">', '</textarea></div>')
    
    with open("proxies.txt", 'w+') as f:
        f.write(clean_proxies)