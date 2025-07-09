# main.py
from fastapi import FastAPI
from infrastructure.api.routes import router as api_router
from infrastructure.api.middlewares import add_middlewares

app = FastAPI(
    title="User Metrics API",
    description="Secure API for user metrics with JWT authentication",
    version="1.0.0"
)

app.include_router(api_router)
add_middlewares(app)