
from typing import Any
from datetime import timedelta, datetime, timezone
from app.core.config import settings

from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer

ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/auth/user/login",
)

def create_access_token(
        subject: str,
        expires_delta: timedelta | None = None,
    ) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    payload: dict[str, Any] ={
        "sub": subject,
        "exp": expire
    }
    
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )
    
    
def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

    except JWTError:
        raise ValueError("Invalid token")