# infrastructure/auth/jwt_handler.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.domain.exceptions import UnauthorizedAccessError
import os

# Configuration (should be in settings)
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedAccessError()
        return user_id
    except JWTError:
        raise UnauthorizedAccessError()