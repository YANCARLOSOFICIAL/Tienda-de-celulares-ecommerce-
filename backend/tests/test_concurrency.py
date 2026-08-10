"""Prueba de condición de carrera en el checkout.

Dos usuarios intentan comprar simultáneamente más unidades de las disponibles.
El bloqueo SELECT ... FOR UPDATE debe garantizar que:
- Solo un pedido se crea correctamente.
- El otro falla con error de stock.
- El stock final nunca es negativo.
"""

import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from tests.conftest import register_and_login
from tests.test_products import create_product


@pytest.fixture
def low_stock_product(client, admin_token):
    return create_product(client, admin_token, price="500.00", stock=5).json()["data"]["id"]


def _checkout(token: str) -> int:
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        r = c.post("/api/orders", headers={"Authorization": f"Bearer {token}"})
        return r.status_code


def test_concurrent_checkout_never_negative_stock(client, low_stock_product):
    token_a = register_and_login(client, "race-a@test.com", "Password123!")
    token_b = register_and_login(client, "race-b@test.com", "Password123!")

    client.post(
        "/api/cart/items",
        json={"product_id": low_stock_product, "quantity": 3},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    client.post(
        "/api/cart/items",
        json={"product_id": low_stock_product, "quantity": 3},
        headers={"Authorization": f"Bearer {token_b}"},
    )

    with ThreadPoolExecutor(max_workers=2) as pool:
        future_a = pool.submit(_checkout, token_a)
        future_b = pool.submit(_checkout, token_b)
        results = sorted([future_a.result(), future_b.result()])

    assert results == [201, 400], f"Se esperaba un éxito y un fallo, se obtuvo: {results}"

    product = client.get(f"/api/products/{low_stock_product}").json()["data"]
    assert product["stock"] == 2
    assert product["stock"] >= 0
