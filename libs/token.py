import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from schemas.user import CurrentUser
from core.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        id: str = payload.get("id")
        email: str = payload.get("email")

        if email is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token Not Match")
        return CurrentUser(id=id, email=email)
    except InvalidTokenError:
        raise credentials_exception 