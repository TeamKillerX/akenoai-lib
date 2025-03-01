from base64 import b64decode as m

import wget  # type: ignore

from akenoai.reqs import async_search


class PornoHub:
    def __init__(self, key=..., base_api_dev: str = "https://private-akeno.randydev.my.id"):
        if key is Ellipsis:
            self.key = m("cmFuZGlnaXRodWIzNTY=").decode("utf-8")
        elif not key:
            raise ValueError("API key must be provided!")
        else:
            self.key = key
        self.base_api_dev = base_api_dev
        self.headers = {"x-akeno-key": str(self.key)}

    def set_key(self, new_key: str):
        self.key = new_key

    def show_key(self):
        return f"The API key is: {self.key}"

    async def x_search(self, query=None):
        url = f"{self.base_api_dev}/akeno/xnxxsearch-v2?query={query}"
        res = await async_search(url, headers=self.headers, re_json=True)
        results = res["randydev"]["results"]
        if res["randydev"]["results"] is None and results is None:
            return None
        y = res["randydev"]["results"][0]
        link = y["link"]
        title = y["title"]
        return [link, title, results]

    async def x_download(self, query=None, url=None, is_stream=False):
        if is_stream and url:
            url_ = f"{self.base_api_dev}/akeno/xnxx-dl-v2?link={url}"
            response = await async_search(url_, headers=self.headers, re_json=True)
            file_path = wget.download(response["randydev"]["results"]["url"])
            thumb = wget.download(response["randydev"]["results"]["thumb"])
            title = response["randydev"]["results"].get("title", "Powered by Randydev")
            return file_path, thumb, title
        else:
            schub = await self.x_search(query=query)
            url_dl = f"{self.base_api_dev}/akeno/xnxx-dl-v2?link={schub[0]}"
            response = await async_search(url_dl, headers=self.headers, re_json=True)
            file_path = wget.download(response["randydev"]["results"]["url"])
            thumb = wget.download(response["randydev"]["results"]["thumb"])
            title = response["randydev"]["results"].get("title", "Powered by Randydev")
            return file_path, thumb, title
