import asyncio

from akenoai import AkenoXJs

js = AkenoXJs(is_akenox_fast=True).connect()

async def test_main():
    response = js.fast.create(
        model="lu-sunda",
        query="hello",
        is_obj=True
    )
    print(response)


asyncio.run(test_main())
