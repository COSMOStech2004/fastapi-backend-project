from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.middlewar import request_logging_middleware
from app.routers.user_rotuers import router
from fastapi.middleware.cors import CORSMiddleware
from app.exception import (
    http_exception_handler,
    validation_exception_handler,
    
    general_exception_handler
)
from app.routers.auth import router as auth_router
from app.routers.user_rotuers import router as user_router
from app.routers.admin import router as admin_router

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(request_logging_middleware)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Auth"]
)

app.include_router(
    user_router,
    prefix="/api/v1/users",
    tags=["Users"]
)

app.include_router(
    admin_router,
    prefix="/api/v1/admin",
    tags=["Admin"]
)