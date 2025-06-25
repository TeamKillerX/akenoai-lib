import json as rjson
import logging
import os
import platform
from typing import *

import aiohttp
import requests
from box import Box  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

import akenoai.logger as fast
from akenoai.errors import IncorrectInputError
from akenoai.types import *

LOGS = logging.getLogger(__name__)

class BaseDev:
    def __init__(self, public_url: str):
        self.public_url = public_url
        self.obj = Box

    def _extract_all_hrefs(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        return [a['href'] for a in soup.find_all('a', href=True)]

    def _handle_response(self, response, mode):
        if mode == ResponseMode.TEXT:
            return response.text
        elif mode == ResponseMode.JSON:
            try:
                return response.json()
            except ValueError as e:
                logging.debug("Failed to parse JSON response: %s", e)
                return response.text

    def _handle_text_response(self, response):
        return response.text

    def _handle_json_response(self, response):
        try:
            return response.json()
        except ValueError as e:
            logging.debug("Failed to parse JSON response: %s", e)
            return response.text

    def _handle_proxy(self, x, data):
        proxies = {
            "https": x.login.proxy_url.format(api_key=x.login.api_key, port=x.login.port)
        }
        resp = (requests.post(x.url, proxies=proxies, json=data.pop("json_proxy", None), verify=x.proxy_options.verify_ssl)
                if x.proxy_options.use_post_proxy else
                requests.get(x.url, proxies=proxies, verify=x.proxy_options.verify_ssl))
        return self._extract_all_hrefs(resp.text) if x.proxy_options.extract_all_hrefs_only_proxy else resp

    def _get_random_from_channel(self, link: str = None):
        clean_link = link.split("?")[0]
        target_link = clean_link.split("/c/") if "/c/" in clean_link else clean_link.split("/")
        random_id = int(target_link[-1].split("/")[-1]) if len(target_link) > 1 else None
        desired_username = target_link[3] if len(target_link) > 3 else None
        username = (
            f"@{desired_username}"
            if desired_username
            else (
                "-100" + target_link[1].split("/")[0]
                if len(target_link) > 1
                else None
            )
        )
        return username, random_id

    async def _translate(self, text: str = None, target_lang: str = None):
        API_URL = "https://translate.googleapis.com/translate_a/single"
        HEADERS = {"User-Agent": "Mozilla/5.0"}
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, headers=HEADERS, params=params) as response:
                if response.status != 200:
                    return None
                translation = await response.json()
                return "".join([item[0] for item in translation[0]])

    def _prepare_request(
        self,
        endpoint: str,
        header: HeaderOptions,
        api_key: str = None
    ):
        """Prepare request URL and headers."""
        if not api_key:
            api_key = os.environ.get("AKENOX_KEY")
        if not api_key:
            api_key = os.environ.get("AKENOX_KEY_PREMIUM")
        if not api_key:
            api_key = "demo"
        url =  f"{self.public_url}/{endpoint}"
        headers = {
            "User-Agent": f"Ryzenth/Python-{platform.python_version()}",
            "x-api-key": api_key
        }
        if header.custom_headers:
            headers |= header.custom_headers
        return url, headers

    def _make_request_with_scraper(self, x: ScraperProxy, **data):
        if not x.login.api_key:
            return "Required api key"
        params = {"api_key": x.login.api_key, "url": x.url}
        request_kwargs = {"data": data} if x.proxy_options.extract_data else {"json": data}
        response = (requests.post(x.api_url, params=params, **request_kwargs)
                    if x.proxy_options.use_post else
                    requests.get(x.api_url, params=params))

        if x.response_mode in {ResponseMode.TEXT, ResponseMode.JSON}:
            return self._handle_response(response, x.response_mode)
        if x.proxy_options.extract_all_hrefs:
            return self._extract_all_hrefs(response.text)
        if x.proxy_options.use_proxy_mode:
            return self._handle_proxy(x, data)
        return response

    async def _make_request(
        self,
        u: MakeRequest,
        **params
    ):
        url, headers = self._prepare_request(
            endpoint=u.endpoint,
            header=u.options.headers,
            api_key=params.pop("api_key", None)
        )
        try:
            async with aiohttp.ClientSession() as session:
                request = getattr(session, u.method)
                async with request(
                    url,
                    headers=headers,
                    params=u.options.json_response.use_params,
                    json=u.options.json_response.use_json,
                    data=u.options.json_response.use_form_data
                ) as response:
                    json_data = response
                    if u.options.image_read:
                        return await json_data.read()
                    if u.options.remove_author:
                        vjson = await json_data.json()
                        key_to_remove = params.pop("del_author", None)
                        if key_to_remove is not None and key_to_remove in vjson:
                            del vjson[key_to_remove]
                        if u.options.tools.obj_flag:
                            return self.obj(vjson) or {}
                        return vjson
                    if u.options.serialize_response:
                        if u.options.tools.obj_flag:
                            return rjson.dumps(
                                self.obj(await json_data.json()) or {},
                                indent=u.options.json_response.indent
                            )
                        return rjson.dumps(await json_data.json(), indent=u.options.json_response.indent)
                    if u.options.return_text_response:
                        return await json_data.text() if u.options.return_text_response else None
                    if u.options.tools.obj_flag:
                        return self.obj(await json_data.json()) or {} if u.options.tools.obj_flag else None
                    return await json_data.json()
        except (aiohttp.client_exceptions.ContentTypeError, rjson.decoder.JSONDecodeError) as e:
            raise IncorrectInputError("GET OR POST INVALID: check problem, invalid JSON") from e
        except (aiohttp.ClientConnectorError, aiohttp.client_exceptions.ClientConnectorSSLError) as e:
            raise IncorrectInputError("Cannot connect to host") from e
        except Exception as e:
            LOGS.exception("An error occurred")
            return None

__all__ = ["BaseDev"]
