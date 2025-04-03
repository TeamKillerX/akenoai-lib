# Version 1.9.5
```py
from akenoai.base import BaseDev
from akenoai.types import MakeRequest, RequestOptions, JSONResponse, HeaderOptions

response = await BaseDev(
    "https://faster.maiysacollection.com/v2"
)._make_request(
    MakeRequest(
        method="get",
        endpoint="fast/list-endpoint",
        options=RequestOptions(
            serialize_response=True,
            json_response=JSONResponse(indent=4),
            headers=HeaderOptions(custom_headers={"Authorization": "Bearer YOUR_TOKEN"})
        )
    )
)
print(response)
```
---
# Object-rotation Access
```py
from akenoai.base import BaseDev
from akenoai.types import MakeRequest, LibraryTool, RequestOptions

response = await BaseDev(
    "https://faster.maiysacollection.com/v2"
)._make_request(
    MakeRequest(
        method="get",
        endpoint="fast/list-endpoint",
        options=RequestOptions(
            tools=LibraryTool(obj_flag=True)
        )
    )
)
print(response.gempa)
```
