import logging
from . import login, register
from .instructor_apis import instructor_api
from .students_api import student_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app")

app = FastAPI(
    title="LQS Database API",
    description="API for LQS Database",
    version="1.0.0",
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(register.router)
app.include_router(instructor_api.router)
app.include_router(student_api.router)
