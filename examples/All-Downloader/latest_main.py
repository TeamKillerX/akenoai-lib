# Use AkenoXJs instead of AkenoXToJs
# Latest Don't worry 

from akenoai import AkenoXJs

js = AkenoXJs().connect()

async def InstagramDL(url):
    return await js.downloader.create(
        "instagram-v4",
        api_key="<your-api-key-free>",
        is_obj=False,
        url=url
    )

async def TeraboxDL(url):
    return await js.downloader.create(
        "terabox-v3",
        api_key="<your-api-key-free>",
        is_obj=False,
        url=url
    )

async def FacebookDL(url):
    return await js.downloader.create(
        "fb",
        api_key="<your-api-key-free>",
        is_obj=False,
        url=url
    )

async def TikTokDL(url):
    return await js.downloader.create(
        "tiktok",
        api_key="<your-api-key-free>",
        is_obj=False,
        url=url
    )
