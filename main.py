import os
from dotenv import load_dotenv

load_dotenv()  # ← Adicionado para carregar variáveis do .env

from fastapi import FastAPI
from infrastructure.api.routes import router as api_router
from infrastructure.monitoring.prometheus import setup_metrics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="User Metrics API",
    version="1.0.0"
)

setup_metrics(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
