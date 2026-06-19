from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status


RATE_LIMIT_STORE = {}


def rate_limiter(
    max_requests: int,
    window_seconds: int,
    name: str
):
    def dependency(request: Request):
        client_ip = request.client.host if request.client else "unknown"

        key = f"{name}:{client_ip}"

        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)

        request_times = RATE_LIMIT_STORE.get(key, [])

        request_times = [
            request_time
            for request_time in request_times
            if request_time > window_start
        ]

        if len(request_times) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )

        request_times.append(now)

        RATE_LIMIT_STORE[key] = request_times

    return dependency


login_rate_limit = rate_limiter(
    max_requests=5,
    window_seconds=60,
    name="login"
)


forgot_password_rate_limit = rate_limiter(
    max_requests=3,
    window_seconds=15 * 60,
    name="forgot_password"
)


resend_verification_rate_limit = rate_limiter(
    max_requests=3,
    window_seconds=15 * 60,
    name="resend_verification"
)