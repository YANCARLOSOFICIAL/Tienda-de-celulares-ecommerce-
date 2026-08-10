"""Seed de desarrollo: roles, usuarios, categorías y productos de prueba.

Uso:
    python -m scripts.seed

Crea (o es idempotente sobre):
- Roles USER y ADMIN
- Un usuario administrador y un usuario normal (configurables por variables de entorno)
- Categorías y productos de ejemplo

IMPORTANTE: las credenciales generadas son SOLO para desarrollo.
"""

from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.db.base import Category, Product, Role, User  # importa y registra todos los modelos
from app.db.session import SessionLocal
from app.utils.slug import slugify

ROLE_NAMES = ["USER", "ADMIN"]

CATEGORIES = [
    {"name": "Smartphones", "description": "Teléfonos inteligentes de todas las marcas"},
    {"name": "Accesorios", "description": "Fundas, cargadores, audífonos y más"},
    {"name": "Reparación", "description": "Servicios de reparación de pantallas y baterías"},
]

PRODUCTS = [
    {
        "name": "iPhone 16 Pro Max",
        "brand": "Apple",
        "model": "A3101",
        "price": "28999.00",
        "stock": 15,
        "category": "Smartphones",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=iPhone+16&font=inter",
        "description": "El iPhone más potente. Chip A18 Pro, cámara de 48MP, batería para todo el día.",
    },
    {
        "name": "Samsung Galaxy S25 Ultra",
        "brand": "Samsung",
        "model": "SM-S938",
        "price": "25999.00",
        "stock": 20,
        "category": "Smartphones",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Galaxy+S25&font=inter",
        "description": "Potenciado por Galaxy AI. Cámara de 200MP, S Pen integrado.",
    },
    {
        "name": "Xiaomi 15 Pro",
        "brand": "Xiaomi",
        "model": "2410DPN6CC",
        "price": "15999.00",
        "stock": 25,
        "category": "Smartphones",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Xiaomi+15&font=inter",
        "description": "Cámara Leica, Snapdragon 8 Elite, carga ultrarrápida 120W.",
    },
    {
        "name": "Motorola Edge 50 Fusion",
        "brand": "Motorola",
        "model": "XT2503",
        "price": "7999.00",
        "stock": 30,
        "category": "Smartphones",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Edge+50&font=inter",
        "description": "Pantalla pOLED 144Hz, cámara de 50MP OIS, carga TurboPower 68W.",
    },
    {
        "name": "Honor Magic6 Pro",
        "brand": "Honor",
        "model": "BVL-AN00",
        "price": "18999.00",
        "stock": 12,
        "category": "Smartphones",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Magic6+Pro&font=inter",
        "description": "Cámara Falcon Camera AIS, Snapdragon 8 Gen 3, batería silicona-carbono.",
    },
    {
        "name": "Oppo Find X8 Pro",
        "brand": "Oppo",
        "model": "CPH2669",
        "price": "21999.00",
        "stock": 10,
        "category": "Smartphones",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Find+X8&font=inter",
        "description": "Cámara cuádruple Hasselblad, carga SUPERVOOC 80W.",
    },
    {
        "name": "Funda Silicona iPhone 16",
        "brand": "Spigen",
        "model": "ACC-FND-01",
        "price": "349.00",
        "stock": 100,
        "category": "Accesorios",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Funda&font=inter",
        "description": "Funda de silicona resistente con protección en las esquinas.",
    },
    {
        "name": "Cargador Rápido 65W USB-C",
        "brand": "Baseus",
        "model": "ACC-CRG-01",
        "price": "599.00",
        "stock": 80,
        "category": "Accesorios",
        "image": "https://placehold.co/400x400/111111/FFD60A?text=Cargador&font=inter",
        "description": "Cargador GaN de 65W compatible con la mayoría de smartphones.",
    },
]


def seed_roles(db) -> dict[str, Role]:
    roles = {}
    for name in ROLE_NAMES:
        role = db.scalar(select(Role).where(Role.name == name))
        if role is None:
            role = Role(name=name)
            db.add(role)
            db.flush()
        roles[name] = role
    return roles


def seed_user(db, roles, email: str, password: str, full_name: str, role_name: str) -> None:
    user = db.scalar(select(User).where(User.email == email))
    if user is None:
        db.add(
            User(
                email=email,
                full_name=full_name,
                password_hash=hash_password(password),
                role_id=roles[role_name].id,
                is_active=True,
            )
        )
        print(f"  Usuario creado: {email} ({role_name})")
    else:
        print(f"  Usuario ya existente: {email}")


def seed_categories(db) -> dict[str, Category]:
    categories = {}
    for data in CATEGORIES:
        category = db.scalar(select(Category).where(Category.slug == slugify(data["name"])))
        if category is None:
            category = Category(name=data["name"], slug=slugify(data["name"]), description=data["description"])
            db.add(category)
            db.flush()
            print(f"  Categoría creada: {data['name']}")
        categories[data["name"]] = category
    return categories


def seed_products(db, categories: dict[str, Category]) -> None:
    existing = set(db.scalars(select(Product.name)))
    for data in PRODUCTS:
        if data["name"] in existing:
            print(f"  Producto ya existente: {data['name']}")
            continue
        category = categories[data["category"]]
        db.add(
            Product(
                name=data["name"],
                brand=data["brand"],
                model=data["model"],
                price=data["price"],
                stock=data["stock"],
                image=data["image"],
                description=data["description"],
                category_id=category.id,
                is_active=True,
            )
        )
        print(f"  Producto creado: {data['name']}")


def main() -> None:
    print("Ejecutando seed de desarrollo...")
    with SessionLocal() as db:
        try:
            roles = seed_roles(db)
            seed_user(
                db,
                roles,
                settings.seed_admin_email,
                settings.seed_admin_password,
                "Administrador",
                "ADMIN",
            )
            seed_user(
                db,
                roles,
                settings.seed_user_email,
                settings.seed_user_password,
                "Usuario de Prueba",
                "USER",
            )
            categories = seed_categories(db)
            seed_products(db, categories)
            db.commit()
        except Exception:
            db.rollback()
            raise
    print("Seed completado.")


if __name__ == "__main__":
    main()
