# original developer @xpushz

import asyncio

from pyrogram import Client
from pyrogram.errors import AuthKeyInvalid, UserDeactivated

import akenoai.logger as fast


class CreateTaskManagerClient:
    def __init__(self):
        pass

    async def check_session_user_health(self, client: Client, user_id: int, callback_func: callable, interval: int = 300) -> None:
        while True:
            try:
                await asyncio.wait_for(client.get_me(), timeout=10)
                if not client.is_connected:
                    raise ConnectionError("Client disconnected")
                await fast.info(f"Session health OK: User {user_id}")
                await asyncio.sleep(interval)
            except (UserDeactivated, AuthKeyInvalid) as e:
                await fast.warning(f"💀 Session dead for {user_id}: {type(e).__name__}")
                await callback_func(user_id)
                break
            except Exception as e:
                await fast.warning(f"Health check failed for {user_id}: {type(e).__name__}: {str(e)}")
                await asyncio.sleep(60)

    async def _check_connection(self, client: Client) -> bool:
        try:
            return await client.get_me() is not None
        except:
            return False

    async def connection_watchdog(self, client: Client):
        while True:
            if not await self._check_connection(client):
                await fast.warning("Reconnecting...")
                await client.disconnect()
                await client.connect()
            await asyncio.sleep(300)
