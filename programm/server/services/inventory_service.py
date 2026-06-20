from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.repositories.inventory_repository import InventoryRepository
from ..db.repositories.storage_repository import StorageRepository
from ..schemas.schemas import (
    InventoryAddRequest,
    InventoryConsumeRequest,
    InventoryMoveRequest,
    InventoryThresholdRequest,
)
from .shopping_list_service import ShoppingListService


class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_repo = InventoryRepository(db)
        self.storage_repo = StorageRepository(db)
        self.shopping_service = ShoppingListService(db)

    def list_storage_inventory(self, storage_id: int):
        return self.inventory_repo.list_by_storage(storage_id)

    def add_inventory(self, payload: InventoryAddRequest):
        storage = self.storage_repo.get(payload.storage_id)
        if not storage:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Storage not found")
        item = self.inventory_repo.get_by_name(payload.storage_id, payload.product_name)
        if item is None:
            item = self.inventory_repo.create(
                storage_id=payload.storage_id,
                product_name=payload.product_name,
                quantity=payload.quantity,
                unit=payload.unit,
                min_threshold=payload.min_threshold,
            )
        else:
            item = self.inventory_repo.update(
                item,
                quantity=item.quantity + payload.quantity,
                unit=payload.unit,
                min_threshold=payload.min_threshold,
            )
        self.db.commit()
        self.db.refresh(item)
        return item

    def consume_inventory(self, payload: InventoryConsumeRequest):
        item = self.inventory_repo.get(payload.inventory_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")

        next_quantity = max(item.quantity - payload.quantity, 0)
        item = self.inventory_repo.update(item, quantity=next_quantity)

        storage = self.storage_repo.get(item.storage_location_id)
        if storage:
            self.shopping_service.add_low_stock_if_needed(
                group_id=storage.group_id,
                storage_id=storage.id,
                product_name=item.product_name,
                quantity=item.quantity,
                threshold=item.min_threshold,
            )

        self.db.commit()
        self.db.refresh(item)
        return item

    def move_inventory(self, payload: InventoryMoveRequest):
        item = self.inventory_repo.get(payload.inventory_id)
        if not item or item.storage_location_id != payload.from_storage_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found in source storage")

        if item.quantity < payload.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough quantity to move")

        destination = self.storage_repo.get(payload.to_storage_id)
        if not destination:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination storage not found")

        self.inventory_repo.update(item, quantity=item.quantity - payload.quantity)

        target_item = self.inventory_repo.get_by_name(payload.to_storage_id, item.product_name)
        if target_item is None:
            target_item = self.inventory_repo.create(
                storage_id=payload.to_storage_id,
                product_name=item.product_name,
                quantity=payload.quantity,
                unit=item.unit,
                min_threshold=item.min_threshold,
            )
        else:
            self.inventory_repo.update(target_item, quantity=target_item.quantity + payload.quantity)

        self.db.commit()
        self.db.refresh(target_item)
        return target_item

    def update_threshold(self, inventory_id: int, payload: InventoryThresholdRequest):
        item = self.inventory_repo.get(inventory_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
        self.inventory_repo.update(item, min_threshold=payload.min_threshold)
        self.db.commit()
        self.db.refresh(item)
        return item

    def search_products(self, group_id: int, query: str) -> list[str]:
        return self.inventory_repo.search_products_in_group(group_id, query)

