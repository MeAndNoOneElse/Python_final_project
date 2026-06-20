from pydantic import BaseModel


class GroupMember(BaseModel):
    user_id: int
    group_id: int
