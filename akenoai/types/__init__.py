import os
from dataclasses import field
from enum import Enum
from typing import *

import aiohttp  # type: ignore
from pydantic import BaseModel, ConfigDict  # type: ignore


class HeaderOptions(BaseModel):
    custom_headers: Optional[dict] = None

class PyrogramConfig(BaseModel):
    name: str
    app_version: Optional[str] = "AkenoAI Latest"
    api_id: Optional[int] = os.environ.get('API_ID')
    api_hash: Optional[str] = os.environ.get('API_HASH')
    bot_token: Optional[str] = os.environ.get('BOT_TOKEN')
    plugins: Optional[str] = None

class JSONResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    use_json: Optional[dict] = None
    use_params: Optional[dict] = None
    indent: Optional[int] = 2
    use_form_data: Optional[aiohttp.FormData] = None

class DifferentAPIDefault(BaseModel):
    is_masya: bool= False
    is_err: Optional[bool] = False
    is_itzpire: Optional[bool] = False
    is_akenox_fast: Optional[bool] = False

class LibraryTool(BaseModel):
    obj_flag: Optional[bool] = False

class RequestOptions(BaseModel):
    image_read: Optional[bool] = False
    remove_author: Optional[bool] = False
    return_text_response: Optional[bool] = False
    serialize_response: Optional[bool] = False
    json_response: JSONResponse = JSONResponse()
    headers: HeaderOptions = HeaderOptions()
    tools: LibraryTool = LibraryTool()

class MakeRequest(BaseModel):
    method: str
    endpoint: str
    options: RequestOptions = RequestOptions()

class MakeFetch(BaseModel):
    url: str
    post: Optional[bool] = False
    head: Optional[bool] = False
    headers: Optional[dict] = None
    evaluate: Optional[str] = None
    object_flag: Optional[bool] = False
    return_json: Optional[bool] = False
    return_content: Optional[bool] = False
    return_json_and_obj: Optional[bool] = False

class ResponseMode(Enum):
    DEFAULT = "default"
    TEXT = "text"
    JSON = "json"

class ProxyLogin(BaseModel):
    proxy_url: Optional[str] = "http://scraperapi:{api_key}@proxy-server.scraperapi.com:{port}"
    api_key: Optional[str] = os.environ.get('SCRAPER_KEY')
    port: Optional[int] = 8001

class ProxyOptions(BaseModel):
    use_proxy_mode: Optional[bool] = False
    use_post: Optional[bool] = False
    use_post_proxy: Optional[bool] = False
    verify_ssl: Optional[Union[bool, str]] = True
    extract_data: Optional[bool] = False
    extract_all_hrefs: Optional[bool] = False
    extract_all_hrefs_only_proxy: Optional[bool] = False

class ScraperProxy(BaseModel):
    url: str
    api_url: str = "https://api.scraperapi.com"
    login: ProxyLogin = ProxyLogin()
    proxy_options: ProxyOptions = ProxyOptions()
    response_mode: ResponseMode = ResponseMode.DEFAULT

class EditCustomOpenAPI(BaseModel):
    logo_url: Optional[str] = None
    title: Optional[str] = "AkenoX Demo API"
    version: Optional[str] = "1.0.0"
    summary: Optional[str] = "Use It Only For Personal Projects"
    description: Optional[str] = "Free API By akenoai-lib"

__all__ = [
    "JSONResponse",
    "DifferentAPIDefault",
    "RequestOptions",
    "MakeRequest",
    "MakeFetch",
    "ResponseMode",
    "ProxyLogin",
    "ProxyOptions",
    "ScraperProxy",
    "HeaderOptions",
    "EditCustomOpenAPI",
    "PyrogramConfig",
]
