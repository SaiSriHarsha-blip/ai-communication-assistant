import time
import logging

# pyrefly: ignore [missing-import]
from fastapi import Request
# pyrefly: ignore [missing-import]
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        duration = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "%s %s | %s | %sms",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )

        return response