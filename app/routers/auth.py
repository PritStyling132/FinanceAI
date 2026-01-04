"""
Authentication API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import timedelta

from sqlalchemy.orm import Session
from app.database import get_db, User
from app.services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
    update_user_profile,
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# Pydantic models for requests/responses
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserProfileUpdate(BaseModel):
    age: Optional[int] = None
    annual_income: Optional[float] = None
    current_savings: Optional[float] = None
    monthly_investment: Optional[float] = None
    debt_amount: Optional[float] = None
    risk_tolerance: Optional[str] = None
    investment_horizon: Optional[int] = None
    goals: Optional[List[str]] = None
    has_emergency_fund: Optional[bool] = None
    has_retirement_account: Optional[bool] = None

    # Alias for frontend compatibility
    income: Optional[float] = None


class UserProfileResponse(BaseModel):
    id: int
    email: str
    full_name: str
    age: Optional[int]
    annual_income: float
    current_savings: float
    monthly_investment: float
    debt_amount: float
    risk_tolerance: str
    investment_horizon: int
    goals: list
    has_emergency_fund: bool
    has_retirement_account: bool


def get_current_user_from_header(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = parts[1]
    user = get_current_user(db, token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = create_user(db, user_data.email, user_data.password, user_data.full_name)

    # Create token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    user = authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    )


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user_from_header)):
    """Get current user profile."""
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        age=current_user.age,
        annual_income=current_user.annual_income or 0,
        current_savings=current_user.current_savings or 0,
        monthly_investment=current_user.monthly_investment or 0,
        debt_amount=current_user.debt_amount or 0,
        risk_tolerance=current_user.risk_tolerance or "moderate",
        investment_horizon=current_user.investment_horizon or 10,
        goals=current_user.goals or [],
        has_emergency_fund=current_user.has_emergency_fund or False,
        has_retirement_account=current_user.has_retirement_account or False
    )


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """Update user profile."""
    update_data = profile_data.model_dump(exclude_none=True)

    # Handle income alias
    if "income" in update_data:
        update_data["annual_income"] = update_data.pop("income")

    user = update_user_profile(db, current_user.id, update_data)

    return UserProfileResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        age=user.age,
        annual_income=user.annual_income or 0,
        current_savings=user.current_savings or 0,
        monthly_investment=user.monthly_investment or 0,
        debt_amount=user.debt_amount or 0,
        risk_tolerance=user.risk_tolerance or "moderate",
        investment_horizon=user.investment_horizon or 10,
        goals=user.goals or [],
        has_emergency_fund=user.has_emergency_fund or False,
        has_retirement_account=user.has_retirement_account or False
    )


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user_from_header)):
    """Get basic current user info."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }
