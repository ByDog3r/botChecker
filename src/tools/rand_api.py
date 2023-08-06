from requests import get

class GenerateInformation:
    def __init__(self):
        self.API = "Your-Api-should-be-here"
        self.headers = {"X-Api-Key": "53b4353f9f744254ac8c061d484f341a"}
        self.params = '{"only-if":"is-require"}'

    def GetName(self):
        self.API = "https://randommer.io/api/Name"
        self.params = {"nameType": "fullname", "quantity": 1}
        response = get(self.API, headers=self.headers, params=self.params)
        return response.json()

    def GetAddress(self, culture):
        self.API = "https://randommer.io/api/Misc/Random-Address"
        self.params = {"number": 1, "culture": culture}

        response = get(self.API, headers=self.headers, params=self.params).json()

        return response

    def FakeIdentity(self, CountryCode):
        name = self.GetName()
        address = self.GetAddress(CountryCode)

        return name[0], address