from sqlalchemy.orm import Session

from ..group import Group


class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_user(self, user_id: int) -> list[Group]:
        from ..group_member import GroupMember

        return (
            self.db.query(Group)
            .join(GroupMember, GroupMember.group_id == Group.id)
            .filter(GroupMember.user_id == user_id)
            .all()
        )

    def create(self, chat_id: int, name: str, mode, notifications_enabled: bool = True, auto_shopping_list: bool = True) -> Group:
        group = Group(
            chat_id=chat_id,
            name=name,
            mode=mode,
            notifications_enabled=notifications_enabled,
            auto_shopping_list=auto_shopping_list,
        )
        self.db.add(group)
        self.db.flush()
        return group

    def get(self, group_id: int):
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_by_chat_id(self, chat_id: int):
        return self.db.query(Group).filter(Group.chat_id == chat_id).first()

    def update(self, group: Group, **fields) -> Group:
        for key, value in fields.items():
            setattr(group, key, value)
        self.db.flush()
        return group

    def delete(self, group: Group) -> None:
        self.db.delete(group)
        self.db.flush()

