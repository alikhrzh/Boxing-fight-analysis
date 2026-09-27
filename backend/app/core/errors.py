from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str) -> None:
        super().__init__(
            code=f"{resource}_not_found",
            message=f"{resource.replace('_', ' ').title()} was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"id": resource_id},
        )


class ConflictError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message, status.HTTP_409_CONFLICT)


class UploadError(AppError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(code, message, status.HTTP_400_BAD_REQUEST)


def _error_body(error: AppError) -> dict[str, Any]:
    body: dict[str, Any] = {"error": {"code": error.code, "message": error.message}}
    if error.details is not None:
        body["error"]["details"] = error.details
    return body


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, error: AppError) -> JSONResponse:
        return JSONResponse(status_code=error.status_code, content=_error_body(error))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _: Request, error: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "The request contains invalid data.",
                    "details": error.errors(),
                }
            },
        )
