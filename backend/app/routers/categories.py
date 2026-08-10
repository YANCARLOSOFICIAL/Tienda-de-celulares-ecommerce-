from fastapi import APIRouter

from app.core.dependencies import AdminUser, DbDep
from app.schemas.category import (
    CategoryApiResponse,
    CategoryCreate,
    CategoryListApiResponse,
    CategoryOut,
    CategoryUpdate,
)
from app.schemas.common import ApiResponse
from app.services import categories as category_service

router = APIRouter(prefix="/categories", tags=["Categorías"])


@router.get("", response_model=CategoryListApiResponse, summary="Listar categorías")
def list_categories(db: DbDep) -> CategoryListApiResponse:
    categories = category_service.list_categories(db)
    return CategoryListApiResponse(
        success=True,
        message="Categorías obtenidas correctamente",
        data=[CategoryOut.model_validate(c) for c in categories],
    )


@router.get("/{category_id}", response_model=CategoryApiResponse, summary="Obtener una categoría")
def get_category(category_id: int, db: DbDep) -> CategoryApiResponse:
    category = category_service.get_category_or_404(db, category_id)
    return CategoryApiResponse(
        success=True, message="Categoría obtenida correctamente", data=CategoryOut.model_validate(category)
    )


@router.post(
    "",
    response_model=CategoryApiResponse,
    status_code=201,
    summary="Crear categoría (admin)",
)
def create_category(payload: CategoryCreate, db: DbDep, _admin: AdminUser) -> CategoryApiResponse:
    category = category_service.create_category(db, payload)
    return CategoryApiResponse(
        success=True, message="Categoría creada correctamente", data=CategoryOut.model_validate(category)
    )


@router.patch(
    "/{category_id}",
    response_model=CategoryApiResponse,
    summary="Actualizar categoría (admin)",
)
def update_category(
    category_id: int, payload: CategoryUpdate, db: DbDep, _admin: AdminUser
) -> CategoryApiResponse:
    category = category_service.update_category(db, category_id, payload)
    return CategoryApiResponse(
        success=True,
        message="Categoría actualizada correctamente",
        data=CategoryOut.model_validate(category),
    )


@router.delete(
    "/{category_id}",
    response_model=ApiResponse,
    summary="Eliminar categoría (admin)",
)
def delete_category(category_id: int, db: DbDep, _admin: AdminUser) -> ApiResponse:
    category_service.delete_category(db, category_id)
    return ApiResponse(success=True, message="Categoría eliminada correctamente", data=None)
