# Use AkenoXJs instead of AkenoXToJs
# Latest Don't worry

from akenoai import AkenoXJs

js = AkenoXJs().connect()

async def download(service, url, *, api_key="<your-api-key-free>"):
    return await js.downloader.create(
        service,
        api_key=api_key,
        is_obj=False,
        url=url
    )

async def InstagramDL(url):
    return await download("instagram-v4", url)

async def TeraboxDL(url):
    return await download("terabox-v3", url)

async def FacebookDL(url):
    return await download("fb", url)

async def TikTokDL(url):
    return await download("tiktok", url)
