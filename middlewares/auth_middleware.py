# middlewares/auth_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
from fastapi import Request, HTTPException

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, excluded_paths: list = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths if excluded_paths else []

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)

        access_token = request.headers.get("Authorization")
        if not access_token:
            raise HTTPException(status_code=401, detail="Authorization required")
        
        response = await call_next(request)
        return response
