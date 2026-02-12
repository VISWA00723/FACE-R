"""
Simple in-memory rate limiter middleware.
"""
from collections import defaultdict, deque
from time import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60, protected_prefix: str = "/api/v1/auth/login"):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.protected_prefix = protected_prefix
        self.requests = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(self.protected_prefix):
            client_ip = request.client.host if request.client else "unknown"
            key = f"{client_ip}:{request.url.path}"
            now = time()
            history = self.requests[key]

            while history and now - history[0] > self.window_seconds:
                history.popleft()

            if len(history) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many login attempts. Please try again later."},
                )

            history.append(now)

        return await call_next(request)
