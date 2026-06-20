from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from ..models.group import GroupMode


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GroupCreate(BaseModel):
    chat_id: int
    name: str
    mode: GroupMode


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    mode: Optional[GroupMode] = None
    notifications_enabled: Optional[bool] = None
    auto_shopping_list: Optional[bool] = None


class GroupResponse(ORMModel):
    id: int
    chat_id: int
    name: str
    mode: GroupMode
    notifications_enabled: bool
    auto_shopping_list: bool
    created_at: datetime


class GroupMemberResponse(BaseModel):
    id: Optional[int] = None
    group_id: int
    role: str
    joined_at: datetime

    name: Optional[str] = None
    username: Optional[str] = None
    telegram_id: Optional[int] = None

class StorageCreate(BaseModel):
    group_id: int
    name: str
    is_default: bool = False


class StorageUpdate(BaseModel):
    name: Optional[str] = None
    is_default: Optional[bool] = None


class StorageResponse(ORMModel):
    id: int
    name: str
    group_id: int
    is_default: bool


class StorageWithCountResponse(StorageResponse):
    product_count: int


class InventoryAddRequest(BaseModel):
    storage_id: int
    product_name: str
    quantity: float = Field(gt=0)
    unit: str = "pcs"
    min_threshold: float = Field(default=0, ge=0)


class InventoryConsumeRequest(BaseModel):
    inventory_id: int
    quantity: float = Field(gt=0)


class InventoryMoveRequest(BaseModel):
    inventory_id: int
    from_storage_id: int
    to_storage_id: int
    quantity: float = Field(gt=0)


class InventoryThresholdRequest(BaseModel):
    min_threshold: float = Field(ge=0)


class InventoryResponse(ORMModel):
    id: int
    storage_location_id: int
    product_name: str
    quantity: float
    unit: str
    min_threshold: float
    updated_at: datetime


class ShoppingListCreate(BaseModel):
    group_id: int
    product_name: str
    quantity: float = Field(gt=0)
    storage_location_id: Optional[int] = None


class ShoppingListUpdate(BaseModel):
    quantity: Optional[float] = Field(default=None, gt=0)
    storage_location_id: Optional[int] = None


class ShoppingListResponse(ORMModel):
    id: int
    group_id: int
    storage_location_id: Optional[int]
    product_name: str
    quantity: float
    is_purchased: bool
    is_critical: bool


class ExpenseItemCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: float = Field(default=1, gt=0)
    unit: str = "pcs"


class ExpenseManualCreate(BaseModel):
    group_id: int
    uploaded_by_user_id: int
    title: str
    total_amount: float = Field(gt=0)
    category: str
    purchase_date: Optional[date] = None
    participant_ids: list[int] = Field(default_factory=list)
    is_grocery: bool = False
    storage_location_id: Optional[int] = None
    items: list[ExpenseItemCreate] = Field(default_factory=list)
    comment: Optional[str] = None


class ExpenseResponse(ORMModel):
    id: int
    group_id: int
    uploaded_by_user_id: int
    title: str
    total_amount: float
    category: str
    purchase_date: Optional[date]
    is_grocery: bool
    status: str
    comment: Optional[str]


class DebtResponse(ORMModel):
    id: int
    group_id: Optional[int]
    receipt_id: Optional[int]
    from_user_id: int
    to_user_id: int
    amount: float
    is_settled: bool
    created_at: datetime
    settled_at: Optional[datetime]


class BalanceResponse(BaseModel):
    user_id: int
    group_id: int
    total_owed: float
    total_due: float
    net_balance: float


class ConfirmationResponse(ORMModel):
    id: int
    user_id: int
    type: str
    data: dict[str, Any]
    created_at: datetime
    expires_at: datetime
    is_approved: bool
    is_rejected: bool


class UserSettingsUpdate(BaseModel):
    default_storage_id: Optional[int] = None
    notifications_enabled: Optional[bool] = None
    preferred_unit: Optional[str] = None
    language: Optional[str] = None


class UserResponse(ORMModel):
    id: int
    telegram_id: int
    name: str
    username: Optional[str]
    language: str
    preferred_unit: str
    notifications_enabled: bool
    default_storage_id: Optional[int]
    created_at: datetime


class DashboardStatsResponse(BaseModel):
    groups_count: int
    total_open_debts: float
    low_stock_products: int
    pending_confirmations: int

