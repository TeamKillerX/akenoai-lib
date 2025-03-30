import os
from enum import Enum
import aiohttp  # type: ignore
from pydantic import BaseModel, ConfigDict  # type: ignore
from dataclasses import field

class JSONResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    use_json: Optional[dict] = None
    use_params: Optional[dict] = None
    use_form_data: Optional[aiohttp.FormData] = None

class DifferentAPIDefault(BaseModel):
    is_err: Optional[bool] = field(default=False)
    is_itzpire: Optional[bool] = field(default=False)
    is_akenox_fast: Optional[bool] = field(default=False)
    is_masya: bool = False

class MakeRequest(BaseModel):
    method: str
    endpoint: str
    image_read: Optional[bool] = False
    remove_author: Optional[bool] = False
    return_text_response: Optional[bool] = False
    serialize_response: Optional[bool] = False
    json_indent: Optional[int] = 4

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

class ScraperProxy(BaseModel):
    url: str
    api_url: str = "https://api.scraperapi.com"
    proxy_url: Optional[str] = "http://scraperapi:{api_key}@proxy-server.scraperapi.com:{port}"
    api_key: Optional[str] = os.environ.get('SCRAPER_KEY')
    port: Optional[int] = 8001
    use_proxy_mode: Optional[bool] = False
    use_post: Optional[bool] = False
    use_post_proxy: Optional[bool] = False
    verify_ssl: Optional[Union[bool, str]] = True
    extract_data: Optional[bool] = False
    extract_all_hrefs: Optional[bool] = False
    extract_all_hrefs_only_proxy: Optional[bool] = False
    response_mode: ResponseMode = ResponseMode.DEFAULT
