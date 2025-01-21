import requests as r
import re

def chatgpt(prompt):
        url = "https://aigencycms.polartemplates.com/php/api.php"
        data = {
                "prompt": prompt,
                "ai_id": 2
        }
        resp =  r.post(url, data=data)
        convo =  re.findall(r'content":"([^"]+)"', resp.text)
        return "".join(convo)

