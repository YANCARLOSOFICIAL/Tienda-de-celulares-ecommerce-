from tests.conftest import create_user_via_db


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "nuevo@test.com", "full_name": "Nuevo Usuario", "password": "Password123!"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["email"] == "nuevo@test.com"
    assert "password" not in body["data"]


def test_register_duplicate_email(client, user_token):
    response = client.post(
        "/api/auth/register",
        json={"email": "user@test.com", "full_name": "Otro", "password": "Password123!"},
    )
    assert response.status_code == 409
    assert response.json()["success"] is False


def test_register_short_password(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "corto@test.com", "full_name": "Corto", "password": "123"},
    )
    assert response.status_code == 422


def test_login_success(client):
    create_user_via_db("login@test.com", "LoginPass123!", full_name="Login User")
    response = client.post("/api/auth/login", data={"username": "login@test.com", "password": "LoginPass123!"})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["access_token"]
    assert body["data"]["token_type"] == "bearer"


def test_login_wrong_password(client):
    create_user_via_db("wrong@test.com", "Correcto123!", full_name="Wrong")
    response = client.post("/api/auth/login", data={"username": "wrong@test.com", "password": "Incorrecta!"})
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_login_unknown_user(client):
    response = client.post("/api/auth/login", data={"username": "nadie@test.com", "password": "Whatever123!"})
    assert response.status_code == 401


def test_get_me(client, user_token):
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["email"] == "user@test.com"
    assert body["data"]["role"]["name"] == "USER"
    assert "password" not in body["data"]


def test_get_me_without_token(client):
    response = client.get("/api/users/me")
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_get_me_with_invalid_token(client):
    response = client.get("/api/users/me", headers={"Authorization": "Bearer token-invalido"})
    assert response.status_code == 401


def test_update_profile(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = client.patch("/api/users/me", json={"full_name": "Nombre Actualizado"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["full_name"] == "Nombre Actualizado"

    response = client.patch("/api/users/me", json={"password": "NuevaPass123!"}, headers=headers)
    assert response.status_code == 200

    login = client.post("/api/auth/login", data={"username": "user@test.com", "password": "NuevaPass123!"})
    assert login.status_code == 200
