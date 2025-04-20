from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging import get_logger

logger = get_logger(__name__)

async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(
            "unhandled_error",
            error=str(e),
            path=request.url.path,
            method=request.method
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )