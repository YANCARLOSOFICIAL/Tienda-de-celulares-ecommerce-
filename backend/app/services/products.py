from decimal import Decimal

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.pagination import compute_pages

ORDERING_FIELDS = {
    "price": Product.price,
    "-price": Product.price.desc(),
    "name": Product.name,
    "-name": Product.name.desc(),
    "created_at": Product.created_at,
    "-created_at": Product.created_at.desc(),
    "stock": Product.stock,
    "-stock": Product.stock.desc(),
}


class ProductFilters:
    def __init__(
        self,
        search: str | None = None,
        category_ids: list[int] | None = None,
        brands: list[str] | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        is_active: bool | None = None,
        ordering: str = "-created_at",
        include_inactive: bool = False,
    ):
        self.search = search
        self.category_ids = [c for c in (category_ids or []) if c is not None]
        self.brands = [b.strip() for b in (brands or []) if b and b.strip()]
        self.min_price = min_price
        self.max_price = max_price
        self.is_active = is_active
        self.ordering = ordering
        self.include_inactive = include_inactive

    def apply(self, stmt: Select) -> Select:
        if self.search:
            pattern = f"%{self.search.strip()}%"
            stmt = stmt.where(
                or_(
                    Product.name.ilike(pattern),
                    Product.brand.ilike(pattern),
                    Product.model.ilike(pattern),
                )
            )
        if self.category_ids:
            stmt = stmt.where(Product.category_id.in_(self.category_ids))
        if self.brands:
            stmt = stmt.where(Product.brand.in_(self.brands))
        if self.min_price is not None:
            stmt = stmt.where(Product.price >= self.min_price)
        if self.max_price is not None:
            stmt = stmt.where(Product.price <= self.max_price)
        if self.is_active is not None:
            stmt = stmt.where(Product.is_active == self.is_active)
        elif not self.include_inactive:
            stmt = stmt.where(Product.is_active.is_(True))
        return stmt

    def order(self, stmt: Select) -> Select:
        column = ORDERING_FIELDS.get(self.ordering)
        if column is None:
            raise AppException(
                status_code=422,
                message=(
                    "Parámetro 'ordering' inválido. Valores permitidos: "
                    + ", ".join(ORDERING_FIELDS.keys())
                ),
            )
        return stmt.order_by(column)


def get_product_or_404(db: Session, product_id: int, include_inactive: bool = False) -> Product:
    product = db.get(Product, product_id)
    if product is None:
        raise AppException(status_code=404, message="Producto no encontrado")
    if not product.is_active and not include_inactive:
        raise AppException(status_code=404, message="Producto no encontrado")
    return product


def list_products(db: Session, filters: ProductFilters, page: int, page_size: int) -> dict:
    base = filters.apply(select(Product))
    total = db.scalar(select(func.count()).select_from(base.subquery())) or 0
    stmt = filters.order(base).offset((page - 1) * page_size).limit(page_size)
    items = list(db.scalars(stmt))
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": compute_pages(total, page_size),
    }


def list_brands(db: Session) -> list[str]:
    """Marcas distintas de productos activos, ordenadas alfabéticamente."""
    stmt = (
        select(Product.brand)
        .where(Product.is_active.is_(True))
        .distinct()
        .order_by(Product.brand)
    )
    return [b for b in db.scalars(stmt) if b]


def _validate_category(db: Session, category_id: int | None) -> None:
    if category_id is not None and db.get(Category, category_id) is None:
        raise AppException(status_code=404, message="Categoría no encontrada")


def create_product(db: Session, payload: ProductCreate) -> Product:
    _validate_category(db, payload.category_id)
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_product_or_404(db, product_id, include_inactive=True)
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)

    if "category_id" in changes:
        _validate_category(db, changes["category_id"])
        product.category_id = changes["category_id"]

    for field in ("name", "description", "price", "stock", "brand", "model", "image", "images", "is_active"):
        if field in changes:
            setattr(product, field, changes[field])

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product_or_404(db, product_id, include_inactive=True)
    db.delete(product)
    db.commit()
