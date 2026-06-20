from pydantic import BaseModel


class StorageLocation(BaseModel):
    id: int
    name: str
    group_id: int
    is_default: bool
