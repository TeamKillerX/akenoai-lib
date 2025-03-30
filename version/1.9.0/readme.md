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
