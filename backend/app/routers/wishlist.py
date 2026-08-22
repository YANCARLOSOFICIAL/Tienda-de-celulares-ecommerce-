from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbDep
from app.schemas.common import ApiResponse
from app.schemas.wishlist import WishlistApiResponse, WishlistItemOut
from app.services import wishlist as wishlist_service

router = APIRouter(prefix="/wishlist", tags=["Favoritos"])


@router.get("", response_model=WishlistApiResponse, summary="Listar favoritos")
def list_wishlist(db: DbDep, current_user: CurrentUser) -> WishlistApiResponse:
    items = wishlist_service.list_wishlist(db, current_user)
    return WishlistApiResponse(
        success=True,
        message="Favoritos obtenidos correctamente",
        data=[WishlistItemOut.model_validate(i) for i in items],
    )


@router.post("/{product_id}", response_model=ApiResponse, status_code=201, summary="Agregar a favoritos")
def add_to_wishlist(product_id: int, db: DbDep, current_user: CurrentUser) -> ApiResponse:
    wishlist_service.add_to_wishlist(db, current_user, product_id)
    return ApiResponse(success=True, message="Producto agregado a favoritos", data=None)


@router.delete("/{product_id}", response_model=ApiResponse, summary="Eliminar de favoritos")
def remove_from_wishlist(product_id: int, db: DbDep, current_user: CurrentUser) -> ApiResponse:
    wishlist_service.remove_from_wishlist(db, current_user, product_id)
    return ApiResponse(success=True, message="Producto eliminado de favoritos", data=None)
