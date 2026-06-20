from sqlalchemy.orm import Session

from ..group_member import GroupMember


class GroupMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_member(self, group_id: int, user_id: int, role: str = "member") -> GroupMember:
        member = GroupMember(group_id=group_id, user_id=user_id, role=role)
        self.db.add(member)
        self.db.flush()
        return member

    def get_member(self, group_id: int, user_id: int) -> GroupMember | None:
        return (
            self.db.query(GroupMember)
            .filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id)
            .first()
        )

        return self.db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    def remove_by_group(self, group_id: int) -> None:
        self.db.query(GroupMember).filter(GroupMember.group_id == group_id).delete()
    def list_members_with_users(self, group_id: int) -> list[dict]:
        from ..user import User

        rows = (
            self.db.query(GroupMember, User)
            .join(User, User.id == GroupMember.user_id)
            .filter(GroupMember.group_id == group_id)
            .all()
        )
        return [
            {
                "id": member.id,
                "user_id": member.user_id,
                "group_id": member.group_id,
                "role": member.role,
                "joined_at": member.joined_at,
                "name": user.name,
                "username": user.username,
                "telegram_id": user.telegram_id,
            }
            for member, user in rows
        ]


