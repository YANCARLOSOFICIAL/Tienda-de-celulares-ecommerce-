import pytest

from tests.test_products import create_product


@pytest.fixture
def product_id(client, admin_token):
    created = create_product(client, admin_token, stock=10).json()["data"]
    return created["id"]


def add_to_cart(client, token, product_id, quantity=1):
    return client.post(
        "/api/cart/items",
        json={"product_id": product_id, "quantity": quantity},
        headers={"Authorization": f"Bearer {token}"},
    )


def test_cart_requires_auth(client):
    assert client.get("/api/cart").status_code == 401
    assert client.post("/api/cart/items", json={"product_id": 1, "quantity": 1}).status_code == 401


def test_add_item_to_cart(client, user_token, product_id):
    response = add_to_cart(client, user_token, product_id, quantity=2)
    assert response.status_code == 201
    body = response.json()
    assert body["data"]["product_id"] == product_id
    assert body["data"]["quantity"] == 2
    assert body["data"]["subtotal"] == "19999.98"


def test_cart_total_is_computed_server_side(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=2)
    add_to_cart(client, user_token, product_id, quantity=3)

    response = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"})
    cart = response.json()["data"]
    assert cart["item_count"] == 5
    assert cart["items"][0]["quantity"] == 5
    assert cart["total"] == "49999.95"


def test_add_item_accumulates_quantity(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    add_to_cart(client, user_token, product_id, quantity=2)
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    assert cart["items"][0]["quantity"] == 3


def test_add_nonexistent_product(client, user_token):
    response = add_to_cart(client, user_token, product_id=99999)
    assert response.status_code == 404


def test_add_quantity_zero_rejected(client, user_token, product_id):
    response = client.post(
        "/api/cart/items",
        json={"product_id": product_id, "quantity": 0},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 422


def test_add_quantity_above_stock_rejected(client, user_token, product_id):
    response = add_to_cart(client, user_token, product_id, quantity=11)
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["message"]


def test_add_inactive_product_rejected(client, admin_token, user_token):
    created = create_product(client, admin_token, stock=5).json()["data"]
    client.patch(
        f"/api/products/{created['id']}",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = add_to_cart(client, user_token, created["id"])
    assert response.status_code == 404


def test_update_quantity(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    item_id = cart["items"][0]["id"]

    response = client.patch(
        f"/api/cart/items/{item_id}",
        json={"quantity": 4},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["quantity"] == 4


def test_update_quantity_above_stock_rejected(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    item_id = cart["items"][0]["id"]

    response = client.patch(
        f"/api/cart/items/{item_id}",
        json={"quantity": 999},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400


def test_remove_item(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    item_id = cart["items"][0]["id"]

    response = client.delete(
        f"/api/cart/items/{item_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    assert cart["item_count"] == 0


def test_remove_item_from_other_user_cart(client, user_token, admin_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    item_id = cart["items"][0]["id"]

    response = client.delete(
        f"/api/cart/items/{item_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404


def test_clear_cart(client, user_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=3)
    response = client.delete("/api/cart", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    cart = client.get("/api/cart", headers={"Authorization": f"Bearer {user_token}"}).json()["data"]
    assert cart["item_count"] == 0


def test_carts_are_isolated_per_user(client, user_token, admin_token, product_id):
    add_to_cart(client, user_token, product_id, quantity=1)
    admin_cart = client.get("/api/cart", headers={"Authorization": f"Bearer {admin_token}"}).json()["data"]
    assert admin_cart["item_count"] == 0
