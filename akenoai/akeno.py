#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Credits @xpushz on telegram
# Copyright 2020-2025 (c) Randy W @xtdevs, @xtsea on telegram
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import base64
import json
import logging
import os
import re
import subprocess
from base64 import b64decode as m
from datetime import datetime

import aiohttp  # type: ignore
import requests  # type: ignore
from box import Box  # type: ignore
from bs4 import BeautifulSoup

import akenoai.logger as fast

LOGS = logging.getLogger(__name__)

class BaseDev:
    def __init__(self, public_url: str):
        self.public_url = public_url
        self.obj = Box

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
        api_key: str = None,
        headers_extra: dict = None,
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
            "x-api-key": api_key,
            "Authorization": f"Bearer {api_key}"
        }
        if headers_extra:
            headers.update(headers_extra)
        return url, headers

    def _make_request_with_scraper(
        self,
        api_key: str = None,
        url: str = None,
        is_text: bool = False,
        is_data: bool = False,
        **data
    ):
        api_url = "https://api.scraperapi.com"
        params = {"api_key": api_key, "url": url}
        request_kwargs = {"data": data} if is_data else {"json": data}
        response = requests.post(api_url, params=params, **request_kwargs)
        return response.text if is_text and not is_data else response

    async def _make_upload_file_this(self, upload_file=None, is_upload=False):
        form_data = aiohttp.FormData()
        form_data.add_field(
            'file',
            open(upload_file, 'rb'),
            filename=os.path.basename(upload_file),
            content_type='application/octet-stream'
        )
        return form_data if is_upload else None

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        upload_file=None,
        image_read=False,
        remove_author=False,
        add_field=False,
        is_upload=False,
        **params
    ):
        """Handles async API requests.

        Parameters:
            method (str): HTTP method to use.
            endpoint (str): API endpoint.
            image_read (bool): If True, expects the response to be an image.
                The method will verify that the response's Content-Type begins with 'image/'
                and then return the raw bytes from the response.
            **params: Additional parameters to be sent with the request.
        """
        url, headers = self._prepare_request(
            endpoint,
            params.pop("api_key", None),
            params.pop("headers_extra", None),
        )
        json = params.pop("body_data", None)
        try:
            async with aiohttp.ClientSession() as session:
                request = getattr(session, method)
                form_data = None
                if add_field:
                    form_data = await self._make_upload_file_this(upload_file=upload_file, is_upload=is_upload)
                async with request(url, headers=headers, params=params, json=json, data=form_data) as response:
                    if image_read:
                        return await response.read()
                    if remove_author:
                        response = await response.json()
                        del response["author"]
                        return response
                    return await response.json()
        except (aiohttp.client_exceptions.ContentTypeError, json.decoder.JSONDecodeError) as e:
            raise Exception("GET OR POST INVALID: check problem, invalid JSON") from e
        except (aiohttp.ClientConnectorError, aiohttp.client_exceptions.ClientConnectorSSLError) as e:
            raise Exception("Cannot connect to host") from e
        except Exception as e:
            LOGS.exception("An error occurred")
            return None

class GenImageEndpoint:
    def __init__(
        self,
        parent: BaseDev,
        endpoint: str,
        super_fast: bool = False
    ):
        self.parent = parent
        self.endpoint = endpoint
        self.super_fast = super_fast

    @fast.log_performance
    async def create(self, ctx: str = None, is_obj: bool = False, **kwargs):
        if not ctx:
            raise ValueError("ctx name is required.")
        _response_image = await self.parent._make_request("get", f"{self.endpoint}/{ctx}", **kwargs)
        return _response_image if self.super_fast else None

class GenericEndpoint:
    def __init__(
        self,
        parent: BaseDev,
        endpoint: str,
        is_post: bool = False,
        super_fast: bool = False
    ):
        self.parent = parent
        self.is_post = is_post
        self.endpoint = endpoint
        self.super_fast = super_fast

    @fast.log_performance
    async def create(self, ctx: str = None, is_obj: bool = False, **kwargs):
        if not ctx:
            raise ValueError("ctx name is required.")
        response = await self.parent._make_request("post", f"{self.endpoint}/{ctx}", **kwargs) or {} if self.is_post else await self.parent._make_request("get", f"{self.endpoint}/{ctx}", **kwargs) or {}
        _response_parent = self.parent.obj(response) if is_obj else response
        return _response_parent if self.super_fast else None

