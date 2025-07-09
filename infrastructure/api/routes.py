from fastapi import APIRouter, Depends, HTTPException
from infrastructure.auth.rate_limit import enforce_rate_limit
from infrastructure.auth.token import validate_token
from infrastructure.auth.oauth2_scheme import oauth2_scheme 
from app.use_cases.interactors.metrics import MetricsInteractor
from infrastructure.api.dependencies import get_metrics_interactor
from infrastructure.errors import UnauthorizedAccessError, MetricsNotFoundError

router = APIRouter()

@router.get("/users/{user_id}/metrics")
async def get_authenticated_user_metrics(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    interactor: MetricsInteractor = Depends(get_metrics_interactor)
):
    try:
        token_user_id = validate_token(token)
        if token_user_id != user_id:
            raise UnauthorizedAccessError()

        enforce_rate_limit(user_id)
        return await interactor.get_user_metrics(user_id)

    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    except MetricsNotFoundError:
        raise HTTPException(status_code=404, detail="Metrics not found")


@router.get("/metrics/{user_id}")
async def get_public_user_metrics(
    user_id: str,
    interactor: MetricsInteractor = Depends(get_metrics_interactor)
):
    try:
        return await interactor.get_user_metrics(user_id)
    except MetricsNotFoundError:
        raise HTTPException(status_code=404, detail="User metrics not found")
