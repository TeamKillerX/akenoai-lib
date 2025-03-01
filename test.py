import asyncio

from akenoai import AkenoXToJs

js = AkenoXToJs().connect()

async def main():
    response = await js.chat.create(
        "openai/gpt-old",
        api_key="demo",
        query="test"
    )
    print(response)


asyncio.run(main())