class BaseDevWithEndpoints(BaseDev):
    def __init__(self, public_url: str, endpoints: dict, **kwargs):
        super().__init__(public_url)
        for attr, endpoint in endpoints.items():
            setattr(self, attr, GenericEndpoint(self, endpoint, super_fast=True))

class AkenoXDevFaster(BaseDevWithEndpoints):
    def __init__(self, public_url: str = "https://faster.maiysacollection.com/v2"):
        endpoints = {
            "fast": "fast"
        }
        super().__init__(public_url, endpoints)

class ItzPire(BaseDevWithEndpoints):
    def __init__(self, public_url: str = "https://itzpire.com"):
        endpoints = {
            "chat": "ai",
            "anime": "anime",
            "check": "check",
            "downloader": "download",
            "games": "games",
            "information": "information",
            "maker": "maker",
            "movie": "movie",
            "random": "random",
            "search": "search",
            "stalk": "stalk",
            "tools": "tools",
        }
        super().__init__(public_url, endpoints)

class ErAPI(BaseDevWithEndpoints):
    def __init__(self, public_url: str = "https://er-api.biz.id"):
        """
        The ErAPI requires the following parameters:

          • "u=": This parameter is required
          • "t=": This parameter is required
          • "c=": This parameter is required

        Example usage:
          /get/run?c={code}&bhs={languages}
        """
        endpoints = {
            "chat": "luminai",
            "get": "get",
            "downloader": "dl",
        }
        super().__init__(public_url, endpoints)

class RandyDev(BaseDev):
    def __init__(self, is_bypass_control: bool = False):
        """
        Parameters:
            .chat (any): for Chat AI
            .downloader (any): for all downloader
            .image (any): for image generate AI
            .user (any): for user telegram API
            .translate (any): for translate google API
            .story_in_tg (any): for story DL telegram
            .proxy (any): for scaper proxy API
            .super_fast (bool): for fast response
        """
        self.is_bypass_control = is_bypass_control
        self.update_public_url()
        super().__init__(self.public_url)
        self.chat = GenericEndpoint(self, "fast", is_post=True, super_fast=True) if self.is_bypass_control else GenericEndpoint(self, "ai", super_fast=True)
        self.downloader = GenericEndpoint(self, "fast", super_fast=True) if self.is_bypass_control else GenericEndpoint(self, "dl", super_fast=True)
        self.image = GenImageEndpoint(self, "flux", super_fast=True)
        self.user = self.User(self)
        self.translate = self.Translate(self)
        self.story_in_tg = self.LinkExtraWithStory(self)
        self.proxy = self.Proxy(self)

    def update_public_url(self):
        self.public_url = "https://faster.maiysacollection.com/v2" if self.is_bypass_control else "https://randydev-ryu-js.hf.space/api/v1"

    def set_bypass_control(self, value: bool):
        self.is_bypass_control = value
        self.update_public_url()

    class User:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        @fast.log_performance
        async def create(self, action: str = None, is_obj=False, **kwargs):
            """Handle User API requests."""
            ops = {
                "status_ban": "status/ban",
                "check_admin": "author/admin",
                "raw_chat": "raw/getchat",
                "date": "creation-date",
                "ban": "ban-user",
                "check_ban": "check-ban",
            }
            if action not in ops:
                raise ValueError(f"Invalid User action: {action}")
            response = await self.parent._make_request("get", f"user/{ops[action]}", **kwargs) or {}
            return self.parent.obj(response) if is_obj else response

        async def api_key_operation(self, action: str, is_obj=False, **kwargs):
            ops = {
                "generate": "generate-key",
                "ban": "api-key-ban"
            }
            if action not in ops:
                raise ValueError(f"Invalid API key action: {action}")
            response = await self.parent._make_request("get", f"key/{ops[action]}", **kwargs) or {}
            return self.parent.obj(response) if is_obj else response

    class Proxy:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        async def scraper(self, **kwargs):
            return self.parent._make_request_with_scraper(**kwargs)

    class Translate:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        async def to(self, text: str = None, is_obj=False, **kwargs):
            """Handle Translate Google API requests."""
            if not text:
                raise ValueError("text name is required for Google Translate.")
            response = await self.parent._translate(text, **kwargs) or {}
            return self.parent.obj(response) if is_obj else response

    class LinkExtraWithStory:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        async def links_extra_with(self, link: str = None):
            """Handle Link Story Random in Telegram."""
            if not link:
                raise ValueError("link name is required for Link Story Random.")
            return self.parent._get_random_from_channel(link)

        async def download_story(self, filename: str = "downloaded_story.mp4", **kwargs):
            """Handle Story Downloader in Telegram."""
            if not filename:
                raise ValueError("filename name is required for Story Downloader.")
            response = await self.parent.user.create("story-dl", is_obj=True, **kwargs)
            if not hasattr(response, "download") or not response.download:
                raise ValueError("Invalid response: No downloadable content found.")
            with open(filename, "wb") as f:
                f.write(base64.b64decode(response.download))
            return filename

