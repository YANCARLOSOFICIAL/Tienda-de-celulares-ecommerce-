def create_product(client, token, **overrides):
    payload = {
        "name": "Test Phone",
        "description": "Descripción de prueba",
        "price": "9999.99",
        "stock": 10,
        "brand": "TestBrand",
        "model": "T-1000",
        "is_active": True,
    }
    payload.update(overrides)
    return client.post(
        "/api/products",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )


def test_admin_creates_product(client, admin_token):
    response = create_product(client, admin_token)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Test Phone"
    assert body["data"]["price"] == "9999.99"
    assert body["data"]["stock"] == 10


def test_user_cannot_create_product(client, user_token):
    response = create_product(client, user_token)
    assert response.status_code == 403
    assert response.json()["success"] is False


def test_unauthenticated_cannot_create_product(client):
    response = client.post(
        "/api/products",
        json={"name": "X", "price": "1.00", "stock": 1, "brand": "B"},
    )
    assert response.status_code == 401


def test_list_products(client, admin_token):
    create_product(client, admin_token, name="Alpha Phone", price="1000.00", brand="BrandA")
    create_product(client, admin_token, name="Beta Phone", price="2000.00", brand="BrandB")

    response = client.get("/api/products")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["total"] == 2
    assert body["data"]["page"] == 1
    assert len(body["data"]["items"]) == 2


def test_list_products_pagination(client, admin_token):
    for i in range(5):
        create_product(client, admin_token, name=f"Phone {i}", price=f"{100 + i}.00")

    response = client.get("/api/products", params={"page": 2, "page_size": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["total"] == 5
    assert body["data"]["page"] == 2
    assert body["data"]["pages"] == 3
    assert len(body["data"]["items"]) == 2


def test_search_products(client, admin_token):
    create_product(client, admin_token, name="iPhone 16 Pro", brand="Apple")
    create_product(client, admin_token, name="Galaxy S25", brand="Samsung")

    response = client.get("/api/products", params={"search": "iPhone"})
    assert response.status_code == 200
    assert response.json()["data"]["total"] == 1
    assert response.json()["data"]["items"][0]["name"] == "iPhone 16 Pro"


def test_filter_products_by_price_and_sort(client, admin_token):
    create_product(client, admin_token, name="Barato", price="500.00")
    create_product(client, admin_token, name="Caro", price="5000.00")

    response = client.get("/api/products", params={"min_price": "1000", "max_price": "6000", "ordering": "price"})
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert [i["name"] for i in items] == ["Caro"]

    response = client.get("/api/products", params={"ordering": "-price"})
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert items[0]["name"] == "Caro"


def test_get_product_by_id(client, admin_token):
    created = create_product(client, admin_token).json()["data"]
    response = client.get(f"/api/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == created["id"]


def test_get_nonexistent_product(client):
    response = client.get("/api/products/999999")
    assert response.status_code == 404


def test_update_product_admin_only(client, admin_token, user_token):
    created = create_product(client, admin_token).json()["data"]

    response = client.patch(
        f"/api/products/{created['id']}",
        json={"price": "7777.00", "stock": 5},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403

    response = client.patch(
        f"/api/products/{created['id']}",
        json={"price": "7777.00", "stock": 5},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["price"] == "7777.00"
    assert response.json()["data"]["stock"] == 5


def test_delete_product_admin_only(client, admin_token, user_token):
    created = create_product(client, admin_token).json()["data"]

    response = client.delete(
        f"/api/products/{created['id']}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

    response = client.delete(
        f"/api/products/{created['id']}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    response = client.get(f"/api/products/{created['id']}")
    assert response.status_code == 404


def test_inactive_products_hidden_from_public(client, admin_token):
    created = create_product(client, admin_token, is_active=True).json()["data"]
    client.patch(
        f"/api/products/{created['id']}",
        json={"is_active": False},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    response = client.get("/api/products")
    assert all(item["id"] != created["id"] for item in response.json()["data"]["items"])

    response = client.get(f"/api/products/{created['id']}")
    assert response.status_code == 404

    response = client.get("/api/products", headers={"Authorization": f"Bearer {admin_token}"})
    assert any(item["id"] == created["id"] for item in response.json()["data"]["items"])
