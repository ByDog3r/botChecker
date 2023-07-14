from requests import get
import json

class GenerateInformation():

    def __init__(self):
        self.API = "Your-Api-should-be-here"
        self.headers = {"X-Api-Key":"53b4353f9f744254ac8c061d484f341a"}
        self.params = '{"only-if":"is-require"}'

    def GetName(self):

        self.API = "https://randommer.io/api/Name" 
        self.params = {
                "nameType":"fullname",
                "quantity":1
                }
        response = get(self.API, headers=self.headers, params=self.params)
        return response.json()


    def GetAddress(self, culture):

        self.API = "https://randommer.io/api/Misc/Random-Address"
        self.params = {
                "number":1,
                "culture":culture
                }

        response = get(self.API, headers=self.headers, params=self.params).json()
        
        return response

    def FakeIdentity(self, CountryCode):

        name = self.GetName()
        address = self.GetAddress(CountryCode)

        return name[0], address


async def genAddress(update, AreaCode, ParseMode, ChatAction):

    await update.message.reply_chat_action(ChatAction.TYPING)
    try:
        try:
            if AreaCode.args[0].lower() == "usa":
                AreaCode = "en"
            elif AreaCode.args[0].lower() == "esp":
                AreaCode = "es"
            elif AreaCode.args[0].lower() == "ger":
                AreaCode = "de"
            elif AreaCode.args[0].lower() == "can":
                AreaCode = "fr_CA"
            elif AreaCode.args[0].lower() == "mx":
                AreaCode = "es_MX"
            elif AreaCode.args[0].lower() == "aus":
                AreaCode = "en_AU"
            elif AreaCode.args[0].lower() == "br":
                AreaCode = "pt_BR"
            else: 
                AreaCode = AreaCode.args[0].lower()
            name, address = GenerateInformation().FakeIdentity(AreaCode)
            address = str(address[0]).split(", ")
        
            try:
                int(address[3])
                msg = f"""╔═══════════════════════╗
╟ • [ 📍 ] Name -» <code>{name}</code>
╟═══════════════════════╝
╟ •「火」Street: <code>{address[0]}</code>
╟ •「点」City: <code>{address[4]}</code>
╟ •「德」State: <code>{address[5]}</code>
╟ •「点」Zipcode: <code>{address[3]}</code>
╟ •「火」Country: <code>{address[6]}</code>
<b>╚━━━━━━「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」━━━━━━╝</b>"""


            except:
                msg = f"""╔═══════════════════════╗
╟ • [ 📍 ] Name -» <code>{name}</code>
╟═══════════════════════╝
╟ •「火」Street: <code>{address[0]}</code>
╟ •「点」City: <code>{address[3]}</code>
╟ •「德」State: <code>{address[4]}</code>
╟ •「点」Zipcode: <code>{address[2]}</code>
╟ •「火」Country: <code>{address[5]}</code>
<b>╚━━━━━━「@𝑩𝒚𝑪𝒉𝒆𝒄𝒌𝒆𝒓」━━━━━━╝</b>"""

        except:
            msg = """<b>Countries available:</b>
\t<code>usa</code> - United States
\t<code>can</code> - Canada
\t<code>mx</code>  - Mexico
\t<code>fr</code>  - France
\t<code>ger</code> - Germany
\t<code>ru</code>  - Russia
\t<code>ja</code>  - Japan
\t<code>ge</code>  - Georgia
\t<code>it</code>  - Italy
\t<code>ko</code>  - Korea
\t<code>nl</code>  - Netherlands
\t<code>aus</code> - Australia
\t<code>br</code>  - Brazil
━━━━━━━━━━━
<b>Example to use:</b> /faker usa
"""

        await update.message.reply_text(msg, reply_to_message_id=update.message.message_id, parse_mode=ParseMode)

    except:
        await update.message.reply_text("<b> Enter a valid Area code.</b>", reply_to_message_id=update.message.message_id, parse_mode=ParseMode)
