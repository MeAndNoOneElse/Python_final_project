from pydantic import BaseModel


class Inventory(BaseModel):
    id: int
    storage_location_id: int
    product_name: str
    quantity: float
    unit: str
    min_threshold: float
