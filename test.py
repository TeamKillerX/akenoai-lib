from akenoai import AkenoXToJs
import asyncio

js = AkenoXToJs().connect()

async def main():
    response = await js.chat.create(
        "openai/gpt-old", 
        api_key="demo",
        query="test"
    )
    print(response)


asyncio.run(main())