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

import base64
import json as rjson
import logging
import os
import re
from base64 import b64decode as m
from dataclasses import dataclass, field
from typing import *

import aiofiles
import aiohttp  # type: ignore
import requests  # type: ignore
from box import Box  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from fastapi.openapi.utils import get_openapi  # type: ignore
from pydantic import BaseModel  # type: ignore

import akenoai.logger as fast
from akenoai.base import *
from akenoai.types import *

LOGS = logging.getLogger(__name__)

class FormDataBuilder:
    def __init__(self):
        self.file_data = aiohttp.FormData()

    def append(self, name: str, value: bytes, filename: str = None, content_type: str = None):
        self.file_data.add_field(name, value, filename=filename, content_type=content_type)

    async def aiofiles_catbox(self, path: str) -> aiohttp.FormData:
        self.append("reqtype", b"fileupload")
        async with aiofiles.open(path, mode="rb") as file:
            file_data = await file.read()
            self.append(
                "fileToUpload",
                file_data,
                filename=path.split("/")[-1],
                content_type="application/octet-stream"
            )
        return self.file_data

def configure_openapi(app, _sw: EditCustomOpenAPI, custom_openapi=get_openapi):
    if not app:
        raise ValueError("Required app")
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = custom_openapi(
        title=_sw.title,
        version=_sw.version,
        summary=_sw.summary,
        description=_sw.description,
    )
    openapi_schema["info"]["x-logo"] = {"url": _sw.logo_url}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@dataclass
class GenImageEndpoint:
    parent: BaseDev
    endpoint: str
    is_post: Optional[bool] = field(default=False)
    super_fast: Optional[bool] = field(default=False)

    @fast.log_performance
    async def create(self, ctx: str = None, **kwargs):
        if not ctx:
            raise ValueError("ctx name is required.")
        request_params = MakeRequest(
            method="get",
            endpoint=f"{self.endpoint}/{ctx}",
            options=RequestOptions(
                image_read=kwargs.pop("image_read", False),
                remove_author=kwargs.pop("remove_author", False),
                serialize_response=kwargs.pop("serialize_response", False),
                json_response=JSONResponse(
                    use_json=kwargs.pop("body_data", None),
                    use_params=kwargs.pop("params_data", None),
                    indent=kwargs.pop("json_indent", 2)
                ),
                headers=HeaderOptions(custom_headers=kwargs.pop("headers_extra", None)),
            )
        )
        return await self.parent._make_request(
            request_params,
            **kwargs
        ) if self.super_fast else None

@dataclass
class GenericEndpoint:
    parent: BaseDev
    endpoint: str
    is_post: Optional[bool] = field(default=False)
    super_fast: Optional[bool] = field(default=False)

    @fast.log_performance
    async def create(self, ctx: str = None, is_obj: bool = False, **kwargs):
        if not ctx:
            raise ValueError("ctx name is required.")
        _check_method = "post" if self.is_post else "get"
        request_params = MakeRequest(
            method=_check_method,
            endpoint=f"{self.endpoint}/{ctx}",
            options=RequestOptions(
                image_read=kwargs.pop("image_read", False),
                remove_author=kwargs.pop("remove_author", False),
                serialize_response=kwargs.pop("serialize_response", False),
                json_response=JSONResponse(
                    use_json=kwargs.pop("body_data", None),
                    use_params=kwargs.pop("params_data", None),
                    indent=kwargs.pop("json_indent", 2)
                ),
                headers=HeaderOptions(custom_headers=kwargs.pop("headers_extra", None)),
            )
        )
        response = await self.parent._make_request(
            request_params,
            **kwargs
        ) or {}
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
            .translate (any): for translate google API
            .story_in_tg (any): for story DL telegram
            .super_fast (bool): for fast response
        """
        self.is_bypass_control = is_bypass_control
        self.update_public_url()
        super().__init__(self.public_url)
        self.chat = GenericEndpoint(self, "fast", is_post=True, super_fast=True) if self.is_bypass_control else GenericEndpoint(self, "ai", super_fast=True)
        self.downloader = GenericEndpoint(self, "fast", super_fast=True) if self.is_bypass_control else GenericEndpoint(self, "dl", super_fast=True)
        self.image = GenImageEndpoint(self, "flux", super_fast=True)
        self.translate = self.Translate(self)
        self.story_in_tg = self.LinkExtraWithStory(self)

    def update_public_url(self):
        self.public_url = "https://faster.maiysacollection.com/v2" if self.is_bypass_control else "https://randydev-ryu-js.hf.space/api/v1"

    def set_bypass_control(self, value: bool):
        self.is_bypass_control = value
        self.update_public_url()

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

@dataclass
class AkenoXJs:
    dev: DifferentAPIDefault
    """
    Parameters:
        is_err (bool): for ErAPI
        is_itzpire (bool): for itzpire API
        is_akenox_fast (bool): for AkenoX hono API Faster
        default (bool): If False, default using AkenoX API or Masya API (is_masya=True)
    """
    def __post_init__(self):
        self.endpoints = {
            "itzpire": ItzPire(),
            "err": ErAPI(),
            "akenox_fast": AkenoXDevFaster(),
            "default": RandyDev(self.dev.is_masya)
        }
        self.flags = {
            "itzpire": self.dev.is_itzpire,
            "err": self.dev.is_err,
            "akenox_fast": self.dev.is_akenox_fast
        }

    def connect(self):
        if self.flags["itzpire"]:
            return self.endpoints["itzpire"]
        if self.flags["err"]:
            return self.endpoints["err"]
        if self.flags["akenox_fast"]:
            return self.endpoints["akenox_fast"]
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

async def fetch(fetch_params: MakeFetch, *args, **kwargs):
    return await simple_fetch(fetch_params, *args, **kwargs)

async def simple_fetch(fetch: MakeFetch, *args, **kwargs):
    if aiohttp:
        async with aiohttp.ClientSession(headers=fetch.headers) as session:
            method = session.head if fetch.head else (session.post if fetch.post else session.get)
            async with method(fetch.url, *args, **kwargs) as response:
                return await _process_response(
                    response,
                    evaluate=fetch.evaluate,
                    return_json=fetch.return_json,
                    return_json_and_obj=fetch.return_json_and_obj,
                    return_content=fetch.return_content,
                    head=fetch.head,
                    object_flag=fetch.object_flag,
                )
    else:
        raise DependencyMissingError("Install 'aiohttp' required") # type: ignore
