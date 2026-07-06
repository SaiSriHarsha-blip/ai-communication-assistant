import logging

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException, Request

# pyrefly: ignore [missing-import] 
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception("Unhandled server exception")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error.",
            },
        )