import os
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from typing import Union

SECRET_KEY = os.getenv("JWT_SECRET", "mysecret")
ALGORITHM = "HS256"

def validate_token(token: Union[str, HTTPAuthorizationCredentials]) -> str:
    try:
        if isinstance(token, HTTPAuthorizationCredentials):
            token = token.credentials

        if not isinstance(token, str) or len(token.split(".")) != 3:
            raise HTTPException(status_code=403, detail="Malformed token")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if not user_id or not isinstance(user_id, str):
            raise HTTPException(status_code=403, detail="Invalid token payload: missing 'sub'")

        return user_id

    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")

    except JWTError as e:
        raise HTTPException(status_code=403, detail=f"Invalid token: {str(e)}")
