"""Auth crypto: user password hashing, JWT issuance, and mailbox-password encryption.

Two distinct needs live here:
  - bcrypt hashing (one-way) for user login passwords.
  - Fernet encryption (reversible) for mailbox passwords, since the sweep
    worker needs the plaintext back to authenticate against IMAP.
"""

import datetime
from typing import Optional

import bcrypt
import jwt
from cryptography.fernet import Fernet

from app.core.config import settings

_fernet = Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_password(password: str) -> str:
    return _fernet.encrypt(password.encode()).decode()


def decrypt_password(token: str) -> str:
    return _fernet.decrypt(token.encode()).decode()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_access_token(subject: str, expires_delta: Optional[datetime.timedelta] = None) -> str:
    expire = datetime.datetime.now(datetime.timezone.utc) + (
        expires_delta or datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
