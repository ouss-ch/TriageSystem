"""Shared FastAPI dependencies (DB session, auth, pagination, etc.)."""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole

# TODO: pagination params

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    user = await db.get(User, int(user_id))
    if user is None:
        raise credentials_error
    return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin role required")
    return user
