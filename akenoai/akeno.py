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
import os
import subprocess
from base64 import b64decode as m
from datetime import datetime

import aiohttp  # type: ignore
import requests  # type: ignore
from box import Box  # type: ignore

import akenoai.logger as fast


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

    async def _make_request(self, method: str, endpoint: str, image_read=False, remove_author=False, **params):
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
        try:
            async with aiohttp.ClientSession() as session:
                request = getattr(session, method)
                async with request(url, headers=headers, params=params) as response:
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
        except Exception:
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
        super_fast: bool = False
    ):
        self.parent = parent
        self.endpoint = endpoint
        self.super_fast = super_fast

    @fast.log_performance
    async def create(self, ctx: str = None, is_obj: bool = False, **kwargs):
        if not ctx:
            raise ValueError("ctx name is required.")
        response = await self.parent._make_request("get", f"{self.endpoint}/{ctx}", **kwargs) or {}
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
    def __init__(self, public_url: str = "https://randydev-ryu-js.hf.space/api/v1"):
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
        super().__init__(public_url)
        self.chat = GenericEndpoint(self, "ai", super_fast=True)
        self.downloader = GenericEndpoint(self, "dl", super_fast=True)
        self.image = GenImageEndpoint(self, "flux", super_fast=True)
        self.user = self.User(self)
        self.translate = self.Translate(self)
        self.story_in_tg = self.LinkExtraWithStory(self)
        self.proxy = self.Proxy(self)

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
    def __init__(self, is_err: bool = False, is_itzpire: bool = False, is_akenox_fast: bool = False):
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
            "default": RandyDev()
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
        return self.endpoints["default"]
