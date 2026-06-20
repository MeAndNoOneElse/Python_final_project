from sqlalchemy.orm import Session

from ..inventory import Inventory


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_storage(self, storage_id: int) -> list[Inventory]:
        return self.db.query(Inventory).filter(Inventory.storage_location_id == storage_id).all()

    def get(self, inventory_id: int):
        return self.db.query(Inventory).filter(Inventory.id == inventory_id).first()

    def get_by_name(self, storage_id: int, product_name: str):
        return (
            self.db.query(Inventory)
            .filter(
                Inventory.storage_location_id == storage_id,
                Inventory.product_name == product_name,
            )
            .first()
        )

    def create(self, storage_id: int, product_name: str, quantity: float, unit: str, min_threshold: float) -> Inventory:
        item = Inventory(
            storage_location_id=storage_id,
            product_name=product_name,
            quantity=quantity,
            unit=unit,
            min_threshold=min_threshold,
        )
        self.db.add(item)
        self.db.flush()
        return item

    def update(self, inventory: Inventory, **fields) -> Inventory:
        for key, value in fields.items():
            setattr(inventory, key, value)
        self.db.flush()
        return inventory

    def delete_by_storage(self, storage_id: int) -> None:
        self.db.query(Inventory).filter(Inventory.storage_location_id == storage_id).delete()

    def search_products_in_group(self, group_id: int, query: str) -> list[str]:
        from ..storage_location import StorageLocation

        rows = (
            self.db.query(Inventory.product_name)
            .join(StorageLocation, StorageLocation.id == Inventory.storage_location_id)
            .filter(StorageLocation.group_id == group_id, Inventory.product_name.ilike(f"%{query}%"))
            .distinct()
            .all()
        )
        return [row[0] for row in rows]

