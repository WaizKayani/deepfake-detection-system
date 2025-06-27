"""
Logging configuration for the Media Authentication System.
"""

import sys
import logging
from typing import Any, Dict
import structlog
from pythonjsonlogger import jsonlogger

from app.core.config import settings


def setup_logging():
    """Setup structured logging configuration."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Set log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("motor").setLevel(logging.WARNING)
    
    # Create logger instance
    logger = structlog.get_logger()
    logger.info("Logging configured", level=settings.LOG_LEVEL)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a logger instance."""
    return structlog.get_logger(name)


class LoggingMiddleware:
    """Middleware for logging HTTP requests."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("http")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Log request
            self.logger.info(
                "HTTP request started",
                method=scope["method"],
                path=scope["path"],
                client=scope.get("client"),
                headers=dict(scope.get("headers", []))
            )
            
            # Track response
            response_status = None
            
            async def send_wrapper(message):
                nonlocal response_status
                if message["type"] == "http.response.start":
                    response_status = message["status"]
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
            
            # Log response
            self.logger.info(
                "HTTP request completed",
                method=scope["method"],
                path=scope["path"],
                status=response_status
            )
        else:
            await self.app(scope, receive, send) 