class AkenoXJs:
    def __init__(
        self,
        is_err: bool = False,
        is_itzpire: bool = False,
        is_akenox_fast: bool = False,
        is_bypass_control: bool = False
    ):
        """
        Parameters:
            is_err (bool): for ErAPI
            is_itzpire (bool): for itzpire API
            is_akenox_fast (bool): for AkenoX hono API Faster
            default (bool): If False, default using AkenoX API
        """

        self.endpoints = {
            "itzpire": ItzPire(),
            "err": ErAPI(),
            "akenox_fast": AkenoXDevFaster(),
            "default": RandyDev(is_bypass_control)
        }
        self.flags = {
            "itzpire": is_itzpire,
            "err": is_err,
            "akenox_fast": is_akenox_fast
        }

    def connect(self):
        if self.flags["itzpire"]:
            return self.endpoints["itzpire"]
        if self.flags["err"]:
            return self.endpoints["err"]
        if self.flags["akenox_fast"]:
            return self.endpoints["akenox_fast"]
        if self.endpoints["default"]:
            return self.endpoints["default"]

class AkenoXDev:
    BASE_URL = "https://randydev-ryu-js.hf.space/api/v1"
    BASE_DEV_URL = "https://learn.maiysacollection.com/api/v1"

    def __init__(self):
        self.api_key = None
        self.user_id = None
        self.storage = {}
        self.connected = False

    @classmethod
    def fast(cls):
        return cls()

    def _check_connection(self):
        if not self.connected or "results" not in self.storage:
            return False, {"status": "disconnected"}
        return True, self.storage["results"]

    def _perform_request(self, url, params, return_json=True):
        try:
            response = requests.get(url, params=params, headers={"x-api-key": self.storage["results"]["key"]})
            return response.json() if return_json else response.content
        except requests.RequestException as e:
            self.connected = False
            LOGS.error(f"❌ API Request Failed: {e}")
            return {"status": "error", "message": f"API Request Failed: {e}"}

    def connect(self, api_key: str = None, user_id: int = None):
        if not api_key:
            api_key = os.environ.get("AKENOX_KEY")
        if not api_key or not isinstance(user_id, int):
            raise ValueError("Invalid API key or user ID")

        self.api_key = api_key
        self.user_id = user_id

        try:
            response = requests.post(
                f"{self.BASE_URL}/debug/connect",
                params={"user_id": self.user_id, "api_key": self.api_key}
            ).json()

            if response.get("is_connect"):
                self.storage["results"] = response
                self.connected = True
                LOGS.info(f"✅ Connected with API key: {self.api_key} and user ID: {self.user_id}")
                return {"status": "Successfully connected."}
            else:
                self.connected = False
                return {"status": "Connection failed. Check API key or user ID."}
        except requests.RequestException as e:
            self.connected = False
            LOGS.error(f"❌ API Request Failed: {e}")
            return {"status": "error", "message": f"API Request Failed: {e}"}

    def disconnect(self):
        self.storage.pop("results", None)
        self.connected = False
        return {"status": "Successfully disconnected"}

    def status(self):
        ok, status_or_response = self._check_connection()
        if not ok:
            return status_or_response
        status = self.storage["results"]
        return {
            "status": "connected",
            "api_key": status.get("key", "unknown"),
            "user_id": status.get("owner", "unknown"),
            "is_banned": status.get("is_banned", False)
        }

    def instagram(self, link: str = None, version: str = "v3"):
        ok, status_or_response = self._check_connection()
        if not ok:
            return status_or_response
        if not link:
            return {"error": "required link"}
        url = f"{self.BASE_DEV_URL}/dl/ig/custom"
        params = {"link": link, "version": version}
        return self._perform_request(url, params, return_json=True)

    def flux_schnell(self, prompt: str = None, filename: str = "randydev.jpg", image_content: bool = False):
        ok, status_or_response = self._check_connection()
        if not ok:
            return status_or_response
        if not prompt:
            return {"error": "required prompt"}
        url = f"{self.BASE_URL}/flux/black-forest-labs/flux-1-schnell"
        params = {"query": prompt}
        if image_content:
            return self._perform_request(url, params, return_json=False)

        responses_content = self._perform_request(url, params, return_json=False)
        with open(filename, "wb") as f:
            f.write(responses_content)
        LOGS.info(f"Successfully save check: {filename}")
        return filename

    def anime_hentai(self, view_url=False):
        ok, status_or_response = self._check_connection()
        if not ok:
            return status_or_response
        url = f"{self.BASE_URL}/anime/hentai"
        if view_url:
            response = self._perform_request(url, params=None, return_json=True)
            return [urls["video_1"] for urls in response["result"]]
        return self._perform_request(url, params=None, return_json=True)

