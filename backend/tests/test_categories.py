def create_category(client, token, name="Smartphones"):
    return client.post(
        "/api/categories",
        json={"name": name, "description": "Descripción"},
        headers={"Authorization": f"Bearer {token}"},
    )


def test_admin_creates_category(client, admin_token):
    response = create_category(client, admin_token)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Smartphones"
    assert body["data"]["slug"] == "smartphones"


def test_user_cannot_create_category(client, user_token):
    response = create_category(client, user_token)
    assert response.status_code == 403


def test_duplicate_category_rejected(client, admin_token):
    create_category(client, admin_token, name="Smartphones")
    response = create_category(client, admin_token, name="Smartphones")
    assert response.status_code == 409


def test_list_categories(client, admin_token):
    create_category(client, admin_token, name="Smartphones")
    create_category(client, admin_token, name="Accesorios")

    response = client.get("/api/categories")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_category(client, admin_token):
    created = create_category(client, admin_token, name="Reparación").json()["data"]
    response = client.get(f"/api/categories/{created['id']}")
    assert response.status_code == 200
    assert response.json()["data"]["slug"] == "reparacion"


def test_update_category(client, admin_token):
    created = create_category(client, admin_token, name="Smartphones").json()["data"]
    response = client.patch(
        f"/api/categories/{created['id']}",
        json={"name": "Teléfonos"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Teléfonos"
    assert response.json()["data"]["slug"] == "telefonos"


def test_delete_category_without_products(client, admin_token):
    created = create_category(client, admin_token, name="Temporal").json()["data"]
    response = client.delete(
        f"/api/categories/{created['id']}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert client.get(f"/api/categories/{created['id']}").status_code == 404


def test_delete_category_with_products_rejected(client, admin_token):
    category = create_category(client, admin_token, name="ConProductos").json()["data"]
    client.post(
        "/api/products",
        json={
            "name": "Producto",
            "price": "100.00",
            "stock": 5,
            "brand": "Brand",
            "category_id": category["id"],
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = client.delete(
        f"/api/categories/{category['id']}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 409
