from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppException(Exception):
    """Excepción de aplicación con código de estado y mensaje propio."""

    def __init__(self, status_code: int, message: str, errors: list[str] | None = None):
        self.status_code = status_code
        self.message = message
        self.errors = errors or []


def register_exception_handlers(app: FastAPI) -> None:
    """Registra manejadores globales de errores con un formato de respuesta consistente."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message, "errors": exc.errors},
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": str(exc.detail), "errors": []},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = []
        for err in exc.errors():
            loc = ".".join(str(item) for item in err.get("loc", []) if item != "body")
            errors.append(f"{loc}: {err.get('msg', 'valor inválido')}")
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": "Error de validación", "errors": errors},
        )
