from sqlalchemy.orm import Session

from ..storage_location import StorageLocation


class StorageRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_group(self, group_id: int) -> list[StorageLocation]:
        return self.db.query(StorageLocation).filter(StorageLocation.group_id == group_id).all()

    def create(self, group_id: int, name: str, is_default: bool) -> StorageLocation:
        storage = StorageLocation(group_id=group_id, name=name, is_default=is_default)
        self.db.add(storage)
        self.db.flush()
        return storage

    def get(self, storage_id: int):
        return self.db.query(StorageLocation).filter(StorageLocation.id == storage_id).first()

    def reset_default_for_group(self, group_id: int) -> None:
        self.db.query(StorageLocation).filter(StorageLocation.group_id == group_id).update({"is_default": False})

    def update(self, storage: StorageLocation, **fields) -> StorageLocation:
        for key, value in fields.items():
            setattr(storage, key, value)
        self.db.flush()
        return storage

    def delete(self, storage: StorageLocation) -> None:
        self.db.delete(storage)
        self.db.flush()

