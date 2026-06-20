from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import (
    InventoryResponse,
    StorageCreate,
    StorageResponse,
    StorageUpdate,
    StorageWithCountResponse,
)
from ..services.inventory_service import InventoryService
from ..services.storage_service import StorageService

router = APIRouter(tags=["storage"])


@router.get("/api/groups/{group_id}/storage", response_model=list[StorageWithCountResponse])
def list_group_storage(group_id: int, db: Session = Depends(get_db)):
    return StorageService(db).list_group_storage(group_id)


@router.post("/api/storage", response_model=StorageResponse)
def create_storage(payload: StorageCreate, db: Session = Depends(get_db)):
    return StorageService(db).create_storage(payload)


@router.put("/api/storage/{storage_id}", response_model=StorageResponse)
def update_storage(storage_id: int, payload: StorageUpdate, db: Session = Depends(get_db)):
    return StorageService(db).update_storage(storage_id, payload)


@router.delete("/api/storage/{storage_id}")
def delete_storage(storage_id: int, db: Session = Depends(get_db)):
    return StorageService(db).delete_storage(storage_id)


@router.get("/api/storage/{storage_id}/inventory", response_model=list[InventoryResponse])
def list_storage_inventory(storage_id: int, db: Session = Depends(get_db)):
    return InventoryService(db).list_storage_inventory(storage_id)

