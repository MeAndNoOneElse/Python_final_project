from pydantic import BaseModel


class User(BaseModel):
    telegram_id: int
    name: str
    username: str
