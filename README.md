# AkenoAI-Lib
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/TeamKillerX/akenoai-lib)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-green)](https://github.com/TeamKillerX/akenoai-lib/graphs/commit-activity)
[![GitHub Forks](https://img.shields.io/github/forks/TeamKillerX/akenoai-lib?&logo=github)](https://github.com/TeamKillerX/akenoai-lib)
[![License](https://img.shields.io/badge/License-GPL-pink)](https://github.com/TeamKillerX/akenoai-lib/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![akenoai - Version](https://img.shields.io/pypi/v/akenoai?style=round)](https://pypi.org/project/akenoai)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/akenoai?label=DOWNLOADS&style=round)](https://pypi.org/project/akenoai)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/akenoai/1.7.2?artifact_id=tar-gz)](https://socket.dev/pypi/package/akenoai/overview/1.7.2/tar-gz)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/TeamKillerX/akenoai-lib/main.svg)](https://results.pre-commit.ci/latest/github/TeamKillerX/akenoai-lib/main)

**AkenoAI-Lib** is a high-performance library for making raw HTTP requests, powered by `aiohttp`. It provides a simple yet powerful syntax for handling API requests efficiently, ensuring speed and flexibility.

### Features:
- **Asynchronous Requests** – Fully utilizes `aiohttp` for non-blocking HTTP calls.
- **Optimized Performance** – Designed for speed and low-latency API interactions.
- **Flexible Request Handling** – Supports JSON, form-data, and custom headers.
- **Built-in Response Serialization** – Easily parse and structure API responses.
- **Lightweight & Scalable** – Minimal dependencies with a focus on performance.
- **Optional:** `JSONResponse, HeaderOptions`

> [!IMPORTANT]
> **AkenoAI-Lib**: (Closed for updates)
There won’t be new updates, but if the **raw method** is stable, there’s no need to panic about updates causing errors.

## Installation

```bash
pip install akenoai[fast]
```

## Quick Start

```python
from akenoai.base import BaseDev
from akenoai.types import MakeRequest, RequestOptions, JSONResponse

async def fetch_data():
    response = await BaseDev("https://api.example.com")._make_request(
        MakeRequest(
            method="get",
            endpoint="data/list",
            options=RequestOptions(serialize_response=True)
        )
    )
    return response
```

## Usage

### Making a GET Request

```python
response = await BaseDev("https://example.com")._make_request(
    MakeRequest(
        method="get",
        endpoint="api/resource",
        json_response=JSONResponse()
    )
)
print(response)
```

### Sending a POST Request with JSON Data

```python
response = await BaseDev("https://example.com")._make_request(
    MakeRequest(
        method="post",
        endpoint="api/create",
        options=RequestOptions(),
        json_response=JSONResponse(use_json={"key": "value"})
    )
)
print(response)
```

## Notes
- When using `from akenoai import *`, you may run into errors. Instead, explicitly import required modules: `from akenoai.types import *`.
---
### 📊 Developed by:
- [`AkenoX API`](https://t.me/xpushz) - Full stack Developer Backend
- [`ErrAPI`](https://t.me/Chakszzz) - Backend And Frontend Web
- [`itzpire API`](https://itzpire.com) - Backend And Frontend Web

### ❤️ Special Thanks To
- [`Kurigram`](https://github.com/KurimuzonAkuma/pyrogram)
- [`FastAPI`](https://github.com/fastapi/fastapi)
- Thank you all developers 😊
---
## Contributing
Feel free to open issues and contribute to the development of AkenoAI-Lib!

## License
This project is licensed under the MIT License.
