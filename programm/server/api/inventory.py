from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import (
    InventoryAddRequest,
    InventoryConsumeRequest,
    InventoryMoveRequest,
    InventoryResponse,
    InventoryThresholdRequest,
)
from ..services.inventory_service import InventoryService

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.post("/add", response_model=InventoryResponse)
def add_inventory(payload: InventoryAddRequest, db: Session = Depends(get_db)):
    return InventoryService(db).add_inventory(payload)


@router.post("/consume", response_model=InventoryResponse)
def consume_inventory(payload: InventoryConsumeRequest, db: Session = Depends(get_db)):
    return InventoryService(db).consume_inventory(payload)


@router.post("/move", response_model=InventoryResponse)
def move_inventory(payload: InventoryMoveRequest, db: Session = Depends(get_db)):
    return InventoryService(db).move_inventory(payload)


@router.put("/{inventory_id}/threshold", response_model=InventoryResponse)
def update_threshold(inventory_id: int, payload: InventoryThresholdRequest, db: Session = Depends(get_db)):
    return InventoryService(db).update_threshold(inventory_id, payload)


@router.get("/search-products", response_model=list[str])
def search_products(group_id: int = Query(...), q: str = Query(""), db: Session = Depends(get_db)):
    return InventoryService(db).search_products(group_id=group_id, query=q)

