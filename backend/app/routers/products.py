from decimal import Decimal

from fastapi import APIRouter, Query

from app.core.dependencies import AdminUser, DbDep, OptionalUser
from app.schemas.common import ApiResponse, Page
from app.schemas.product import (
    ProductApiResponse,
    ProductCreate,
    ProductListApiResponse,
    ProductOut,
    ProductUpdate,
)
from app.services import products as product_service
from app.utils.pagination import validate_page

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("", response_model=ProductListApiResponse, summary="Listar productos con filtros y paginación")
def list_products(
    db: DbDep,
    current_user: OptionalUser = None,
    search: str | None = Query(default=None, description="Buscar por nombre, marca o modelo"),
    category_id: list[int] | None = Query(default=None, description="Filtrar por uno o varios IDs de categoría"),
    brand: list[str] | None = Query(default=None, description="Filtrar por una o varias marcas"),
    min_price: Decimal | None = Query(default=None, gt=0, description="Precio mínimo"),
    max_price: Decimal | None = Query(default=None, gt=0, description="Precio máximo"),
    ordering: str = Query(
        default="-created_at",
        description="Ordenamiento: price, -price, name, -name, created_at, -created_at, stock, -stock",
    ),
    page: int = Query(default=1, ge=1, description="Número de página"),
    page_size: int = Query(default=12, ge=1, le=100, description="Elementos por página"),
) -> ProductListApiResponse:
    validate_page(page, page_size)

    is_admin = bool(current_user) and current_user.role.name == "ADMIN"
    filters = product_service.ProductFilters(
        search=search,
        category_ids=category_id,
        brands=brand,
        min_price=min_price,
        max_price=max_price,
        is_active=None if is_admin else True,
        ordering=ordering,
        include_inactive=is_admin,
    )
    result = product_service.list_products(db, filters, page, page_size)
    result["items"] = [ProductOut.model_validate(p) for p in result["items"]]
    page_data = Page[ProductOut](**result)
    return ProductListApiResponse(success=True, message="Productos obtenidos correctamente", data=page_data)


@router.get("/brands", response_model=ApiResponse[list[str]], summary="Listar marcas disponibles")
def list_brands(db: DbDep) -> ApiResponse[list[str]]:
    return ApiResponse[list[str]](
        success=True, message="Marcas obtenidas correctamente", data=product_service.list_brands(db)
    )


@router.get("/{product_id}", response_model=ProductApiResponse, summary="Obtener un producto por ID")
def get_product(product_id: int, db: DbDep) -> ProductApiResponse:
    product = product_service.get_product_or_404(db, product_id)
    return ProductApiResponse(
        success=True, message="Producto obtenido correctamente", data=ProductOut.model_validate(product)
    )


@router.post(
    "",
    response_model=ProductApiResponse,
    status_code=201,
    summary="Crear producto (admin)",
)
def create_product(payload: ProductCreate, db: DbDep, _admin: AdminUser) -> ProductApiResponse:
    product = product_service.create_product(db, payload)
    return ProductApiResponse(
        success=True, message="Producto creado correctamente", data=ProductOut.model_validate(product)
    )


@router.patch("/{product_id}", response_model=ProductApiResponse, summary="Actualizar producto (admin)")
def update_product(
    product_id: int, payload: ProductUpdate, db: DbDep, _admin: AdminUser
) -> ProductApiResponse:
    product = product_service.update_product(db, product_id, payload)
    return ProductApiResponse(
        success=True,
        message="Producto actualizado correctamente",
        data=ProductOut.model_validate(product),
    )


@router.delete("/{product_id}", response_model=ApiResponse, summary="Eliminar producto (admin)")
def delete_product(product_id: int, db: DbDep, _admin: AdminUser) -> ApiResponse:
    product_service.delete_product(db, product_id)
    return ApiResponse(success=True, message="Producto eliminado correctamente", data=None)
