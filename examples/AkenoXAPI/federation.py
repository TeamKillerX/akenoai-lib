import akenoai as js


class Federation:
    API_BASE = "https://randydev-ryu-js.hf.space/api/v2"
    API_KEYS = "your_api_key"

    def __init__(self):
        pass

    async def federation_newfed(self, **data):
        url = f"{self.API_BASE}/federation/newfed"
        return await js.fetch(
            url,
            post=True,
            json=data,
            headers={"x-api-key": self.API_KEYS}
        )
    async def federation_subfed(self, **data):
        url = f"{self.API_BASE}/federation/subfed"
        return await js.fetch(
            url,
            post=True,
            json=data,
            headers={"x-api-key": self.API_KEYS}
        )

    async def federation_ban(self, **data):
        pass

# check out: https://t.me/RendyProjects/2537
