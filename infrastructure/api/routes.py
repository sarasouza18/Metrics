from infrastructure.auth.rate_limiter import enforce_rate_limit

@router.get("/users/{user_id}/metrics")
async def get_user_metrics(
    user_id: str,
    token: str = Depends(oauth2_scheme),
    interactor: MetricsInteractor = Depends(get_metrics_interactor)
):
    try:
        token_user_id = validate_token(token)
        if token_user_id != user_id:
            raise UnauthorizedAccessError()
        
        enforce_rate_limit(user_id)  # 🚦 aplica rate limit
        return await interactor.get_user_metrics(user_id)

    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    except MetricsNotFoundError:
        raise HTTPException(status_code=404, detail="Metrics not found")
