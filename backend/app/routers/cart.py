from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbDep
from app.schemas.cart import (
    CartApiResponse,
    CartItemApiResponse,
    CartItemCreate,
    CartItemOut,
    CartItemUpdate,
    CartMessageApiResponse,
)
from app.schemas.common import ApiResponse
from app.services import cart as cart_service

router = APIRouter(prefix="/cart", tags=["Carrito"])


@router.get("", response_model=CartApiResponse, summary="Obtener el carrito del usuario autenticado")
def get_cart(db: DbDep, current_user: CurrentUser) -> CartApiResponse:
    data = cart_service.get_cart_data(db, current_user)
    return CartApiResponse(success=True, message="Carrito obtenido correctamente", data=data)


@router.post(
    "/items",
    response_model=CartItemApiResponse,
    status_code=201,
    summary="Agregar un producto al carrito",
)
def add_item(
    payload: CartItemCreate, db: DbDep, current_user: CurrentUser
) -> CartItemApiResponse:
    item = cart_service.add_item(db, current_user, payload)
    return CartItemApiResponse(
        success=True, message="Producto agregado al carrito", data=CartItemOut.model_validate(item)
    )


@router.patch(
    "/items/{item_id}",
    response_model=CartItemApiResponse,
    summary="Modificar la cantidad de un ítem del carrito",
)
def update_item(
    item_id: int, payload: CartItemUpdate, db: DbDep, current_user: CurrentUser
) -> CartItemApiResponse:
    item = cart_service.update_item_quantity(db, current_user, item_id, payload.quantity)
    return CartItemApiResponse(
        success=True, message="Cantidad actualizada correctamente", data=CartItemOut.model_validate(item)
    )


@router.delete(
    "/items/{item_id}",
    response_model=CartMessageApiResponse,
    summary="Eliminar un ítem del carrito",
)
def remove_item(item_id: int, db: DbDep, current_user: CurrentUser) -> CartMessageApiResponse:
    cart_service.remove_item(db, current_user, item_id)
    return CartMessageApiResponse(success=True, message="Ítem eliminado del carrito", data=None)


@router.delete("", response_model=CartMessageApiResponse, summary="Vaciar el carrito")
def clear_cart(db: DbDep, current_user: CurrentUser) -> CartMessageApiResponse:
    cart_service.clear_cart(db, current_user)
    return CartMessageApiResponse(success=True, message="Carrito vaciado", data=None)
