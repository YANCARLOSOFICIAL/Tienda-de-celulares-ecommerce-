# Tienda Cell - Backend

Backend REST API para la tienda de celulares **Tienda Cell**, construido con FastAPI,
PostgreSQL, SQLAlchemy 2.x, Alembic y JWT.

## Stack

- Python 3.12+
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy 2.x + Alembic
- Pydantic v2
- Autenticación JWT (OAuth2 Password Bearer)
- Hashing de contraseñas con bcrypt
- Pytest + HTTPX
- Docker + Docker Compose
- Gestión de dependencias con `uv`

## Estructura

```
backend/
├── app/
│   ├── main.py              # Aplicación FastAPI
│   ├── core/                # Config, seguridad, dependencias, errores
│   ├── db/                  # Sesión y registro de modelos
│   ├── models/              # Modelos SQLAlchemy (roles, users, products, ...)
│   ├── schemas/             # Schemas Pydantic de entrada/salida
│   ├── routers/             # Capa HTTP
│   ├── services/            # Lógica de negocio
│   └── utils/               # Utilidades (paginación, slugs)
├── alembic/                 # Migraciones
├── scripts/                 # Seed de desarrollo
├── tests/                   # Pruebas pytest
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Puesta en marcha (local)

```bash
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run python scripts/seed.py
uv run uvicorn app.main:app --reload
```

Documentación: http://localhost:8000/docs y http://localhost:8000/redoc

## Puesta en marcha (Docker Compose)

```bash
docker compose up --build
```

## Pruebas

```bash
uv run pytest
```

## Credenciales de desarrollo (solo para pruebas)

Generadas por el seed:

- **Admin:** admin@tiendacell.com / Admin123!
- **Usuario:** usuario@tiendacell.com / Usuario123!

Estas credenciales se sobreescriben mediante variables de entorno
(`SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD`, `SEED_USER_EMAIL`, `SEED_USER_PASSWORD`).
Nunca deben usarse en producción.
