"""Registration + login — issues JWT access tokens used to authenticate other routes.

The first account ever registered is bootstrapped as admin; every account after
that is a plain member. TODO: replace with a proper invite/promotion flow before
real deployment — this is a dev-stage bootstrap, not an access-control model.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.auth import Token, UserRead, UserRegisterRequest

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="email already registered")

    # Bootstrap first user as admin, all others are members
    user_count = await db.scalar(select(func.count()).select_from(User))
    role = UserRole.admin if user_count == 0 else UserRole.member

    user = User(email=payload.email, hashed_password=hash_password(payload.password), role=role)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="incorrect email or password")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)
