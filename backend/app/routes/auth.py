# imports from libs
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

# Local imports
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate, TokenResponse, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    oauth2_scheme,
    get_current_user
)
from app.models.token_blacklist import BlacklistedToken

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    email = payload.email.strip().lower()
    first_name = payload.first_name.strip()
    last_name = payload.last_name.strip()

    # --- Check if user exists ---
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # --- Hash password ---
    hashed_password = hash_password(payload.password)

    # --- Create user ---
    new_user = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
    )

    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email might already be registered"
        )
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating the user"
        )

    return new_user

# Login route
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login a user and return a JWT token"
)
async def login_user(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    email = payload.email.strip().lower()
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    access_token = create_access_token({"user_id": user.id})

    return TokenResponse(access_token=access_token)


# Profile route
@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get the user profile of the logged-in person"
)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


# Logout route
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    # Check if token already blacklisted
    result = await db.execute(select(BlacklistedToken).where(BlacklistedToken.token == token))
    exists = result.scalar_one_or_none()
    
    if exists:
        return {"message": "Already logged out"}

    # Save token to blacklist
    blacklisted = BlacklistedToken(token=token)
    db.add(blacklisted)
    await db.commit()

    return {"message": "Logged out successfully"}