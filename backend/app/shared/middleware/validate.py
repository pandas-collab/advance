"""Request validation middleware."""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any
import re

class RequestValidationMiddleware:
    """Middleware for request validation and rate limiting."""

    def __init__(self, app):
        self.app = app
        self.rate_limits: Dict[str, Dict[str, Any]] = {}

    async def __call__(self, scope, receive, send):
        """Process request through validation."""
        if scope["type"] == "http":
            request = Request(scope, receive)

            # Rate limiting
            client_ip = request.client.host
            if await self._is_rate_limited(client_ip):
                response = JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Too many requests"}
                )
                await response(scope, receive, send)
                return

            # Input validation
            if request.method in ["POST", "PUT", "PATCH"]:
                await self._validate_request_body(request)

        await self.app(scope, receive, send)

    async def _is_rate_limited(self, client_ip: str) -> bool:
        """Check if client IP is rate limited."""
        current_time = time.time()

        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = {
                "requests": 1,
                "window_start": current_time
            }
            return False

        client_data = self.rate_limits[client_ip]

        # Reset window if needed (60 second window)
        if current_time - client_data["window_start"] > 60:
            client_data["requests"] = 1
            client_data["window_start"] = current_time
            return False

        # Check limit (100 requests per minute)
        if client_data["requests"] >= 100:
            return True

        client_data["requests"] += 1
        return False

    async def _validate_request_body(self, request: Request):
        """Validate request body content."""
        try:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                body = await request.json()

                # Basic validation rules
                if isinstance(body, dict):
                    for key, value in body.items():
                        # Sanitize string inputs
                        if isinstance(value, str):
                            if len(value) > 10000:  # Max length check
                                raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Field {key} is too long"
                                )

                            # Basic XSS prevention
                            if re.search(r'<script|javascript:|data:', value, re.IGNORECASE):
                                raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid content detected"
                                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
