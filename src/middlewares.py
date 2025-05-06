from typing import Awaitable, Callable
from uuid import uuid4

import structlog
from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog import contextvars
from structlog.contextvars import bound_contextvars

from src.core.security import AuthManager

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Middleware to add logging context to each request.
        """
        context = {
            "request_id": str(uuid4()),
            # You may need to sanitize or truncate user agent as it could be fingerprinted to help uniquely identify a
            # user — not PII by itself, but becomes sensitive when paired with a user ID.
            "user_agent": request.headers.get("user-agent"),
            # Adding path without query parameters to the context
            "path": request.url.path.split("?")[0],
            "method": request.method,
        }

        try:
            token_payload = await AuthManager().get_token_payload(request)
            if token_payload:
                context["user_id"] = str(token_payload.user_id)
        except HTTPException as e:
            if e.status_code == 401:
                # If the token is invalid, we can just ignore it and continue
                logger.bind(**context).debug("Invalid token")
            else:
                raise e

        contextvars.clear_contextvars()
        with bound_contextvars(**context):
            response = await call_next(request)

        return response
