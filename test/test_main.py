import asyncio

import uvloop  # type: ignore

from akenoai import AkenoXToJs

js = AkenoXToJs().connect()

async def test_main():
    response = await js.chat.create(
        "mistral/mistral-7b-instruct-v0.1",
        api_key="....",
        query="is the api on the python ram server as slow as regular windows on ubuntu, different from the high VPS?",
        is_obj=True
    )
    print(response.results)


uvloop.run(test_main())
