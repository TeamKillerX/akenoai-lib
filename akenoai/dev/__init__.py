import time

from pyrogram import Client

from akenoai.logger import LOGS
from akenoai.types import *


class AkenoAIClient(Client):
    def __init__(self, dev: PyrogramConfig, fast_updates=False):
        self.dev = dev
        super().__init__(
            self.dev.name,
            app_version=self.dev.app_version,
            api_id=self.dev.api_id,
            api_hash=self.dev.api_hash,
            bot_token=self.dev.bot_token,
            plugins=dict(root=self.dev.plugins),
        )
    async def start(self):
        await super().start()
        self.me = await self.get_me()
        self.start_time = time.time()
        LOGS.info(
            "running with Pyrogram v%s (Layer %s) started on @%s. Hi!",
            __version__,
            layer,
            self.me.username,
        )

    async def stop(self):
        await super().stop()
        LOGS.warning("stopped, Bye!")

__all__ = ["AkenoAIClient"]
