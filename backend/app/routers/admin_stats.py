from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import func, select

from app.core.dependencies import AdminUser, DbDep
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User
from app.schemas.admin_stats import AdminStats, AdminStatsApiResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminStatsApiResponse, summary="Metricas del dashboard admin")
def get_stats(db: DbDep, _admin: AdminUser) -> AdminStatsApiResponse:
    total_orders = db.scalar(select(func.count(Order.id))) or 0
    total_revenue = db.scalar(select(func.coalesce(func.sum(Order.total), 0))) or Decimal("0.00")
    total_products = db.scalar(select(func.count(Product.id))) or 0
    total_users = db.scalar(select(func.count(User.id))) or 0

    orders_by_status: dict[str, int] = {}
    for status in OrderStatus:
        count = db.scalar(select(func.count(Order.id)).where(Order.status == status)) or 0
        orders_by_status[status.value] = count

    recent_stmt = select(Order).order_by(Order.created_at.desc()).limit(5)
    recent_orders = []
    for o in db.scalars(recent_stmt):
        recent_orders.append({
            "id": o.id,
            "status": o.status.value,
            "total": str(o.total),
            "created_at": o.created_at.isoformat() if o.created_at else "",
        })

    top_stmt = (
        select(
            OrderItem.product_name,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.subtotal).label("total_revenue"),
        )
        .group_by(OrderItem.product_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
    )
    top_products = []
    for row in db.scalars(top_stmt):
        pass

    top_stmt_rows = db.execute(top_stmt).fetchall()
    for row in top_stmt_rows:
        top_products.append({
            "name": row[0],
            "total_sold": int(row[1]),
            "total_revenue": str(row[2]),
        })

    return AdminStatsApiResponse(
        success=True,
        message="Estadisticas obtenidas correctamente",
        data=AdminStats(
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_products=total_products,
            total_users=total_users,
            orders_by_status=orders_by_status,
            recent_orders=recent_orders,
            top_products=top_products,
        ),
    )
