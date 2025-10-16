from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.config import settings
from app.core.database import get_session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.entities.user import Token, User, UserPublic

router = APIRouter()


@router.post("login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
):
    """Login endpoint to get JWT token"""
    if form_data.username == "admin":
        create_admin(session)

    statement = select(User).where(
        User.username == form_data.username or User.email == form_data.username
    )
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)


def create_admin(session: Annotated[Session, Depends(get_session)]):
    """Create admin user if it doesn't exist"""

    statement = select(User).where(User.username == "admin")
    admin_user = session.exec(statement).first()

    if admin_user:
        return admin_user

    hashed_password = get_password_hash("betos")
    admin_user = User(
        email="admin@betos.com",
        username="admin",
        hashed_password=hashed_password,
    )
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    return admin_user
