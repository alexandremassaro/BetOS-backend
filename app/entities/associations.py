from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.utils.datetime import utc_now


class UserRole(SQLModel, table=True):
    __tablename__ = "users_roles"  # type: ignore

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True
    )
    assigned_at: Optional[datetime] = Field(default_factory=utc_now)
    assigned_by: Optional[int] = Field(default=None, foreign_key="users.id")
