# main.py

from fastapi import FastAPI
from infrastructure.api.routes import router as api_router
from infrastructure.monitoring.prometheus import setup_metrics

app = FastAPI(
    title="User Metrics API",
    version="1.0.0"
)

setup_metrics(app)

app.include_router(api_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
