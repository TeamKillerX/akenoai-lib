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

import aiohttp
import httpx
import requests
import uvloop
import wget
from box import Box

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
            "@" + desired_username if desired_username else "-100" + target_link[1].split("/")[0]
            if len(target_link) > 1 else None
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

    def _prepare_request(self, endpoint: str, api_key: str = None, headers_extra: dict = None):
        """Prepare request URL and headers."""
        if not api_key:
            api_key = os.environ.get("AKENOX_KEY")
        if not api_key:
            raise ValueError("Required variables AKENOX_KEY or api_key")
        url = f"{self.public_url}/{endpoint}"
        headers = {
            "x-api-key": api_key,
            "Authorization": f"Bearer {api_key}"
        }
        if headers_extra:
            headers.update(headers_extra)
        return url, headers

    async def _make_request(self, method: str, endpoint: str, image_read=False, **params):
        """Handles async API requests.

        Parameters:
            method (str): HTTP method to use.
            endpoint (str): API endpoint.
            image_read (bool): If True, expects the response to be an image.
                The method will verify that the response's Content-Type begins with 'image/'
                and then return the raw bytes from the response.
            **params: Additional parameters to be sent with the request.
        """
        url, headers = self._prepare_request(endpoint, params.pop("api_key", None))
        try:
            async with aiohttp.ClientSession() as session:
                request = getattr(session, method)
                async with request(url, headers=headers, params=params) as response:
                    if image_read:
                        return await response.read()
                    return await response.json()
        except (aiohttp.client_exceptions.ContentTypeError, json.decoder.JSONDecodeError):
            raise Exception("GET OR POST INVALID: check problem, invalid JSON")
        except (aiohttp.ClientConnectorError, aiohttp.client_exceptions.ClientConnectorSSLError):
            raise Exception("Cannot connect to host")
        except Exception:
            return None

class RandyDev(BaseDev):
    def __init__(self, public_url: str = "https://randydev-ryu-js.hf.space/api/v1"):
        super().__init__(public_url)
        self.chat = self.Chat(self)
        self.downloader = self.Downloader(self)
        self.image = self.Image(self)
        self.user = self.User(self)
        self.translate = self.Translate(self)
        self.story_in_tg = self.LinkExtraWithStory(self)

    class Chat:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        @fast.log_performance
        async def create(self, model: str = None, is_obj=False, **kwargs):
            """Handle AI Chat API requests."""
            if not model:
                raise ValueError("Model name is required for AI requests.")
            response = await self.parent._make_request("get", f"ai/{model}", **kwargs) or {}
            return self.parent.obj(response) if is_obj else response

    class User:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        @fast.log_performance
        async def create(self, model: str = None, is_obj=False, **kwargs):
            """Handle User API requests."""
            if not model:
                raise ValueError("User name is required for Telegram")
            response = await self.parent._make_request("get", f"user/{model}", **kwargs) or {}
            return self.parent.obj(response) if is_obj else response

    class Image:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        @fast.log_performance
        async def create(self, model: str = None, **kwargs):
            """Handle Image API requests."""
            if not model:
                raise ValueError("Image model is required for generating image AI")
            return await self.parent._make_request("get", f"flux/{model}", **kwargs)

    class Downloader:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        @fast.log_performance
        async def create(self, model: str = None, is_obj=False, **kwargs):
            """Handle downloader API requests."""
            if not model:
                raise ValueError("Model name is required for downloader requests.")
            response = await self.parent._make_request("get", f"dl/{model}", **kwargs) or {}
            return self.parent.obj(response) if is_obj else response

    class Translate:
        def __init__(self, parent: BaseDev):
            self.parent = parent

        async def lang(self, text: str = None, is_obj=False, **kwargs):
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
    def __init__(self, public_url: str = "https://randydev-ryu-js.hf.space/api/v1"):
        self.randydev = RandyDev(public_url)

AkenoXToJs = AkenoXJs
