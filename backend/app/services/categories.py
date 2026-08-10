from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug import slugify


def get_category_or_404(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if category is None:
        raise AppException(status_code=404, message="Categoría no encontrada")
    return category


def list_categories(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.name)))


def create_category(db: Session, payload: CategoryCreate) -> Category:
    name = payload.name.strip()
    if db.scalar(select(Category).where(Category.name == name)):
        raise AppException(status_code=409, message="Ya existe una categoría con ese nombre")

    base_slug = slugify(name)
    slug = base_slug
    counter = 2
    while db.scalar(select(Category).where(Category.slug == slug)):
        slug = f"{base_slug}-{counter}"
        counter += 1

    category = Category(name=name, slug=slug, description=payload.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, payload: CategoryUpdate) -> Category:
    category = get_category_or_404(db, category_id)
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)

    if "name" in changes:
        new_name = changes["name"].strip()
        duplicate = db.scalar(
            select(Category).where(Category.name == new_name, Category.id != category_id)
        )
        if duplicate:
            raise AppException(status_code=409, message="Ya existe una categoría con ese nombre")
        category.name = new_name
        category.slug = slugify(new_name)

    if "description" in changes:
        category.description = changes["description"]

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category_or_404(db, category_id)
    if category.products:
        raise AppException(
            status_code=409,
            message="No se puede eliminar: la categoría tiene productos asociados",
        )
    db.delete(category)
    db.commit()
