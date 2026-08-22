from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import AppException
from app.models.product import Product
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ProductRatingSummary


def list_reviews_for_product(db: Session, product_id: int) -> list[Review]:
    stmt = (
        select(Review)
        .options(joinedload(Review.user))
        .where(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
    )
    return list(db.scalars(stmt))


def get_user_review_for_product(db: Session, user_id: int, product_id: int) -> Review | None:
    return db.scalar(select(Review).where(Review.user_id == user_id, Review.product_id == product_id))


def get_rating_summary(db: Session, product_id: int) -> ProductRatingSummary:
    avg = db.scalar(select(func.avg(Review.rating)).where(Review.product_id == product_id))
    total = db.scalar(select(func.count(Review.id)).where(Review.product_id == product_id)) or 0

    distribution: dict[int, int] = {}
    for stars in range(1, 6):
        count = db.scalar(
            select(func.count(Review.id)).where(Review.product_id == product_id, Review.rating == stars)
        ) or 0
        distribution[stars] = count

    return ProductRatingSummary(
        average=round(float(avg), 1) if avg else 0.0,
        total=total,
        distribution=distribution,
    )


def create_review(db: Session, user: User, payload: ReviewCreate) -> Review:
    product = db.get(Product, payload.product_id)
    if product is None or not product.is_active:
        raise AppException(status_code=404, message="Producto no encontrado")

    existing = get_user_review_for_product(db, user.id, payload.product_id)
    if existing:
        raise AppException(status_code=400, message="Ya has dejado una review para este producto")

    review = Review(
        user_id=user.id,
        product_id=payload.product_id,
        rating=payload.rating,
        title=payload.title,
        comment=payload.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return _load_review_user(db, review)


def update_review(db: Session, user: User, review_id: int, payload: ReviewUpdate) -> Review:
    review = db.get(Review, review_id)
    if review is None:
        raise AppException(status_code=404, message="Review no encontrada")
    if review.user_id != user.id:
        raise AppException(status_code=403, message="No puedes editar esta review")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return _load_review_user(db, review)


def delete_review(db: Session, user: User, review_id: int) -> None:
    review = db.get(Review, review_id)
    if review is None:
        raise AppException(status_code=404, message="Review no encontrada")
    if review.user_id != user.id and user.role.name != "ADMIN":
        raise AppException(status_code=403, message="No puedes eliminar esta review")
    db.delete(review)
    db.commit()


def _load_review_user(db: Session, review: Review) -> Review:
    db.refresh(review)
    if review.user is None:
        user = db.get(User, review.user_id)
        if user:
            review.user = user
    return review
