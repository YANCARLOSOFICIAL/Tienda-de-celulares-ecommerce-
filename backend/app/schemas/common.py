from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ORMModel(BaseModel):
    """Base para schemas que se construyen desde objetos ORM."""

    model_config = ConfigDict(from_attributes=True)


class ApiResponse(BaseModel, Generic[T]):
    """Envoltorio de respuesta consistente para toda la API."""

    success: bool = True
    message: str = "OK"
    data: T | None = None


class ApiError(BaseModel):
    """Formato de error consistente para toda la API."""

    success: bool = False
    message: str
    errors: list[str] = []


class Page(BaseModel, Generic[T]):
    """Resultado paginado genérico."""

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int
