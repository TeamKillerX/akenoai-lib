# You can use pyrogram or telethon

# if you are using akenoai[fast]

import akenoai as js


class SangMata:
    API_BASE = "https://randydev-ryu-js.hf.space/api/v2"
    API_KEYS = "your_api_key"

    def __init__(self):
        pass

    async def sangmata_tracker(self, **data):
        url = f"{self.API_BASE}/sangmata/tracker"
        return await js.fetch(
            url,
            post=True,
            headers={"x-api-key": self.API_KEYS},
            json=data,
            return_json=True
        )

    async def sangmata_tracker_check(self, user_id: int):
        url = f"{self.API_BASE}/sangmata/tracker/{user_id}"
        return await js.fetch(
            url,
            post=False,
            headers={"x-api-key": self.API_KEYS},
            return_json=True
        )

sg = SangMata()

async def example_track(c, m):
    response = await sg.sangmata_tracker(
        user_id=m.from_user.id,
        first_name=m.from_user.first_name,
        username=m.from_user.username if m.from_user else None,
    )
    print(response)

async def example_incoming(c, m):
    response = await sg.sangmata_tracker_check(user_id=m.from_user.id)
    print(response)


# if you are using requests (without akenoai)
import requests


class SangMata:
    API_BASE = "https://randydev-ryu-js.hf.space/api/v2"
    API_KEYS = "your_api_key"

    def __init__(self):
        pass

    def _make_requests(url: str, json=None, post=False):
        return requests.post(
            url,
            json=json,
            headers={"x-api-key": self.API_KEYS}
        ) if post else requests.get(
            url,
            json=json,
            headers={"x-api-key": self.API_KEYS}
        )

    def sangmata_tracker(self, **data):
        url = f"{self.API_BASE}/sangmata/tracker"
        return self._make_requests(url, post=True, json=data).json()

    def sangmata_tracker_check(self, user_id: int):
        url = f"{self.API_BASE}/sangmata/tracker/{user_id}"
        return self._make_requests(url, post=False).json()

sg = SangMata()

def example_track2(c, m):
    response = sg.sangmata_tracker(
        user_id=m.from_user.id,
        first_name=m.from_user.first_name,
        username=m.from_user.username if m.from_user else None,
    )
    print(response)

def example_incoming2(c, m):
    response = sg.sangmata_tracker_check(user_id=m.from_user.id)
    print(response)
