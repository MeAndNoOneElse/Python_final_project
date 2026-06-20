from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import ShoppingListCreate, ShoppingListResponse, ShoppingListUpdate
from ..services.shopping_list_service import ShoppingListService

router = APIRouter(tags=["shopping-list"])


@router.get("/api/groups/{group_id}/shopping-list", response_model=list[ShoppingListResponse])
def get_group_shopping_list(group_id: int, db: Session = Depends(get_db)):
    return ShoppingListService(db).list_for_group(group_id)


@router.post("/api/shopping-list", response_model=ShoppingListResponse)
def create_shopping_item(payload: ShoppingListCreate, db: Session = Depends(get_db)):
    return ShoppingListService(db).create_item(payload)


@router.put("/api/shopping-list/{item_id}", response_model=ShoppingListResponse)
def update_shopping_item(item_id: int, payload: ShoppingListUpdate, db: Session = Depends(get_db)):
    item = ShoppingListService(db).update_item(item_id, payload)
    if item is None:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping list item not found")
    return item


@router.delete("/api/shopping-list/{item_id}")
def delete_shopping_item(item_id: int, db: Session = Depends(get_db)):
    deleted = ShoppingListService(db).delete_item(item_id)
    if not deleted:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping list item not found")
    return {"status": "deleted"}


@router.post("/api/shopping-list/{item_id}/buy")
def buy_shopping_item(item_id: int, db: Session = Depends(get_db)):
    result = ShoppingListService(db).buy_item(item_id)
    if result is None:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping list item not found")
    return result

