from sqlalchemy.orm import Session

from ..shopping_list import ShoppingListItem


class ShoppingListRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_group(self, group_id: int) -> list[ShoppingListItem]:
        return self.db.query(ShoppingListItem).filter(ShoppingListItem.group_id == group_id).all()

    def get(self, item_id: int):
        return self.db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()

    def create(self, group_id: int, product_name: str, quantity: float, storage_location_id, is_critical: bool = False) -> ShoppingListItem:
        item = ShoppingListItem(
            group_id=group_id,
            product_name=product_name,
            quantity=quantity,
            storage_location_id=storage_location_id,
            is_critical=is_critical,
        )
        self.db.add(item)
        self.db.flush()
        return item

    def update(self, item: ShoppingListItem, **fields) -> ShoppingListItem:
        for key, value in fields.items():
            setattr(item, key, value)
        self.db.flush()
        return item

    def delete(self, item: ShoppingListItem) -> None:
        self.db.delete(item)
        self.db.flush()

    def exists_open_item(self, group_id: int, product_name: str) -> bool:
        return (
            self.db.query(ShoppingListItem)
            .filter(
                ShoppingListItem.group_id == group_id,
                ShoppingListItem.product_name == product_name,
                ShoppingListItem.is_purchased.is_(False),
            )
            .first()
            is not None
        )

