from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
from logger.logger import logger  # Importing the logger from the logger module
from datetime import datetime

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = datetime.now()
        logger.info(f"{start_time} - Starting request")
        try:
            response = await call_next(request)
            process_time = datetime.now() - start_time
            logger.info(f"{start_time} - Request processed successfully in {process_time.total_seconds()} seconds")
            return response
        except Exception as e:
            logger.exception(f"{start_time} - An error occurred while processing the request")
            raise
