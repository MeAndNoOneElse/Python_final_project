from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import GroupCreate, GroupMemberResponse, GroupResponse, GroupUpdate
from ..services.group_service import GroupService

router = APIRouter(prefix="/api/groups", tags=["groups"])


class GroupMemberCreate(BaseModel):
    user_id: int
    role: str = "member"


@router.get("", response_model=list[GroupResponse])
def get_groups(user_id: int = Query(...), db: Session = Depends(get_db)):
    return GroupService(db).get_user_groups(user_id)


@router.get("/by-chat/{chat_id}", response_model=GroupResponse)
def get_group_by_chat_id(chat_id: int, db: Session = Depends(get_db)):
    return GroupService(db).get_group_by_chat_id(chat_id)


@router.post("", response_model=GroupResponse)
def create_group(payload: GroupCreate, owner_user_id: int = Query(...), db: Session = Depends(get_db)):
    return GroupService(db).create_group(payload, owner_user_id=owner_user_id)


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: int, db: Session = Depends(get_db)):
    return GroupService(db).get_group(group_id)


@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, payload: GroupUpdate, db: Session = Depends(get_db)):
    return GroupService(db).update_group(group_id, payload)


@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    return GroupService(db).delete_group(group_id)


@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    return GroupService(db).list_members(group_id)


@router.post("/{group_id}/members", response_model=GroupMemberResponse)
def add_group_member(
    group_id: int,
    payload: GroupMemberCreate,
    db: Session = Depends(get_db)
):
    """Добавляет пользователя в группу"""
    return GroupService(db).add_member(group_id, payload.user_id, payload.role)


@router.delete("/{group_id}/members/{user_id}")
def remove_group_member(group_id: int, user_id: int, db: Session = Depends(get_db)):
    """Удаляет пользователя из группы"""
    return GroupService(db).remove_member(group_id, user_id)

