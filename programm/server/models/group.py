from pydantic import BaseModel
from enum import Enum


class GroupMode(str, Enum):
    FAMILY = "family"
    FRIENDS = "friends"


class Group(BaseModel):
    chat_id: int
    name: str
    mode: GroupMode
