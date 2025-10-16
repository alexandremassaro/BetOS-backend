import typing
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.utils.datetime import utc_now

from .associations import UserRole

if TYPE_CHECKING:
    from .role import Role


class UserBase(SQLModel):
    """Base user model with common fields"""

    email: str = Field(unique=True, index=True, max_length=320)
    username: str = Field(unique=True, index=True, max_length=50)
    full_name: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User table model"""

    __tablename__: str = "users"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default_factory=utc_now)
    updated_at: Optional[datetime] = Field(default_factory=utc_now)
    roles: List["Role"] = Relationship(
        back_populates="users",
        link_model=UserRole,
        sa_relationship_kwargs={"foreign_keys": "[UserRole.user_id, UserRole.role_id]"},
    )


class UserCreate(UserBase):
    """Schema for creating users"""

    password: str


class UserUpdate(SQLModel):
    """Schema for updating users"""

    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserPublic(UserBase):
    """Public user schema (without sensitive data)"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserWithPassword(UserPublic):
    """User schema with hashed password (for internal use)"""

    hashed_password: str


class Token(SQLModel):
    """JWT Token response"""

    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    """Token payload data"""

    username: Optional[str] = None
