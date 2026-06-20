from pydantic import BaseModel, Json
from enum import Enum
from datetime import datetime


class ConfirmationType(str, Enum):
    DEBT = "debt"
    DISTRIBUTION = "distribution"
    SETTLEMENT = "settlement"


class PendingConfirmation(BaseModel):
    id: int
    user_id: int
    type: ConfirmationType
    data: Json
    expires_at: datetime
