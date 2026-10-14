from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger()

class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.error("application_error", message=exc.message, status_code=exc.status_code, path=request.url.path)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_exception", error=str(exc), path=request.url.path)
        return JSONResponse(
            status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "message": "An internal server error occurred.",
                    "details": {"error": str(exc)} if app.debug else {}
                }
            }
        )
