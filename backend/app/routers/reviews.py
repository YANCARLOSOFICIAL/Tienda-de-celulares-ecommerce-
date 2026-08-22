from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbDep
from app.schemas.common import ApiResponse
from app.schemas.review import (
    RatingSummaryApiResponse,
    ReviewApiResponse,
    ReviewCreate,
    ReviewListApiResponse,
    ReviewOut,
    ReviewUpdate,
)
from app.services import reviews as review_service

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/product/{product_id}", response_model=ReviewListApiResponse, summary="Reviews de un producto")
def list_reviews(product_id: int, db: DbDep) -> ReviewListApiResponse:
    reviews = review_service.list_reviews_for_product(db, product_id)
    return ReviewListApiResponse(
        success=True,
        message="Reviews obtenidas correctamente",
        data=[ReviewOut.model_validate(r) for r in reviews],
    )


@router.get("/product/{product_id}/rating", response_model=RatingSummaryApiResponse, summary="Resumen de calificacion")
def get_rating_summary(product_id: int, db: DbDep) -> RatingSummaryApiResponse:
    summary = review_service.get_rating_summary(db, product_id)
    return RatingSummaryApiResponse(
        success=True,
        message="Resumen obtenido correctamente",
        data=summary,
    )


@router.post("", response_model=ReviewApiResponse, status_code=201, summary="Crear review")
def create_review(payload: ReviewCreate, db: DbDep, current_user: CurrentUser) -> ReviewApiResponse:
    review = review_service.create_review(db, current_user, payload)
    return ReviewApiResponse(
        success=True,
        message="Review creada correctamente",
        data=ReviewOut.model_validate(review),
    )


@router.patch("/{review_id}", response_model=ReviewApiResponse, summary="Actualizar review")
def update_review(review_id: int, payload: ReviewUpdate, db: DbDep, current_user: CurrentUser) -> ReviewApiResponse:
    review = review_service.update_review(db, current_user, review_id, payload)
    return ReviewApiResponse(
        success=True,
        message="Review actualizada correctamente",
        data=ReviewOut.model_validate(review),
    )


@router.delete("/{review_id}", response_model=ApiResponse, summary="Eliminar review")
def delete_review(review_id: int, db: DbDep, current_user: CurrentUser) -> ApiResponse:
    review_service.delete_review(db, current_user, review_id)
    return ApiResponse(success=True, message="Review eliminada correctamente", data=None)
