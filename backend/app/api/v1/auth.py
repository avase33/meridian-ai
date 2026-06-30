"""JWT authentication endpoints."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db

router    = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx   = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2    = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

ALGORITHM = "HS256"
TOKEN_TTL = timedelta(hours=8)


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    expires_in:   int


class TokenData(BaseModel):
    sub:    str        # user_id
    org_id: str
    role:   str


def create_access_token(data: dict) -> str:
    payload = {**data, "exp": datetime.now(timezone.utc) + TOKEN_TTL}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2)],
    db:    Annotated[AsyncSession, Depends(get_db)],
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(sub=user_id, org_id=payload.get("org_id", ""), role=payload.get("role", "viewer"))
    except JWTError:
        raise credentials_exception


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    """Exchange email + password for a JWT access token."""
    # TODO: look up user from DB and verify password
    # For the scaffold we accept admin@example.com / changeme
    if form_data.username != "admin@example.com" or form_data.password != "changeme":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({
        "sub":    "user-admin",
        "org_id": "org-default",
        "role":   "admin",
    })
    return Token(access_token=token, expires_in=int(TOKEN_TTL.total_seconds()))