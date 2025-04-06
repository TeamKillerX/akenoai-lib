from typing import *

from pydantic import BaseModel  # type: ignore


class MongoInitConfig(BaseModel):
    name: str
    url: str

class WhereFind(BaseModel):
    user_id: Optional[int] = 0

__all__ = [
    "MongoInitConfig",
    "WhereFind"
]
