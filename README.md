# Tienda Cell

Tienda Cell es un e-commerce de celulares desarrollado como un monorepo con un frontend en Vue 3 + Vite + TypeScript y un backend en FastAPI con PostgreSQL. El proyecto incluye una tienda pública, autenticación de usuarios, carrito de compras, gestión de pedidos y un panel de administración para administrar productos, categorías y órdenes.

## Características principales

- Catálogo de productos con secciones promocionales y contenido comercial.
- Registro e inicio de sesión de usuarios con autenticación JWT.
- Carrito de compras y flujo de pedidos.
- Panel de administración para gestionar:
  - productos
  - categorías
  - pedidos
- API REST documentada con Swagger / Redoc.
- Migraciones de base de datos con Alembic.
- Datos de ejemplo mediante seed para desarrollo.

## Stack tecnológico

### Frontend
- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- Tailwind-inspired styling y componentes reutilizables

### Backend
- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic v2
- JWT + bcrypt
- Pytest

## Estructura del proyecto

```text
.
├── backend/                 # API FastAPI y base de datos
│   ├── app/                 # Aplicación principal
│   │   ├── api/             # Routers y endpoints
│   │   ├── core/            # Configuración, seguridad y excepciones
│   │   ├── db/              # Conexión y modelos base
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── routers/         # Endpoints HTTP
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── services/        # Lógica de negocio
│   │   └── utils/           # Utilidades
│   ├── alembic/             # Migraciones
│   ├── scripts/             # Seed y scripts auxiliares
│   ├── tests/               # Pruebas del backend
│   ├── Dockerfile           # Imagen Docker del backend
│   ├── docker-compose.yml   # Servicios locales
│   └── pyproject.toml       # Dependencias y configuración Python
├── public/                  # Archivos estáticos
├── src/                     # Aplicación frontend Vue
│   ├── components/          # Componentes reutilizables
│   ├── pages/               # Vistas principales
│   ├── stores/              # Estado global con Pinia
│   ├── api/                 # Servicios de comunicación con backend
│   └── router/              # Configuración de rutas
├── package.json             # Scripts y dependencias del frontend
└── vite.config.ts          # Configuración de Vite
```

## Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- Node.js 20+ y npm
- Python 3.12+
- PostgreSQL (si vas a correr la base de datos localmente)
- Docker y Docker Compose (opcional, para ejecutar el backend en contenedores)

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd tienda-cell
```

### 2. Configurar el backend

```bash
cd backend
cp .env.example .env
```

Ajusta las variables de entorno en el archivo `.env` si es necesario. Por defecto se apunta a una base de datos PostgreSQL local en `localhost:5433`.

Instala las dependencias del backend con `uv`:

```bash
uv sync
```

Aplica las migraciones y carga los datos de ejemplo:

```bash
uv run alembic upgrade head
uv run python scripts/seed.py
```

Inicia el backend:

```bash
uv run uvicorn app.main:app --reload
```

La API estará disponible en:

- http://localhost:8000/docs
- http://localhost:8000/redoc

### 3. Configurar el frontend

En una nueva terminal:

```bash
cd ..
npm install
npm run dev
```

La aplicación frontend correrá en:

- http://localhost:5173

## Ejecución con Docker

También puedes levantar el backend y la base de datos con Docker Compose desde la carpeta `backend`:

```bash
cd backend
docker compose up --build
```

## Pruebas

### Backend

```bash
cd backend
uv run pytest
```

## Credenciales de desarrollo

El seed genera usuarios de prueba para desarrollo. Por defecto:

- Administrador: `admin@tiendacell.com` / `Admin123!`
- Usuario estándar: `usuario@tiendacell.com` / `Usuario123!`

Estas credenciales solo deben usarse en entornos de desarrollo.

## Variables de entorno importantes

En el archivo `.env` del backend puedes ajustar:

- `DATABASE_URL`: conexión a PostgreSQL
- `SECRET_KEY`: clave secreta para JWT
- `ACCESS_TOKEN_EXPIRE_MINUTES`: duración del token
- `CORS_ORIGINS`: orígenes permitidos por CORS
- `SEED_ADMIN_EMAIL`, `SEED_ADMIN_PASSWORD`, `SEED_USER_EMAIL`, `SEED_USER_PASSWORD`

## Notas adicionales

- El frontend está diseñado para consumir la API del backend en local mediante la configuración de CORS y la URL base del cliente API.
- Para trabajar con el panel de administración, inicia sesión con un usuario administrador o usa las credenciales de seed.
- Si necesitas cambiar la URL del backend en el frontend, revisa los archivos dentro de `src/api/`.
