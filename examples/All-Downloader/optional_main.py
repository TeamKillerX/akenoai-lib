from akenoai import OldAkenoXToJs


async def generic_downloader(url: str, service: str):
    endpoint = f"dl/{service}"
    response = await OldAkenoXToJs.randydev(
        endpoint,
        api_key=api_key,
        custom_dev_fast=True,
        url=url
    )
    return response

# Usage in main:
async def main():
    teradl = await generic_downloader("...", "terabox")
    fbdl = await generic_downloader("...", "fb")
    ttk = await generic_downloader("...", "tiktok")
    print("terabox", teradl)
    print("fbdl", fbdl)
    print("tiktok", ttk)
