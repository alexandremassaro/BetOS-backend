from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security import verify_token
from app.entities.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Get current user from JWT token"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authgenticate": "Bearer"},
    )

    username = verify_token(token)
    if username is None:
        raise credentials_exception

    statement = select(User).where(User.email == username)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current active user"""

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")

    return current_user
