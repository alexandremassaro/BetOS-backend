from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.entities.associations import UserRole
from app.utils.datetime import utc_now

if TYPE_CHECKING:
    from .user import User


class RoleBase(SQLModel):
    """Base role model with common fields"""

    name: str = Field(unique=True, index=True, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)


class Role(RoleBase, table=True):
    """Role table model"""

    __tablename__: str = "roles"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=utc_now)
    updated_at: Optional[datetime] = Field(default_factory=utc_now)

    users: List["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole,
        sa_relationship_kwargs={"foreign_keys": "[UserRole.role_id, UserRole.user_id]"},
    )


class RoleCreate(RoleBase):
    """Schema for creating roles"""

    name: str


class RoleUpdate(SQLModel):
    """Schema for updating roles"""

    name: Optional[str] = None
    is_active: Optional[bool] = None


class RolePublic(RoleBase):
    """Public role schema (without sensitive data)"""

    id: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
