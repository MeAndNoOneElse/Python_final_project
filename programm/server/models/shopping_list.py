from pydantic import BaseModel


class ShoppingListItem(BaseModel):
    id: int
    group_id: int
    storage_location_id: int
    product_name: str
    quantity: float
    is_purchased: bool
