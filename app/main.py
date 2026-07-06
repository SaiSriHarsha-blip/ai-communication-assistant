# pyrefly: ignore [missing-import]
from fastapi import FastAPI

# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware

# pyrefly: ignore [missing-import]
from slowapi.errors import RateLimitExceeded

# pyrefly: ignore [missing-import]
from slowapi.middleware import SlowAPIMiddleware

# pyrefly: ignore [missing-import]
from slowapi import _rate_limit_exceeded_handler

from app.api.message import router as message_router

from app.core.exception_handler import register_exception_handlers
from app.core.logging_middleware import LoggingMiddleware
from app.core.security_headers import SecurityHeadersMiddleware
from app.core.rate_limiter import limiter

app = FastAPI(
    title="AI Communication Agent",
    description="An AI agent that generates platform-specific messages.",
    version="0.1.0",
)

# Register exception handlers
register_exception_handlers(app)

# Middlewares
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)

# Rate Limiter
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(SlowAPIMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(
    message_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "ok",
        "project": "AI Communication Agent",
        "version": "0.1.0",
    }