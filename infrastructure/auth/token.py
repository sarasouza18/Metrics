from jose import JWTError, jwt
import os
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("JWT_SECRET", "mysecret")
ALGORITHM = "HS256"

def validate_token(token) -> str:
    try:
        if isinstance(token, HTTPAuthorizationCredentials):
            token = token.credentials

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token payload")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
