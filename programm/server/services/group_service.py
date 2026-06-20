from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.repositories.group_member_repository import GroupMemberRepository
from ..db.repositories.group_repository import GroupRepository
from ..schemas.schemas import GroupCreate, GroupUpdate


class GroupService:
    def __init__(self, db: Session):
        self.db = db
        self.groups = GroupRepository(db)
        self.members = GroupMemberRepository(db)

    def get_user_groups(self, user_id: int):
        return self.groups.list_by_user(user_id)

    def get_group_by_chat_id(self, chat_id: int):
        group = self.groups.get_by_chat_id(chat_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return group

    def create_group(self, payload: GroupCreate, owner_user_id: int):
        group = self.groups.create(chat_id=payload.chat_id, name=payload.name, mode=payload.mode)
        self.members.add_member(group_id=group.id, user_id=owner_user_id, role="owner")
        self.db.commit()
        self.db.refresh(group)
        return group

    def get_group(self, group_id: int):
        group = self.groups.get(group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        return group

    def update_group(self, group_id: int, payload: GroupUpdate):
        group = self.get_group(group_id)
        fields = payload.model_dump(exclude_unset=True)
        self.groups.update(group, **fields)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete_group(self, group_id: int):
        group = self.get_group(group_id)
        self.members.remove_by_group(group_id)
        self.groups.delete(group)
        self.db.commit()
        return {"status": "deleted"}

    def list_members(self, group_id: int):
        self.get_group(group_id)
        return self.members.list_members_with_users(group_id)

    def add_member(self, group_id: int, user_id: int, role: str = "member"):
        """Добавляет пользователя в группу"""
        member = self.members.add_member(group_id=group_id, user_id=user_id, role=role)
        member = self.members.get_member(group_id=group_id, user_id=user_id)
        if member:
            return member

        self.db.commit()
        self.db.refresh(member)
        return member

    def remove_member(self, group_id: int, user_id: int):
        """Удаляет пользователя из группы"""
        self.get_group(group_id)
        from ..db.group_member import GroupMember
        member = self.db.query(GroupMember).filter(
            (GroupMember.group_id == group_id) &
            (GroupMember.user_id == user_id)
        ).first()

        if not member:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

        self.db.delete(member)
        self.db.commit()
        return {"status": "deleted"}

