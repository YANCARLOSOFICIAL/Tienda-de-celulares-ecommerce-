from fastapi import APIRouter

from app.core.dependencies import AdminUser, CurrentUser, DbDep
from app.schemas.common import ApiResponse
from app.schemas.order import (
    OrderApiResponse,
    OrderCreate,
    OrderDetailOut,
    OrderListApiResponse,
    OrderStatusUpdate,
)
from app.services import orders as order_service

router = APIRouter(prefix="/orders", tags=["Pedidos"])


@router.post(
    "",
    response_model=OrderApiResponse,
    status_code=201,
    summary="Crear un pedido a partir del carrito (checkout)",
    description=(
        "Valida el carrito y el stock, calcula precios reales, descuenta inventario "
        "y vacía el carrito, todo dentro de una única transacción."
    ),
)
def create_order(db: DbDep, current_user: CurrentUser, payload: OrderCreate | None = None) -> OrderApiResponse:
    order = order_service.create_order(db, current_user, payload)
    return OrderApiResponse(
        success=True,
        message="Pedido creado correctamente",
        data=OrderDetailOut.model_validate(order),
    )


@router.get("", response_model=OrderListApiResponse, summary="Listar mis pedidos")
def list_orders(db: DbDep, current_user: CurrentUser) -> OrderListApiResponse:
    orders = order_service.list_orders(db, current_user)
    return OrderListApiResponse(
        success=True,
        message="Pedidos obtenidos correctamente",
        data=[OrderDetailOut.model_validate(o) for o in orders],
    )


@router.get("/{order_id}", response_model=OrderApiResponse, summary="Obtener un pedido por ID")
def get_order(order_id: int, db: DbDep, current_user: CurrentUser) -> OrderApiResponse:
    order = order_service.get_order_for_user(db, current_user, order_id)
    return OrderApiResponse(
        success=True, message="Pedido obtenido correctamente", data=OrderDetailOut.model_validate(order)
    )


@router.post("/{order_id}/cancel", response_model=OrderApiResponse, summary="Cancelar mi pedido")
def cancel_order(order_id: int, db: DbDep, current_user: CurrentUser) -> OrderApiResponse:
    order = order_service.cancel_order(db, current_user, order_id)
    return OrderApiResponse(
        success=True,
        message="Pedido cancelado correctamente",
        data=OrderDetailOut.model_validate(order),
    )


@router.patch(
    "/{order_id}/status",
    response_model=OrderApiResponse,
    summary="Actualizar el estado de un pedido (admin)",
)
def update_order_status(
    order_id: int, payload: OrderStatusUpdate, db: DbDep, _admin: AdminUser
) -> OrderApiResponse:
    order = order_service.update_order_status(db, _admin, order_id, payload.status.value)
    return OrderApiResponse(
        success=True,
        message="Estado del pedido actualizado correctamente",
        data=OrderDetailOut.model_validate(order),
    )