def request_params(**params):
    return {**params}

def extract_urls(html_content, *, href_url=r"https://scontent", return_unsafe_href=False):
    soup = BeautifulSoup(html_content, "html.parser")
    return [link.get("href") for link in soup.find_all("a", href=re.compile(href_url))] if return_unsafe_href else []

async def fetch_and_extract_urls(url: str, **kwargs):
    try:
      response = await fetch(url, return_json=False)
      html_content = response
      return extract_urls(html_content, **kwargs)
    except Exception as e:
      logging.exception("Exception in fetch_and_extract_urls for url: %s", url)
      return []

def to_buffer(response=None, filename="randydev.jpg", return_image_base64=False):
    if not filename.endswith(".jpg"):
        return None
    with open(filename, "wb") as f:
        if return_image_base64:
            if not response:
                return None
            try:
                decoded_data = base64.b64decode(response)
            except Exception:
                return None
            f.write(decoded_data)
        else:
            f.write(response)
    return filename

async def _process_response(response, evaluate=None, return_json=False, return_json_and_obj=False, return_content=False, head=False, object_flag=False):
    if evaluate:
        return await evaluate(response)
    if return_json:
        return await response.json()
    if return_json_and_obj:
        return Box(await response.json() or {})
    if return_content:
        return await response.read()
    return response if head or object_flag else await response.text()

async def fetch(
    url: str,
    post: bool = False,
    head: bool = False,
    headers: dict = None,
    evaluate=None,
    object_flag: bool = False,
    return_json: bool = False,
    return_content: bool = False,
    return_json_and_obj: bool = False,
    *args,
    **kwargs,
):
    if aiohttp:
        async with aiohttp.ClientSession(headers=headers) as session:
            method = session.head if head else (session.post if post else session.get)
            async with method(url, *args, **kwargs) as response:
                return await _process_response(
                    response,
                    evaluate=evaluate,
                    return_json=return_json,
                    return_json_and_obj=return_json_and_obj,
                    return_content=return_content,
                    head=head,
                    object_flag=object_flag,
                )
    else:
        raise DependencyMissingError("Install 'aiohttp' required")
