import pytest

from tests.conftest import create_user_via_db
from tests.test_products import create_product


@pytest.fixture
def product_id(client, admin_token):
    return create_product(client, admin_token, price="1000.00", stock=10).json()["data"]["id"]


def add_to_cart(client, token, product_id, quantity=1):
    return client.post(
        "/api/cart/items",
        json={"product_id": product_id, "quantity": quantity},
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_order(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=2)
    response = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 201
    order = response.json()["data"]
    assert order["status"] == "PENDING"
    assert order["total"] == "2099.00"  # 2000 de productos + 99 de envío estándar
    assert order["shipping_cost"] == "99.00"
    assert len(order["items"]) == 1
    assert order["items"][0]["product_name"] == "Test Phone"
    assert order["items"][0]["quantity"] == 2


def test_order_deducts_stock(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=2)
    client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})

    product = client.get(f"/api/products/{product_id}").json()["data"]
    assert product["stock"] == 8


def test_order_clears_cart(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=2)
    client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    assert cart["item_count"] == 0


def test_order_with_empty_cart_rejected(client, user_token):
    response = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 400
    assert "vacio" in response.json()["message"].lower()


def test_order_requires_auth(client):
    assert client.post("/api/orders").status_code == 401


def test_insufficient_stock_rejected_and_no_partial_deduction(client, admin_token, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=5)
    client.patch(
        f"/api/products/{product_id}",
        json={"stock": 2},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["message"]

    product = client.get(f"/api/products/{product_id}").json()["data"]
    assert product["stock"] == 2

    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    assert cart["item_count"] == 5

    assert client.get("/api/orders", headers={"Authorization": f"Bearer {user_token}"}).json()["data"] == []


def test_order_cannot_manipulate_price(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=3)
    response = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    order = response.json()["data"]
    assert order["total"] == "3099.00"  # 3000 de productos + 99 de envío
    assert order["items"][0]["unit_price"] == "1000.00"


def test_order_uses_db_price_after_update(client, admin_token, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    client.patch(
        f"/api/products/{product_id}",
        json={"price": "2500.00"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    order = response.json()["data"]
    assert order["total"] == "2599.00"  # precio actualizado + envío
    assert order["items"][0]["unit_price"] == "2500.00"


def test_list_my_orders(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    add_to_cart(client, user_token, product_id, quantity=1)
    client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})

    response = client.get("/api/orders", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_my_order_detail(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    created = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]

    response = client.get(f"/api/orders/{created['id']}", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json()["data"]["id"] == created["id"]


def test_user_cannot_access_other_user_order(client, admin_token, user_token, product_id):
    create_user_via_db("other@test.com", "OtherPass123!", full_name="Otro")
    other_token = client.post(
        "/api/auth/login", data={"username": "other@test.com", "password": "OtherPass123!"}
    ).json()["data"]["access_token"]

    add_to_cart(client, other_token, product_id, quantity=1)
    other_order = client.post("/api/orders", headers={"Authorization": f"Bearer {other_token}"}).json()["data"]

    response = client.get(
        f"/api/orders/{other_order['id']}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404

    response = client.get(f"/api/orders/{other_order['id']}", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200


def test_admin_can_list_all_orders(client, admin_token, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"})

    response = client.get("/api/orders", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 1


def test_user_cannot_update_order_status(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    created = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]

    response = client.patch(
        f"/api/orders/{created['id']}/status",
        json={"status": "CANCELLED"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403


def test_admin_can_update_order_status(client, admin_token, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    created = client.post("/api/orders", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]

    response = client.patch(
        f"/api/orders/{created['id']}/status",
        json={"status": "CONFIRMED"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "CONFIRMED"
