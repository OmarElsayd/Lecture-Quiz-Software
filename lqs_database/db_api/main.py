import logging
from . import login
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI(
    title="LQS Database API",
    description="API for LQS Database",
    version="1.0.0",
)

app.include_router(login.router)
