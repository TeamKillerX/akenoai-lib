import asyncio
import os
from base64 import b64decode as m

import aiohttp
import httpx
import requests
import wget


class DictToObj:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObj(value))
            elif isinstance(value, list):
                setattr(self, key, [DictToObj(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"{self.__dict__}"


class AkenoPlus:
    def __init__(self, key=..., api_endpoint: str = "https://private-akeno.randydev.my.id"):
        if key is Ellipsis:
            self.key = m("cmFuZGlnaXRodWIzNTY=").decode("utf-8")
        elif not key:
            raise ValueError("API key must be provided!")
        else:
            self.key = key
        self.api_endpoint = api_endpoint
        self.headers = {"x-akeno-key": str(self.key)}

    def api_akenoai(self, method):
        if not method:
            raise ValueError("Method parameter cannot be None or empty")
        return f"{self.api_endpoint}/{method}"

    def set_key(self, new_key: str):
        self.key = new_key

    def show_key(self):
        return f"The API key is: {self.key}"

    async def download_now(self, data):
        return wget.download(data)

    async def clean(self, file_path: str):
        try:
            os.remove(file_path)
        except OSError as e:
            return f"Error removing file {file_path}: {e}"

    async def terabox(self, link=None):
        url = self.api_akenoai(f"akeno/terabox-v1?link={link}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()

    async def terabox_v2(self, link=None):
        url = self.api_akenoai(f"akeno/terabox-v2?link={link}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()

    async def chatgpt_old(self, query=None):
        url = self.api_akenoai("ryuzaki/chatgpt-old")
        payload = {"query": query}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return await response.json()

    async def chatgpt_mode_web(self, query=None, **params):
        url = self.api_akenoai("api/akeno-ai-web")
        combined_params = {"query": query}
        combined_params.update(params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=combined_params) as response:
                return await response.json()

    async def sites_torrens_all(self):
        url = self.api_akenoai("akeno/sites_torrens_all")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def search_for_torrents(self, **params):
        url = self.api_akenoai("akeno/search_for_torrents")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def get_torrent_from_url(self, **params):
        url = self.api_akenoai("akeno/get_torrent_from_url")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def get_recent(self, **params):
        url = self.api_akenoai("akeno/get_recent")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def get_category(self, **params):
        url = self.api_akenoai("akeno/get_category")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()

    async def paal_see(self, files_open=None, **params):
        url = self.api_akenoai("akeno/paal-see")
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field(
                'file',
                open(files_open, 'rb'),
                filename=os.path.basename(files_open),
                content_type='application/octet-stream'
            )
            async with session.post(url, data=form_data, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Error occurred: {response.status}")
                return await response.json()

    async def remini_enhancer(self, files_open=None):
        url = self.api_akenoai("api/v2/remini/enhancer")
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field(
                'file',
                open(files_open, 'rb'),
                filename=os.path.basename(files_open),
                content_type='application/octet-stream'
            )
            async with session.post(url, data=form_data) as response:
                if response.status != 200:
                    raise Exception(f"Error occurred: {response.status}")
                file_path = "enchancer.jpg"
                with open(file_path, "wb") as file:
                    file.write(await response.read())
                return file_path

    async def paal_text_to_image(self, **params):
        url = self.api_akenoai("akeno/paal-text-to-image")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params, headers=self.headers) as response:
                return await response.json()

    async def google_video_to_text(self, files_open=None, **params):
        url = self.api_akenoai("api/v2/google/video-to-text")
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field(
                'file',
                open(files_open, 'rb'),
                filename=os.path.basename(files_open),
                content_type='application/octet-stream'
            )
            async with session.post(url, data=form_data, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Error occurred: {response.status}")
                return await response.json()

    async def google_image_to_text(self, files_open=None, **params):
        url = self.api_akenoai("api/v2/google/image-to-text")
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field(
                'file',
                open(files_open, 'rb'),
                filename=os.path.basename(files_open),
                content_type='application/octet-stream'
            )
            async with session.post(url, data=form_data, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Error occurred: {response.status}")
                return await response.json()

    async def google_audio_to_text(self, files_open=None, **params):
        url = self.api_akenoai("api/v2/google/audio-to-text")
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            form_data.add_field(
                'file',
                open(files_open, 'rb'),
                filename=os.path.basename(files_open),
                content_type='application/octet-stream'
            )
            async with session.post(url, data=form_data, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Error occurred: {response.status}")
                return await response.json()

    async def blackbox(self, **payload):
        url = self.api_akenoai("ryuzaki/blackbox")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                return await response.json()

    async def hentai(self):
        url = self.api_akenoai("akeno/hentai")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                return await response.json()

    async def fbdown(self, link=None):
        url = self.api_akenoai("akeno/fbdown-v2")
        params = {"link": link}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                return await response.json()

    async def pinterest(self, **params):
        url = self.api_akenoai("akeno/pinterest-v2")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                return await response.json()

    async def igdl(self, version=False, **params):
        url_ig2 = self.api_akenoai("akeno/fastdl-ig-v2")
        url = self.api_akenoai("akeno/fastdl-ig")
        async with aiohttp.ClientSession() as session:
            if version:
                async with session.get(url_ig2, params=params) as response:
                    return await response.json()
            else:
                async with session.get(url, params=params) as response:
                    return await response.json()

    async def fdownloader(self, **params):
        url = self.api_akenoai("akeno/fdownloader")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                return await response.json()

    async def capcut(self, link=None):
        self.api_akenoai("akeno/capcut-v1")
        params = {"link": link}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                return await response.json()

    async def add_ipblock(self, ip=None):
        params = {"ip": ip}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_endpoint}/add_to_blacklist_ip/", params=params, headers=self.headers_blacklist) as response:
                return await response.json()

    async def unblock_ip(self, ip=None):
        params = {"ip": ip}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_endpoint}/remove_from_blacklist_ip", params=params, headers=self.headers_blacklist) as response:
                return await response.json()

    async def allowed_ip(self, ip=None):
        payload = {"ip": ip}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_endpoint}/update_allow_ip", json=payload, headers=self.headers_blacklist) as response:
                return await response.json()

    async def unallowed_ip(self, ip=None):
        params = {"ip": ip}
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.api_endpoint}/remove_allow_ip/", params=params, headers=self.headers_blacklist) as response:
                return await response.json()

    async def get_json(self, response=None):
        return DictToObj(response)
