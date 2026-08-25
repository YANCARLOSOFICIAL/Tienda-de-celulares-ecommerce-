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

## Facturación electrónica con Factus

El backend se integra con [Factus](https://www.factus.com.co/) para emitir facturas electrónicas validadas ante la DIAN.

### Configuración

Copia las variables de `.env.example` y completa las credenciales que entrega Factus:

```env
FACTUS_BASE_URL=https://api-sandbox.factus.com.co   # sandbox para pruebas
FACTUS_CLIENT_ID=tu-client-id
FACTUS_CLIENT_SECRET=tu-client-secret
FACTUS_USERNAME=tu-correo
FACTUS_PASSWORD=tu-password
FACTUS_NUMBERING_RANGE_ID=          # opcional si tienes un solo rango activo
FACTUS_DEFAULT_TAX_RATE=19.00       # IVA por defecto de los productos
```

Si estas variables no están definidas, la facturación queda deshabilitada (error 503) y el resto de la tienda funciona normalmente.

### Cómo funciona

> **Versión de la API**: `FACTUS_API_VERSION` (por defecto `v2`). La V2 usa códigos DIAN (`identification_document_code`, `unit_measure_code`...), precios **sin IVA** y `payment_details`; la integración convierte automáticamente los precios con IVA de la tienda a base gravable y ajusta el total al que calcula Factus (con reintento automático si hay desajuste por centavos).

1. **Autenticación OAuth2**: el servicio solicita el token a `POST /oauth/token` (grant `password`) y lo renueva automáticamente con el grant `refresh_token` cuando expira (~1 hora).
2. **Emisión**: cada pedido se convierte al payload de `POST /v1/bills/validate`:
   - `reference_code` = `order-{id}` (idempotente: no se emiten facturas duplicadas).
   - El envío se agrega como línea exenta de IVA.
   - El cupón se reporta como descuento a nivel de factura (`allowance_charges`).
   - Los datos del adquiriente (identificación, tipo de documento, etc.) se envían por API al momento de facturar.
3. **Persistencia**: el resultado (CUFE, número, estado DIAN, respuesta cruda) se guarda en la tabla `invoices`.
4. **Descargas**: Factus devuelve PDF/XML en Base64 dentro del JSON; el backend los decodifica y sirve como archivos.

### Endpoints (`/api/invoices`)

| Método | Ruta | Permisos | Descripción |
| --- | --- | --- | --- |
| POST | `/orders/{order_id}` | Admin | Emite y valida la factura electrónica del pedido |
| GET | `/orders/{order_id}` | Dueño o Admin | Consulta la factura de un pedido |
| DELETE | `/orders/{order_id}` | Dueño o Admin | Elimina una factura NO validada por la DIAN |
| GET | `/{bill_number}/pdf` | Dueño o Admin | Descarga el PDF de la representación gráfica |
| GET | `/{bill_number}/xml` | Dueño o Admin | Descarga el XML UBL |
| GET | `/numbering-ranges` | Admin | Lista los rangos de numeración activos en Factus |

Ejemplo de emisión:

```bash
curl -X POST http://localhost:8000/api/invoices/orders/1 \
  -H "Authorization: Bearer <token-admin>" \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "identification": "1020304050",
      "names": "Juan Pérez",
      "email": "juan@example.com"
    }
  }'
```

> **Nota producción**: cambia `FACTUS_BASE_URL` a `https://api.factus.com.co`. Para anular una factura ya validada por la DIAN se debe emitir una nota crédito (aún no implementado).

### Integración en el frontend

- `src/api/invoices.ts`: cliente de facturas con descargas autenticadas de PDF/XML.
- `OrderDetailPage.vue`: el cliente ve el estado de su factura (CUFE, número DIAN) y descarga PDF/XML.
- `AdminOrders.vue`: el admin emite la factura desde el panel (formulario de datos del adquiriente) y consulta/descarga los documentos.

## Notas adicionales

- El frontend está diseñado para consumir la API del backend en local mediante la configuración de CORS y la URL base del cliente API.
- Para trabajar con el panel de administración, inicia sesión con un usuario administrador o usa las credenciales de seed.
- Si necesitas cambiar la URL del backend en el frontend, revisa los archivos dentro de `src/api/`.
