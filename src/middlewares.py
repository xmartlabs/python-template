from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog import contextvars
from structlog.contextvars import bound_contextvars


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = str(uuid4())

        contextvars.clear_contextvars()
        contextvars.bind_contextvars(
            request_id=request_id,
            # You may need to sanitize or truncate user agent as it could be fingerprinted to help uniquely identify a
            # user — not PII by itself, but becomes sensitive when paired with a user ID.
            user_agent=request.headers.get("user-agent"),
        )
        with bound_contextvars(request_id=request_id):
            response = await call_next(request)

        return response
