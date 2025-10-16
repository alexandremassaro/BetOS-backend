from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.deps import get_current_active_user
from app.core.security import get_password_hash
from app.entities.user import User, UserCreate, UserPublic, UserUpdate
from app.utils.datetime import utc_now

router = APIRouter()


@router.post("/", response_model=UserPublic)
def create_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    user: UserCreate,
    session: Annotated[Session, Depends(get_session)],
):
    """Create new user"""
    # Check if user exists
    statement = select(User).where(User.email == user.email)
    db_user = session.exec(statement).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")

    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    """Get current user info"""
    return current_user


@router.get("/", response_model=List[UserPublic])
def read_users(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
):
    """Get all users (paginated)"""

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Get user by ID"""

    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


@router.put("/{user_id}}", response_model=UserPublic)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Update user"""
    db_user = read_user(user_id=user_id, session=session)

    # Update fields
    user_data = user_update.model_dump(exclude_unset=True)

    if "password" in user_data:
        user_data["hashed_password"] = get_password_hash(user_data["password"])
        del user_data["password"]

    user_data["updated_at"] = utc_now()

    for field, value in user_data.items():
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[Session, Depends(get_session)],
):
    """Delete user"""

    user = read_user(user_id=user_id, session=session)

    session.delete(user)
    session.commit()
    return {"message": "Usuário excluído com sucesso"}
