"""
Authentication service with JWT tokens and password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional
import os
import secrets
import hashlib

from sqlalchemy.orm import Session
from app.database import User


# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    try:
        salt, password_hash = hashed_password.split(":")
        return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
    except ValueError:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a simple token (base64 encoded)."""
    import base64
    import json

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.isoformat()})

    # Create a simple token
    token_data = json.dumps(to_encode)
    token = base64.urlsafe_b64encode(token_data.encode()).decode()

    # Add signature
    signature = hashlib.sha256((token + SECRET_KEY).encode()).hexdigest()[:16]

    return f"{token}.{signature}"


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify a token."""
    import base64
    import json

    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None

        token_data, signature = parts

        # Verify signature
        expected_signature = hashlib.sha256((token_data + SECRET_KEY).encode()).hexdigest()[:16]
        if signature != expected_signature:
            return None

        # Decode data
        data = json.loads(base64.urlsafe_b64decode(token_data.encode()).decode())

        # Check expiration
        exp = datetime.fromisoformat(data.get("exp", ""))
        if datetime.utcnow() > exp:
            return None

        return data
    except Exception:
        return None


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, password: str, full_name: str) -> User:
    """Create a new user."""
    hashed_password = hash_password(password)
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def update_user_profile(db: Session, user_id: int, profile_data: dict) -> Optional[User]:
    """Update user profile."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for key, value in profile_data.items():
        if hasattr(user, key) and key not in ["id", "email", "hashed_password", "created_at"]:
            setattr(user, key, value)

    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def get_current_user(db: Session, token: str) -> Optional[User]:
    """Get the current user from a token."""
    data = decode_token(token)
    if not data:
        return None

    user_id = data.get("sub")
    if not user_id:
        return None

    return get_user_by_id(db, int(user_id))
