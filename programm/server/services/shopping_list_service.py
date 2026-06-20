from sqlalchemy.orm import Session

from ..db.repositories.inventory_repository import InventoryRepository
from ..db.repositories.shopping_list_repository import ShoppingListRepository
from ..schemas.schemas import ShoppingListCreate, ShoppingListUpdate


class ShoppingListService:
    def __init__(self, db: Session):
        self.db = db
        self.shopping_repo = ShoppingListRepository(db)
        self.inventory_repo = InventoryRepository(db)

    def list_for_group(self, group_id: int):
        return self.shopping_repo.list_by_group(group_id)

    def create_item(self, payload: ShoppingListCreate):
        item = self.shopping_repo.create(
            group_id=payload.group_id,
            product_name=payload.product_name,
            quantity=payload.quantity,
            storage_location_id=payload.storage_location_id,
        )
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item(self, item_id: int, payload: ShoppingListUpdate):
        item = self.shopping_repo.get(item_id)
        if not item:
            return None
        self.shopping_repo.update(item, **payload.model_dump(exclude_unset=True))
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item_id: int) -> bool:
        item = self.shopping_repo.get(item_id)
        if not item:
            return False
        self.shopping_repo.delete(item)
        self.db.commit()
        return True

    def buy_item(self, item_id: int):
        item = self.shopping_repo.get(item_id)
        if not item:
            return None

        if item.storage_location_id is not None:
            inventory = self.inventory_repo.get_by_name(item.storage_location_id, item.product_name)
            if inventory is None:
                self.inventory_repo.create(
                    storage_id=item.storage_location_id,
                    product_name=item.product_name,
                    quantity=item.quantity,
                    unit="pcs",
                    min_threshold=0,
                )
            else:
                self.inventory_repo.update(inventory, quantity=inventory.quantity + item.quantity)

        self.shopping_repo.delete(item)
        self.db.commit()
        return {"status": "bought"}

    def add_low_stock_if_needed(
        self,
        group_id: int,
        storage_id: int,
        product_name: str,
        quantity: float,
        threshold: float,
    ):
        if quantity > threshold:
            return
        if self.shopping_repo.exists_open_item(
            group_id=group_id, product_name=product_name
        ):
            return
        self.shopping_repo.create(
            group_id=group_id,
            product_name=product_name,
            quantity=max(threshold - quantity, 1),
            storage_location_id=storage_id,
            is_critical=quantity <= 0,
        )
