from decimal import Decimal

from fastapi import APIRouter

from app.core.dependencies import AdminUser, DbDep
from app.schemas.common import ApiResponse
from app.schemas.coupon import (
    CouponApiResponse,
    CouponCreate,
    CouponListApiResponse,
    CouponOut,
    CouponUpdate,
    CouponValidateOut,
    CouponValidateResponse,
)
from app.services import coupons as coupon_service

router = APIRouter(prefix="/coupons", tags=["Cupones"])


@router.get("", response_model=CouponListApiResponse, summary="Listar cupones (admin)")
def list_coupons(db: DbDep, _admin: AdminUser) -> CouponListApiResponse:
    coupons = coupon_service.list_coupons(db)
    return CouponListApiResponse(
        success=True,
        message="Cupones obtenidos correctamente",
        data=[CouponOut.model_validate(c) for c in coupons],
    )


@router.get("/{coupon_id}", response_model=CouponApiResponse, summary="Obtener un cupon")
def get_coupon(coupon_id: int, db: DbDep, _admin: AdminUser) -> CouponApiResponse:
    coupon = coupon_service.get_coupon(db, coupon_id)
    return CouponApiResponse(
        success=True, message="Cupon obtenido correctamente", data=CouponOut.model_validate(coupon)
    )


@router.post("", response_model=CouponApiResponse, status_code=201, summary="Crear cupon")
def create_coupon(payload: CouponCreate, db: DbDep, _admin: AdminUser) -> CouponApiResponse:
    coupon = coupon_service.create_coupon(db, payload)
    return CouponApiResponse(
        success=True, message="Cupon creado correctamente", data=CouponOut.model_validate(coupon)
    )


@router.patch("/{coupon_id}", response_model=CouponApiResponse, summary="Actualizar cupon")
def update_coupon(coupon_id: int, payload: CouponUpdate, db: DbDep, _admin: AdminUser) -> CouponApiResponse:
    coupon = coupon_service.update_coupon(db, coupon_id, payload)
    return CouponApiResponse(
        success=True, message="Cupon actualizado correctamente", data=CouponOut.model_validate(coupon)
    )


@router.delete("/{coupon_id}", response_model=ApiResponse, summary="Eliminar cupon")
def delete_coupon(coupon_id: int, db: DbDep, _admin: AdminUser) -> ApiResponse:
    coupon_service.delete_coupon(db, coupon_id)
    return ApiResponse(success=True, message="Cupon eliminado correctamente", data=None)


@router.post("/validate", response_model=CouponValidateResponse, summary="Validar cupon (usuario)")
def validate_coupon(code: str, subtotal: Decimal, db: DbDep) -> CouponValidateResponse:
    coupon = coupon_service.validate_coupon(db, code, subtotal)
    return CouponValidateResponse(
        success=True,
        message="Cupon valido",
        data=CouponValidateOut.model_validate(coupon),
    )
