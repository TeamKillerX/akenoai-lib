# akenoai-lib
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/TeamKillerX/akenoai-lib)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-green)](https://github.com/TeamKillerX/akenoai-lib/graphs/commit-activity)
[![GitHub Forks](https://img.shields.io/github/forks/TeamKillerX/akenoai-lib?&logo=github)](https://github.com/TeamKillerX/akenoai-lib)
[![License](https://img.shields.io/badge/License-GPL-pink)](https://github.com/TeamKillerX/akenoai-lib/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![akenoai - Version](https://img.shields.io/pypi/v/akenoai?style=round)](https://pypi.org/project/akenoai)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/akenoai?label=DOWNLOADS&style=round)](https://pypi.org/project/akenoai)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/akenoai/1.7.2?artifact_id=tar-gz)](https://socket.dev/pypi/package/akenoai/overview/1.7.2/tar-gz)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/TeamKillerX/akenoai-lib/main.svg)](https://results.pre-commit.ci/latest/github/TeamKillerX/akenoai-lib/main)

### 🚨 Important Notice:
> [!IMPORTANT]
> Read Before Using!
>
> 📜 Read the Code of Conduct:
> 🔗 [`CODE_OF_CONDUCT`](https://github.com/TeamKillerX/akenoai-lib/blob/main/CODE_OF_CONDUCT.md)
```
- ⚠️ Public copy-pasting without permission violates the rules!
- 🚨 This may result in a GitHub copyright report.
- ⚠️ Your developer account could be blacklisted.
- ❌ You may lose access to your GitHub username permanently.

- 📢 Respect open-source rules & contribute responsibly! 🚀
```

### installation
🔹 <b>Recommended Installation:</b>

✅ Install via [`PYPI`](https://pypi.org/project/akenoai) for the latest updates. e.g.: `pip3 install akenoai[fast]`

✅ Install via github
- Create a requirements.txt file in the project root containing the following dependency to ensure you can install the GitHub version:
- `git+https://github.com/TeamKillerX/akenoai-lib.git#egg=akenoai[fast]`

### How to learn python
- Collaborative learning
- Usage Examples:
```py
class ExampleYourName(BaseDevWithEndpoints):
    def __init__(self, public_url: str = "https://your-endpoint.com"):
        endpoints = {
            "chat": "ai",
        }
        super().__init__(public_url, endpoints)

```
- Please fork the repository and submit a pull request
- Your Own API
- `https://your-api-endpoint/api/v1`
- An API key is required here.
```
dl/{model}
user/{model}
ai/{model}
```
You can use `AkenoXJs()` passing
```py
js = AkenoXJs(is_your_name=True).connect()
js.chat.create(...)
```
AkenoXJs automatically configures the connection, so there's no need to manually initialize it using OldAkenoXToJs and its randydev method.
```py
js = OldAkenoXToJs(public_url="https://your-api-endpoint/api/v1")
js.randydev("api/endpoint", api_key="", custom_dev_fast=True)
```
### FastAPI Demo
- Use `main.py`
- Try running `python3 main.py`
```py
from akenoai.runner import run_fast

# run_fast initializes a FastAPI server with example routes and configurations.

run_fast()
```
### ✨ New AI Models
1. `akenox/moderator`
2. `akenox/mia-khalifah`
3. `akenox/nocodefou`
4. `akenox/al-sholawat`
5. `akenox/lirik-end`
6. `akenox/quotes-sad`
7. `akenox/quotes-lucu`
8. `akenox/lu-sunda`
9. `akenox/lu-melayu`
10. `akenox/curl-command-code`
11. `akenox/python-to-js-api`
12. `akenox/js-to-python-api`
- Why is your API key expired?

Your API key may have expired due to reaching its validity period. But don't worry, you can get a new one!

💰 <b>Pricing:</b>
- API Key V2: <b>25K/month</b>
- Promo: 85K ( ~125K~ ) for 1 year (AI access included)
- API Key V1: <b>Free & unlimited (for downloader only)</b>

💭 Can a new account get a free API Key V2?

Yes! If your previous API key expired from [`@aknuserbot`](https://t.me/aknuserbot) on telegram, you can create a new account and get <b>API Key V2 free for 1 month.</b> 🚀

📩 Need help? Contact [`@xpushz`](https://t.me/xpushz) no problem! 🚀

### Code examples
-> [!TIP]
-> Tip Usage Example:

- Use Access API key V2 Premium
```py
from akenoai import AkenoXJs

js = AkenoXJs().connect()

response = await js.chat.create(
    "qwen/qwen1.5-1.8b-chat",
    api_key="<your-api-key-premium>",
    is_obj=True,
    query="Hello, how are you?"
)

print(response)
```
- 📥 Example Downloader:
```py
from akenoai import AkenoXJs

js = AkenoXJs().connect()

download_response = await js.downloader.create(
    "instagram-v4",
    api_key="<your-api-key-free>",
    is_obj=False,
    url="https://www.instagram.com/reel/DA0p2NoyN_O/?igsh=MWJvejMxZmZ5ZHd3YQ=="
)

print(download_response)
```
### 🌐 Streamlit + AkenoX API
- installation: `pip3 install akenoai[streamlit]`
- You can use `streamlit run app.py`
- `akenoai[fast]` → <b> no import Pyrogram error:</b> *There is no current event loop* (<b>Stuck in Streamlit</b>)

- Full Example usage:

  Note: The import path changed from `akenoai import AkenoXToJs` to `akenoai.streamlit import StreamlitToJs` to clearly separate the streamlit integration functionality from the core API. The previous import path is now deprecated.
```py
import requests
import json
import time
from akenoai.streamlit import StreamlitToJs as js

class GithubUsername:
    def __init__(self, username):
        self.username = username

    def get_github_data(self):
        req = requests.get(f"https://api.github.com/users/{self.username}").json()
        try:
            return req
        except Exception as e:
            base_msg = f"**Error!** \n\n**Traceback:** \n `{e}` \n\n`Make sure that you've sent the command with the correct username!`"
            return base_msg

js_st = js.stl()
js_st.title("Welcome to akenoai-lib APP")
js_st.write("Developed by RandyDev")
js_st.write("GitHub User Information")

with js_st.form("github"):
    username = js_st.text_input("Enter GitHub username:")
    submit_checkbox = js_st.checkbox("Allow users", value=False)
    submitted = js_st.form_submit_button("Submit")
    if submitted and submit_checkbox:
        js_st.spinner("Fetching GitHub data...")
        github_data = GithubUsername(username).get_github_data()
        if isinstance(github_data, dict):
            js_st.json(github_data)
        else:
            js_st.error(github_data)

js_st.title("Examples JSON by AkenoX API")

with js_st.form("json"):
    submitted = js_st.form_submit_button("Submit")
    if submitted:
        js_st.spinner("Loading......")
        try:
            js_st.json(
                js.no_async_randydev("json/all", is_obj=False)
            )
        except Exception as e:
            js_st.error(str(e))

js_st.title("ChatGPT AI")

with js_st.form("openai"):
    text = js_st.text_area('Enter text:', 'How to JavaScript code?')
    submitted = js_st.form_submit_button('Submit')
    placeholder = js_st.empty()
    free_api_key_on = js_st.toggle("Free API Key")
    if submitted:
        try:
            if free_api_key_on:
                with placeholder, js_st.spinner("Processing......"):
                    time.sleep(5)
                js_st.write(
                    js.no_async_randydev("ai/openai/gpt-old", is_obj=True, query=text).results
                )
                js_st.success("Join Channel Telegram : @RendyProjects")
            else:
                js_st.warning('Use button Free API Key', icon="⚠️")
        except Exception as e:
            js_st.error(str(e))

js.waifu_random()
js.hide_streamlit_watermark(unsafe_allow_html=True)
```
> [!WARNING]
>
>⚠️ Breaking Change ⚠️

> Note: The import path has changed!
>
> To better separate Streamlit integration from the core API, the import path has been updated:

> ❌ <b>Deprecated:</b>
> `from akenoai import AkenoXJs`
>
> ✅ Use this <b>instead:</b>
> `from akenoai.streamlit import StreamlitToJs`
>
> Make sure to update your imports to avoid issues. 🚀

- [X] If using API `[fast]` for <b>full-stack</b>, move to `akenoai.clients`:
```py
from akenoai.clients import create_pyrogram # Use [fast]
```

### 🛠️ Custom OpenAI
```py
from akenoai import OldAkenoXToJs

js = OldAkenoXToJs()

fast_app = js.get_app()

js.custom_openapi(
    app=fast_app,
    logo_url="https://github-production-user-asset-6210df.s3.amazonaws.com/90479255/289277800-f26513f7-cdf4-44ee-9a08-f6b27e6b99f7.jpg",
    title="AkenoX Beta AI API",
    version="1.0.0",
    summary="Use It Only For Personal Projects",
    description="Free API By akenoai-lib",
    routes=fast_app.routes,
)
```
### 🥷 Full-Stack Examples
- [X] Powerful & Super Fast Performance
- [X] Recommended RAM: 8GB / 16GB
- [X] Supports `bot_token` & `session_string`
- [X] Custom Web Frontend with HTML & CSS
```py
import logging
from akenoai import OldAkenoXToJs
from akenoai.runner import run_fast
from akenoai.clients import create_pyrogram

js = OldAkenoXToJs()

logger = logging.getLogger(__name__)
LOGS = logging.getLogger("[akenox]")
logger.setLevel(logging.DEBUG)

from akenoai.models import BaseModel

class Items(BaseModel):
    message: str

fast_app = js.get_app()
js.add_cors_middleware()

assistant = create_pyrogram(
    name="fastapi-bot",
    api_id=1234,
    api_hash="asdfghkl",
    bot_token="1235:asdfh"
)

user_client = create_pyrogram(
    name="fastapi-user",
    api_id=1234,
    api_hash="asdfghkl",
    session_string="session"
)

@fast_app.on_event("startup")
async def startup_event():
    bot = await assistant.start()
    user = await user_client.start()
    LOGS.info(f"Started UserBot & Assistant: {user.me.first_name} || {bot.me.first_name}")

@fast_app.get("/api/cohere")
async def cohere(query: str):
    return await js.randydev(
        "ai/cohere/command-plus",
        api_key="<your_api_key>",
        custom_dev_fast=True,
        query=query,
        chatHistory=[],
        system_prompt="You are a helpful AI assistant designed to provide clear and concise responses."
    )

@fast_app.get("/item")
async def example_test(item: Items):
    return {"message": item.message}

@fast_app.get("/test")
async def example_json():
    async with js.fasthttp().ClientSession() as session:
        async with session.get("https://jsonplaceholder.typicode.com/todos/1") as response:
            title = js.dict_to_obj(await response.json()).title
    return {"message": title}

@fast_app.get("/api/tg/send_message")
async def send_message(text: str, chat_id: str):
    response_json = await client.send_message(chat_id, text)
    return {"message_id": response_json.id}

js.custom_openapi(
    app=fast_app,
    logo_url="https://github-production-user-asset-6210df.s3.amazonaws.com/90479255/289277800-f26513f7-cdf4-44ee-9a08-f6b27e6b99f7.jpg",
    title="AkenoX Beta AI API",
    version="1.0.0",
    summary="Use It Only For Personal Project",
    description="Free API By akenoai-lib",
    routes=fast_app.routes,
)

run_fast(build=fast_app)
```

### 🔹 <b>Method Definition:</b>

- [X] Parameters:
- `endpoint:` The API endpoint to call.
- `api_key:` (Optional) API key for authentication.
- `is_obj:` Boolean flag indicating whether the response should be returned as a Python object (True) or in the default format (False).
- `**params:` Allows passing additional parameters as a dictionary, which will be sent as JSON.

### 🔹 <b>User Creation Date:</b>

This feature retrieves the date when the user's account was initially created. It provides a reliable audit trail and allows users or administrators to verify the account's age, which can be important for purposes such as eligibility verification, security audits, or account management.

```py
import os
from akenoai import OldAkenoXToJs

js = OldAkenoXToJs()

response = await js.randydev(
    "user/creation-date",
    custom_dev_fast=True,
    user_id=client.me.id
)
return response
```
### 🔑 API Key
> [!NOTE]
> How to Get an API Key for AkenoX API?
>
> Different V1 Free and V2 Access Premium
>
> You can set up your API key using environment variables:
```env
AKENOX_KEY=akeno_xxxxxx
```
- To get an API key, [`@aknuserbot`](https://t.me/aknuserbot)

- 🚀 Thank you to our 2.7 million users per request!

### ⚠️ Problem Double Fix:
🛠️ **Double Fix for Connection Issues**
- ❌ **Cannot connect to host**
- 🚫 **IP address blocked issue**
- 🌐 **Different DNS settings**

```py
from akenoai import OldAkenoXToJs

js = OldAkenoXToJs()

proxy_url = "http://PROXY.YOUR-SERVER.COM:8080"

return await js.randydev(
    "ai/openai/gpt-old",
    api_key="akeno_xxxxxxx",
    proxy_url=proxy_url,  # Use proxy if needed
    post=False,
    custom_dev_fast=True
)
```
### 📊 Developed by:
- [`AkenoX API`](https://t.me/xpushz) - Full stack Developer Backend
- [`ErrAPI`](https://t.me/Chakszzz) - Backend And Frontend Web
- [`itzpire API`](https://itzpire.com) - Backend And Frontend Web

### ❤️ Special Thanks To
- [`Kurigram`](https://github.com/KurimuzonAkuma/pyrogram)
- [`FastAPI`](https://github.com/fastapi/fastapi)
- Thank you all developers 😊

# Contributing
If you find a bug or have a feature request, please open an issue on our GitHub repository.

We welcome contributions from the community. If you'd like to contribute, please fork the repository and submit a pull request.

# License
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)
TeamKillerX is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

<h4 align="center">Copyright (C) 2019 - 2025 The AkenoAI <a href="https://github.com/TeamKillerX">TeamKillerX</a>
<a href="https://t.me/xtdevs">@xtdevs</a>
</h4>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Project [akenoai-lib](https://github.com/TeamKillerX/) is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
