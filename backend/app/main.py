from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.routers import auth, addresses, admin_stats, cart, categories, coupons, orders, payments, password_resets, products, reviews, users, wishlist

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description=(
        "Backend de la tienda de celulares Tienda Cell. "
        "Incluye autenticación JWT, productos, categorías, carrito, pedidos e inventario.\n\n"
        "Usa el botón **Authorize** para autenticarte y probar los endpoints protegidos."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = settings.api_prefix

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(addresses.router, prefix=API_PREFIX)
app.include_router(admin_stats.router, prefix=API_PREFIX)
app.include_router(categories.router, prefix=API_PREFIX)
app.include_router(products.router, prefix=API_PREFIX)
app.include_router(coupons.router, prefix=API_PREFIX)
app.include_router(cart.router, prefix=API_PREFIX)
app.include_router(orders.router, prefix=API_PREFIX)
app.include_router(payments.router, prefix=API_PREFIX)
app.include_router(password_resets.router, prefix=API_PREFIX)
app.include_router(reviews.router, prefix=API_PREFIX)
app.include_router(wishlist.router, prefix=API_PREFIX)


@app.get("/health", tags=["Salud"], summary="Healthcheck de la API")
def health() -> dict:
    return {"success": True, "message": "OK", "data": {"status": "running", "version": settings.project_version}}


@app.get("/", tags=["Salud"], include_in_schema=False)
def root() -> dict:
    return {"message": "Tienda Cell API - documentación en /docs", "docs": "/docs", "redoc": "/redoc"}
