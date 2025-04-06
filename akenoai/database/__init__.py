import datetime
import time

from motor import motor_asyncio

from akenoai.database.types import *
from akenoai.logger import LOGS


class Database:
    def __init__(self, initdev: MongoInitConfig) -> None:
        self.client: AgnosticClient = motor_asyncio.AsyncIOMotorClient(initdev.url)
        self.db = self.client[initdev.name]
        self.backup_chatbot = self.db["chat_history"]

    async def connect(self):
        try:
            await self.client.admin.command("ping")
            LOGS.info("Database Connection Established!")
        except Exception as e:
            LOGS.error(f"DatabaseErr: {e}")
            raise

    async def _close_(self):
        await self.client.close()

    async def update_chatbot_from_db(self, u: WhereFind, chatbot_chat):
        await self.backup_chatbot.update_one(
            {"user_id": u.user_id},
            {"$set": {"chatbot_chat": chatbot_chat}},
            upsert=True
        )

    async def get_chatbot_from_db(self, u: WhereFind):
        user_data = await self.backup_chatbot.find_one({"user_id": u.user_id})
        return user_data.get("chatbot_chat", []) if user_data else []

    async def none_chatbot_from_db(self, u: WhereFind):
        return await self.backup_chatbot.update_one(
            {"user_id": u.user_id},
            {"$unset": {"chatbot_chat": None}}
        )

    async def del_chatbot_from_db(self, u: WhereFind):
        result = await self.none_chatbot_from_db(u)
        if result.modified_count > 0:
            return "Chat history cleared successfully."
        else:
            return "No chat history found to clear."

__all__ = ["Database"]
