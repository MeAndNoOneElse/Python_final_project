from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.inventory import Inventory
from ..db.repositories.inventory_repository import InventoryRepository
from ..db.repositories.storage_repository import StorageRepository
from ..schemas.schemas import StorageCreate, StorageUpdate, StorageWithCountResponse


class StorageService:
    def __init__(self, db: Session):
        self.db = db
        self.storage_repo = StorageRepository(db)
        self.inventory_repo = InventoryRepository(db)

    def list_group_storage(self, group_id: int) -> list[StorageWithCountResponse]:
        storages = self.storage_repo.list_by_group(group_id)
        result: list[StorageWithCountResponse] = []
        for storage in storages:
            product_count = (
                self.db.query(Inventory)
                .filter(Inventory.storage_location_id == storage.id, Inventory.quantity > 0)
                .count()
            )
            result.append(
                StorageWithCountResponse(
                    id=storage.id,
                    name=storage.name,
                    group_id=storage.group_id,
                    is_default=storage.is_default,
                    product_count=product_count,
                )
            )
        return result

    def create_storage(self, payload: StorageCreate):
        if payload.is_default:
            self.storage_repo.reset_default_for_group(payload.group_id)
        storage = self.storage_repo.create(
            group_id=payload.group_id,
            name=payload.name,
            is_default=payload.is_default,
        )
        self.db.commit()
        self.db.refresh(storage)
        return storage

    def update_storage(self, storage_id: int, payload: StorageUpdate):
        storage = self.storage_repo.get(storage_id)
        if not storage:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Storage not found")
        fields = payload.model_dump(exclude_unset=True)
        if fields.get("is_default"):
            self.storage_repo.reset_default_for_group(storage.group_id)
        self.storage_repo.update(storage, **fields)
        self.db.commit()
        self.db.refresh(storage)
        return storage

    def delete_storage(self, storage_id: int):
        storage = self.storage_repo.get(storage_id)
        if not storage:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Storage not found")
        self.inventory_repo.delete_by_storage(storage_id)
        self.storage_repo.delete(storage)
        self.db.commit()
        return {"status": "deleted"}
