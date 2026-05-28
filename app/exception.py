from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.logger import logger


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
):
    logger.warning(
        f"HTTP error: status_code={exc.status_code}, detail={exc.detail}, path={request.url.path}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.warning(
        f"Validation error: path={request.url.path}, errors={exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        f"Unexpected error: path={request.url.path}, error={str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )