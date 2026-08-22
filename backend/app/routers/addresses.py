from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbDep
from app.schemas.address import (
    AddressApiResponse,
    AddressCreate,
    AddressListApiResponse,
    AddressOut,
    AddressUpdate,
)
from app.schemas.common import ApiResponse
from app.services import addresses as address_service

router = APIRouter(prefix="/addresses", tags=["Direcciones"])


@router.get("", response_model=AddressListApiResponse, summary="Listar mis direcciones")
def list_addresses(db: DbDep, current_user: CurrentUser) -> AddressListApiResponse:
    addresses = address_service.list_addresses(db, current_user)
    return AddressListApiResponse(
        success=True,
        message="Direcciones obtenidas correctamente",
        data=[AddressOut.model_validate(a) for a in addresses],
    )


@router.get("/{address_id}", response_model=AddressApiResponse, summary="Obtener una direccion")
def get_address(address_id: int, db: DbDep, current_user: CurrentUser) -> AddressApiResponse:
    address = address_service.get_address_or_404(db, current_user, address_id)
    return AddressApiResponse(
        success=True, message="Direccion obtenida correctamente", data=AddressOut.model_validate(address)
    )


@router.post("", response_model=AddressApiResponse, status_code=201, summary="Crear direccion")
def create_address(payload: AddressCreate, db: DbDep, current_user: CurrentUser) -> AddressApiResponse:
    address = address_service.create_address(db, current_user, payload)
    return AddressApiResponse(
        success=True, message="Direccion creada correctamente", data=AddressOut.model_validate(address)
    )


@router.patch("/{address_id}", response_model=AddressApiResponse, summary="Actualizar direccion")
def update_address(
    address_id: int, payload: AddressUpdate, db: DbDep, current_user: CurrentUser
) -> AddressApiResponse:
    address = address_service.update_address(db, current_user, address_id, payload)
    return AddressApiResponse(
        success=True, message="Direccion actualizada correctamente", data=AddressOut.model_validate(address)
    )


@router.delete("/{address_id}", response_model=ApiResponse, summary="Eliminar direccion")
def delete_address(address_id: int, db: DbDep, current_user: CurrentUser) -> ApiResponse:
    address_service.delete_address(db, current_user, address_id)
    return ApiResponse(success=True, message="Direccion eliminada correctamente", data=None)
