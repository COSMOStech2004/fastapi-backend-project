import time
from fastapi import Request

from app.logger import logger


async def request_logging_middleware(
    request: Request,
    call_next
):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} "
        f"status_code={response.status_code} "
        f"process_time={process_time:.4f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)

    return response