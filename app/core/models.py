from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Base(SQLModel):
    pass


class RoleBase(SQLModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class Role(RoleBase, table=True):
    id: int = Field(default=None, primary_key=True)
