from requests import get
from bs4 import BeautifulSoup as soup

API = (# ======= RRSS ========= 
       'https://facebook.com/', 
       "https://instagram.com/", 
       "https://twitter.com/",
       "https://www.github.com/",
       "https://www.youtube.com/@",
       "https://reddit.com/user/",
       "https://www.linkedin.com/in/",
       # ======== Games =========
       "https://socialclub.rockstargames.com/member/",
        "https://my.playstation.com/profile/",
       "https://steamcommunity.com/id/",
       "https://www.roblox.com/user.aspx?username=",
       # ======== Misc ==========
       "https://open.spotify.com/user/",
       "https://www.wattpad.com/user/")

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

class Sherlock:

    def __init__(self, user, api, company_name):
        self.Usr = user
        self.Company_name = company_name
        self.API = api

    def whois(self):
        req = get(self.API+self.Usr, headers=headers)

        if req.status_code == 200:
            prf = soup(req.text, 'html.parser')
            if "The specified profile could not be found." in req.text or "Sorry, nobody on Reddit goes by that name." in req.text or 'no_js' in req.text or '<title>Instagram</title>' in req.text:
                self.response = f"<b>{self.Company_name} not found.</b>"
            else:
                self.response = f"<a href='{self.API+self.Usr}'><b>{self.Company_name} found ✅.</b></a>"

        else:
            self.response = f"<b>{self.Company_name} not found.</b>"

        return self.response
    

def sherlock(user):

    usr = user
    # try:
    FB = Sherlock(usr, API[0], "Facebook").whois()
    IG = Sherlock(usr, API[1], "Instagram").whois()
    TW = Sherlock(usr, API[2], "Twitter").whois()
    GT = Sherlock(usr, API[3], "Github").whois()
    YT = Sherlock(usr, API[4], "YouTube").whois()
    RD = Sherlock(usr, API[5], "Reddit").whois()
    LK = Sherlock(usr, API[6], "Linkedin").whois()
    #RG = Sherlock(usr, API[7], "RockstarGames").whois()
    #PS = Sherlock(usr, API[8], "PlayStation").whois()
    ST = Sherlock(usr, API[9], "Steam").whois()
    RB = Sherlock(usr, API[10], "Roblox").whois()
    SP = Sherlock(usr, API[11], "Spotify").whois()
    WT = Sherlock(usr, API[12], "Wattpad").whois()


    msg = f"""<b>RRSS FOUND:</b> {usr}
━━━━━━━━━━━
┌ {FB}
├ {IG}
├ {TW}
├ {GT}
├ {YT}
├ {RD}
└ {LK}

┌{ST}
└ {RB}

┌{SP}
└ {WT} """
        
    
    # except:
        # msg = "⚠️ An error ocurred, please try again."
        
    return msg
