from typing import *
from pydantic import BaseModel # type: ignore

class MongoInitConfig(BaseModel):
    name: str
    url: str
