# infrastructure/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.use_cases.metrics_interactor import MetricsInteractor
from app.domain.exceptions import UnauthorizedAccessError, MetricsNotFoundError
from infrastructure.auth.jwt_handler import validate_token
from infrastructure.api.dependencies import get_metrics_interactor

router = APIRouter(prefix="/api/v1")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/{user_id}/metrics")
async def get_user_metrics(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    interactor: MetricsInteractor = Depends(get_metrics_interactor)
):
    try:
        # Validate token and check if user has access
        token_user_id = validate_token(token)
        if token_user_id != user_id:
            raise UnauthorizedAccessError()
        
        return interactor.get_user_metrics(user_id)
    
    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    except MetricsNotFoundError:
        raise HTTPException(status_code=404, detail="Metrics not found")
    
@router.get("/metrics")
async def metrics():
    return metrics_endpoint()