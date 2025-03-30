# Version 1.9.0
```py
from akenoai import *

results = await BaseDev("https://faster.maiysacollection.com/v2/fast")._make_request(
    MakeRequest(
        method="post",
        endpoint="chat/completion"
    ),
    JSONResponse(
        use_json=request_params(
            prompt="what is python?",
            model="qwen-plus",
        )
    ),
    api_key="<your-api-key-optional>", # Optional: remove if not needed
    headers_extra={"User-Agent": "Mozilla/5.0"} # Optional: remove if not needed
)
response_get = BaseDev(None).obj(results) or {}
print(response_get.response)
```
- ScraperProxy
```py
from akenoai import ScraperProxy, BaseDev

scp = ScraperProxy(
    url="https://ttsave.app/download",
    api_url="https://api.scraperapi.com",
    api_key="your-api-key",
    extract_data=False,
    use_post=True,
    extract_all_hrefs=True,
    response_mode="default"
)

response = BaseDev(None)._make_request_with_scraper(
    scp,
    query="https://www.tiktok.com/@penjasnipam/video/7473392499655068946?is_from_webapp=1&sender_device=pc&web_id=7476152122733725202",
    language_id="2"
)

print(response)```
