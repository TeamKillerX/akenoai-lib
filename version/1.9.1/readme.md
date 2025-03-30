# Version 1.9.1
```py
from akenoai import BaseDev
from akenoai.types import MakeRequest, RequestOptions, JSONResponse

response = await BaseDev("https://faster.maiysacollection.com/v2")._make_request(
    MakeRequest(
        method="get",
        endpoint="fast/list-endpoint",
        options=RequestOptions(
            serialize_response=True
        ),
        json_indent=4
    ),
    JSONResponse()
)
print(response)
```
**Note:** Since `_make_request()` is missing a required positional argument `_json`, you need to use `JSONResponse()` if necessary. If you import `from akenoai import *`, you might encounter errors. Instead, use `from akenoai.types import *` to avoid issues.
