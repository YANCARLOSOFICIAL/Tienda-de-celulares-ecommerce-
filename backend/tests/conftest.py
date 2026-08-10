import os

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://tiendacell:tiendacell@localhost:5433/tiendacell_test",
)

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production-0123456789abcdef"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app

test_engine = create_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def seed_roles(db) -> None:
    from app.models.role import Role

    if db.query(Role).count() == 0:
        db.add_all([Role(name="USER"), Role(name="ADMIN")])
        db.commit()


@pytest.fixture(autouse=True)
def _setup_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        seed_roles(db)
    finally:
        db.close()
    yield


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def create_user_via_db(email: str, password: str, full_name: str = "Usuario", role: str = "USER"):
    """Crea un usuario directamente en la base de datos (sin pasar por la API)."""
    from app.models.role import Role
    from app.models.user import User

    db = TestingSessionLocal()
    try:
        role_obj = db.query(Role).filter(Role.name == role).first()
        user = User(
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            role_id=role_obj.id,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def register_and_login(client: TestClient, email: str, password: str):
    r = client.post(
        "/api/auth/register",
        json={"email": email, "full_name": "Usuario Prueba", "password": password},
    )
    assert r.status_code == 201, r.text
    r = client.post("/api/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["data"]["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def user_token(client):
    return register_and_login(client, "user@test.com", "Password123!")


@pytest.fixture
def admin_token(client):
    create_user_via_db("admin@test.com", "AdminPass123!", full_name="Admin", role="ADMIN")
    r = client.post("/api/auth/login", data={"username": "admin@test.com", "password": "AdminPass123!"})
    assert r.status_code == 200, r.text
    return r.json()["data"]["access_token"]
