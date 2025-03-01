from functools import wraps

import aiohttp  # type: ignore


class DictToObj:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObj(value))
            elif isinstance(value, list):
                setattr(self, key, [DictToObj(item) if isinstance(item, dict) else item for item in value])
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f"{self.__dict__}"

def my_api_search(search: str, check_type=None, post=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            CHECK_DATA = {
                "json": "json",
                "data": "data",
                "params": "params",
            }
            if check_type not in CHECK_DATA:
                return "Error: wrong type provided"

            try:
                async with aiohttp.ClientSession() as session:
                    request_kwargs = {CHECK_DATA[check_type]: kwargs}
                    if post:
                        async with session.post(f"https://private-akeno.randydev.my.id/{search}", **request_kwargs) as response:
                            data = await response.json()
                    else:
                        async with session.get(f"https://private-akeno.randydev.my.id/{search}", **request_kwargs) as response:
                            data = await response.json()
            except aiohttp.ClientError:
                return f"API Error: Request failed"
            except Exception as e:
                return f"Unexpected Error: ok"
            data_as_obj = DictToObj(data)
            return await func(*args, response_data=data_as_obj, **kwargs)
        return wrapper
    return decorator

def my_api_chatgpt_old(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        api_url = "https://private-akeno.randydev.my.id/ryuzaki/chatgpt-old"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=kwargs) as response:
                    data = await response.json()
        except Exception:
            return f"API Error: stuck"
        data_as_obj = DictToObj(data)
        return await func(*args, response_data=data_as_obj, **kwargs)
    return wrapper
