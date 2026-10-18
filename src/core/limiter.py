from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger()

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.warning("rate_limit_exceeded", client=get_remote_address(request), path=request.url.path)
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Too many requests. Please try again later."}
    )
