# Integración de Factus — Facturación Electrónica DIAN

> Documento técnico-pedagógico: explica **paso a paso** cómo se integró la API de
> Factus (https://www.factus.com.co/) en Tienda Cell, qué problemas surgieron y cómo
> se resolvieron. Sirve como guía para futuras integraciones con APIs externas.

---

## 1. Contexto

**Factus** es un proveedor colombiano de facturación electrónica que actúa como
intermediario ante la **DIAN**: les envías los datos de la venta y ellos generan el
documento electrónico válido legalmente (con CUFE, número autorizado, QR, PDF y XML).

Lo que se integró:

| Capacidad | Endpoint Factus usado |
| --- | --- |
| Autenticación OAuth2 | `POST /oauth/token` |
| Crear y validar factura | `POST /v2/bills/validate` |
| Consultar factura por número | `GET /v2/bills/{number}` |
| Descargar PDF (Base64 en JSON) | `GET /v2/bills/{number}/download-pdf` |
| Descargar XML UBL (Base64) | `GET /v2/bills/{number}/download-xml` |
| Eliminar factura NO validada | `DELETE /v2/bills/destroy/reference/{ref}` |
| Rangos de numeración | `GET /v2/numbering-ranges` |

Docs oficiales: https://developers.factus.com.co (ojo: tienen **V1 y V2**, ver §9.3).

---

## 2. Arquitectura general

```
┌──────────────┐   /api/invoices    ┌─────────────────────┐   HTTPS/OAuth2   ┌──────────┐
│  Frontend    │ ─────────────────▶ │  Backend FastAPI     │ ───────────────▶ │  Factus  │
│  Vue 3       │ ◀───────────────── │  · services/factus   │ ◀─────────────── │  (DIAN)  │
└──────────────┘   JSON / PDF blob  │  · services/invoices │   JSON+Base64    └──────────┘
                                    │  · routers/invoices  │
                                    │  · models/invoice    │
                                    └──────────┬──────────┘
                                               ▼
                                          PostgreSQL
                                       (tabla invoices)
```

Decisiones clave:

1. **El backend es el único que habla con Factus.** Las credenciales nunca llegan al
   navegador; el frontend solo consume `/api/invoices/*`.
2. **Persistimos cada factura localmente** (tabla `invoices`) para idempotencia,
   auditoría y para no depender de Factus al mostrar el estado.
3. **Un pedido → una factura** (`reference_code = order-{id}`): la unicidad la
   garantiza tanto nuestra BD (columna `unique`) como Factus (`reference_code`).

---

## 3. Paso a paso de la implementación

### Paso 1 — Investigar la API antes de escribir código

Antes de programar se leyó la documentación oficial y se anotaron:
- URLs de sandbox vs producción (`api-sandbox.factus.com.co` / `api.factus.com.co`)
- El flujo OAuth2 exacto (grant type `password`, no client_credentials)
- La estructura del JSON de creación de factura (3 bloques: factura, cliente, ítems)
- Que las descargas de PDF/XML llegan **en Base64 dentro de un JSON**, no como binario

💡 *Lección*: media hora de leer docs ahorra horas de prueba y error.

### Paso 2 — Configuración (`app/core/config.py` + `.env`)

Se añadieron settings tipados con pydantic-settings:

```python
factus_base_url: str = "https://api-sandbox.factus.com.co"
factus_api_version: str = "v2"
factus_client_id: str | None = None
factus_client_secret: str | None = None
factus_username: str | None = None
factus_password: str | None = None
factus_numbering_range_id: int | None = None   # opcional
factus_default_tax_rate: str = "19.00"

@property
def factus_configured(self) -> bool: ...
```

Patrón importante: **la integración es opcional**. Si faltan credenciales,
`settings.factus_configured` es False y el servicio responde 503 sin romper el resto
de la tienda.

### Paso 3 — Modelo de datos + migración

Nueva tabla `invoices` (modelo `app/models/invoice.py`, migración Alembic):

```
invoices
├── order_id        FK única a orders (1 pedido → 1 factura)
├── reference_code  "order-{id}", unique
├── bill_number     SETP990016470, unique, nullable
├── cufe            identificador DIAN del documento
├── status          PENDING | VALIDATED | FAILED
├── total           total según Factus (puede diferir por centavos)
├── factus_response JSON crudo de respuesta (auditoría/debug)
└── error_message   último error si FAILED
```

Comandos usados:

```bash
# crear migración vacía y editarla a mano (proyecto usa migraciones manuales)
alembic revision -m "invoices table"
# aplicar
alembic upgrade head
```

⚠️ *Tropezón*: al crear la revisión apunté `down_revision` a una revisión vieja y
quedaron **dos cabezas (branches)**. Alembic lo detecta: `Multiple head revisions`.
Solución: encadenar tras la última real (`down_revision = "a6b7c8d9e0f1"`).

### Paso 4 — Cliente HTTP puro (`app/services/factus.py`)

Separación de responsabilidades: este archivo **solo sabe hablar HTTP con Factus**,
no conoce pedidos ni base de datos.

#### 4a. Tokens OAuth con caché automática

```python
_lock = threading.Lock()
_access_token: str | None = None
_refresh_token: str | None = None
_token_expires_at: float = 0.0     # time.monotonic()

def get_access_token() -> str:
    with _lock:
        if _access_token and time.monotonic() < _token_expires_at:
            return _access_token                    # 1) caché vigente
        if _refresh_token:
            try:
                return _store_tokens(_request_token("refresh_token", {...}))
            except AppException:
                pass                                # 2) refresh falló → password
        return _store_tokens(_request_token("password", {...}))
```

Detalles finos:
- Se descuenta un **margen de seguridad de 60s** a `expires_in`.
- Si Factus devuelve 401 en cualquier llamada, se fuerza refresco y **se reintenta
  una vez** (patrón `_send(..., retry_on_auth=True)`).
- `time.monotonic()` (no `time.time()`) para no sufrir si el reloj del SO se ajusta.

#### 4b. Normalización de errores

Toda respuesta >= 400 se convierte en `AppException(502/504, message, errors=[detalle])`
extrayendo `message`/`errors` del JSON de Factus. Así el frontend siempre recibe el
formato estándar `{success, message, errors}`.

#### 4c. Descargas Base64

```python
data = response.json()["data"]
bytes_pdf = base64.b64decode(data["pdf_base_64_encoded"])
return data["file_name"], bytes_pdf
```

### Paso 5 — Lógica de negocio (`app/services/invoices.py`)

Aquí ocurre la traducción **Pedido de la tienda → Documento DIAN**.

#### 5a. Conversión de precios (lo más delicado)

La tienda guarda precios **con IVA incluido** ($10.999). La API V2 espera el precio
**sin IVA** (base gravable). Conversión:

```python
base = round(precio_con_iva / (1 + tasa_iva), 2)      # 10999/1.19 → 8242.86
```

⚠️ Redondear la base introduce desajustes de centavos contra el total del pedido.
Ver §9.4 para cómo se resolvió.

#### 5b. Mapeo completo del payload V2

```jsonc
{
  "document": "01",                          // FE de venta
  "reference_code": "order-5",               // idempotencia
  "customer": {
    "identification_document_code": "13",    // 13=CC, 31=NIT (¡códigos, no IDs!)
    "identification": "1020304050",
    "legal_organization_code": "2",          // 2=Natural, 1=Jurídica
    "tribute_code": "ZZ",                    // ZZ=No aplica
    "names": "...", "email": "...", "address": "...",
    "municipality_code": "88001"             // código DANE
  },
  "items": [{
    "code_reference": "PROD-7",
    "name": "iPhone ...",
    "quantity": "2.00",
    "discount_rate": "0.00",                 // cupón repartido % por ítem
    "price": "8242.86",                      // SIN IVA
    "unit_measure_code": "94",               // unidad
    "standard_code": "999",                  // estándar del contribuyente
    "taxes": [{ "code": "01", "rate": "19.00" }]
  }],
  // el envío va como línea extra exenta:
  // { code_reference: "ENVIO", taxes: [{code:"01", rate:"0.00"}] }
  "payment_details": [{
    "payment_form": "1",                     // 1=contado
    "payment_method_code": "10",             // 10=efectivo
    "amount": "22097.99"                     // ¡obligatorio e igual al total!
  }]
}
```

#### 5c. Estimación del total + auto-reintento

Factus calcula el total así (verificado empíricamente, §9.4):

```
total = Σ( price × qty × (1 - discount%) × (1 + iva%) ) + envío
```

El backend replica esa fórmula con `Decimal` para enviar `amount` correcto, y además,
si Factus rechaza con `Esperado: 45,600.00 - Enviado: ...`, extrae ese valor con regex
y **reintenta una sola vez** con el monto corregido:

```python
_EXPECTED_TOTAL_RE = re.compile(r"Esperado:\s*([\d.,]+)")

try:
    response = factus.validate_bill(payload)
except AppException as exc:
    expected = _parse_expected_total(list(exc.errors))   # coma=miles, punto=decimal
    if expected is None:
        raise
    payload["payment_details"][0]["amount"] = f"{expected:.2f}"
    response = factus.validate_bill(payload)
```

#### 5d. Idempotencia y recuperación de fallos

```
POST /invoices/orders/{id}:
  ¿ya existe factura PENDING/VALIDATED? → devolverla (no duplicar)
  ¿existe FAILED? → DELETE destroy/reference/{ref} (best-effort) → reintentar
  ¿respuesta ok?  → guardar número, CUFE, estado, JSON crudo
  ¿error?         → marcar FAILED con mensaje y relanzar
```

### Paso 6 — Schemas y router (`app/schemas/invoice.py`, `app/routers/invoices.py`)

Endpoints expuestos (todos responden el envelope `{success, message, data}`):

| Método | Ruta | Quién |
| --- | --- | --- |
| POST | `/api/invoices/orders/{order_id}` | Admin |
| GET | `/api/invoices/orders/{order_id}` | Dueño o Admin |
| DELETE | `/api/invoices/orders/{order_id}` | Dueño o Admin |
| GET | `/api/invoices/{bill_number}/pdf` | Dueño o Admin |
| GET | `/api/invoices/{bill_number}/xml` | Dueño o Admin |
| GET | `/api/invoices/numbering-ranges` | Admin |

Extras:
- Los schemas validan códigos DIAN con `pattern` (`"13"`, `"ZZ"`, DANE de 5 dígitos).
- PDF/XML se sirven con `StreamingResponse` + header `Content-Disposition`.
- Además, `OrderOut`/`OrderDetailOut` incluyen un resumen
  `invoice: {bill_number, status}` (relación `lazy="selectin"` para evitar N+1),
  para que el frontend pinte el badge sin pedir nada más.

### Paso 7 — Frontend (Vue 3)

1. **`src/api/client.ts`**: se añadió `Api.download(path)` → `fetch` con Bearer token
   que devuelve `Blob` + filename del header `Content-Disposition`.
2. **`src/api/invoices.ts`**: tipos + `invoicesApi` (create/get/remove/downloadPdf/downloadXml);
   la descarga dispara el archivo en el navegador creando un `<a download>` temporal.
3. **`OrderDetailPage.vue`**: tarjeta "Factura electrónica" (estado DIAN, número, CUFE
   truncado, botones PDF/XML). Se consulta con try/catch silencioso: si no hay
   factura, simplemente no se muestra la tarjeta.
4. **`AdminOrders.vue`**: al expandir un pedido se carga su factura (lazy, caché en
   `invoicesByOrder`), formulario de emisión con datos del adquiriente y banner de
   resultado.
5. **`OrdersPage.vue`**: badge + botón "Descargar PDF" por tarjeta usando el resumen
   `order.invoice` que ya viene en la respuesta de pedidos.

### Paso 8 — Pruebas sin depender de Factus (`tests/test_factus.py`)

Se simula la API completa con `httpx.MockTransport`: un handler que responde
token, validate, show, downloads y destroy según la ruta. Ventajas:
- Suite rápida y determinística, sin gastar facturas reales del sandbox.
- Se pueden probar casos raros (401 → retry, expiración de token).

```python
client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://mock.factus.test")
factus.set_http_client(client)   # inyección: el servicio usa el cliente que le demos
```

14 pruebas cubren: caché de token, refresh grant, decodificación Base64,
estructura del payload (precios base, descuento cupón, envío exento, total estimado),
flujo end-to-end vía TestClient, permisos e idempotencia.

---

## 4. Operación

### Levantar todo (Docker)

```bash
cd backend
docker compose up -d --build     # db (5434) + api (8001), aplica migraciones y seed
cd .. && npm run dev             # frontend 5173 (proxy /api → localhost:8001)
```

### Variables `.env` (backend)

```env
FACTUS_BASE_URL=https://api-sandbox.factus.com.co   # producción: https://api.factus.com.co
FACTUS_API_VERSION=v2
FACTUS_CLIENT_ID=... FACTUS_CLIENT_SECRET=...
FACTUS_USERNAME=... FACTUS_PASSWORD=...
```

### Flujo de usuario final

```
Cliente compra → pedido PENDING
Admin: Panel → Pedidos → expandir → "Emitir factura electrónica"
       → llena identificación (CC/NIT) y contacto → Emitir
Backend: arma payload V2 → Factus valida ante DIAN → guarda invoice
Cliente: Mis pedidos → ve número de factura + descarga PDF/XML
```

---

## 5. Problemas encontrados y cómo se resolvieron (lo más valioso)

| # | Síntoma | Causa raíz | Solución |
|---|---------|-----------|----------|
| 1 | `502 Bad Gateway` en `/api/*` desde el frontend | El proxy de Vite apunta a `localhost:8001` pero el contenedor `tiendacell_api` no estaba levantado | `docker compose up -d --build`. Regla: **el proxy dice dónde debería estar el backend; verifica que exista** |
| 2 | Seed fallaba en Docker: `No module named 'app'` | `python scripts/seed.py` pone `scripts/` en sys.path, no el proyecto | `ENV PYTHONPATH=/app` en el Dockerfile |
| 3 | Uvicorn caía: `'WishlistItem' failed to locate a name` | `app/db/base.py` no importaba todos los modelos; SQLAlchemy resuelve strings de `relationship()` contra el registro global | Importar TODOS los modelos en `db/base.py`. En FastAPI funciona "de casualidad" porque los routers importan servicios; un script suelto lo destapa |
| 4 | `POST /orders` devolvía 422 | FastAPI exigía body aunque todos los campos tenían default | `payload: OrderCreate \| None = None` en el router |
| 5 | **`403 "Version de API no disponible para esta empresa"`** | La cuenta estaba habilitada solo para la **API V2** y el código usaba V1 | Migración completa a V2 + setting `FACTUS_API_VERSION`. Diagnóstico: llamar directo con httpx leyendo el cuerpo del error |
| 6 | `422 ... payment_details.0.amount obligatorio` | V2 exige array `payment_details` con `amount` igual al total calculado por Factus | Réplica de la fórmula de totales + reintento con "Esperado: X" |
| 7 | Totales desfasaban centavos vs el pedido | Convertir precio-con-IVA→base redondeando a 2 decimales pierde precisión | Aceptado y documentado: `invoice.total` guarda lo que Factus realmente calculó (práctica normal en facturadores); el auto-reinteno garantiza que la factura siempre se acepte |
| 8 | Dos cabezas en Alembic | Nueva migración apuntando a una revisión antigua | Encadenar `down_revision` a la cabeza real |

### Lecciones para futuras integraciones con APIs externas

1. **Lee primero, codifica después**, y verifica la VERSIÓN de la API de tu cuenta
   (V1/V2 cambiaron payloads completos).
2. **Aisla el cliente HTTP** en un módulo sin lógica de negocio: testeable con MockTransport.
3. **Tokens en caché con margen de seguridad + reintento ante 401** es patrón obligatorio.
4. **Idempotencia por referencia externa** (`reference_code`) te salva de duplicados.
5. **Persiste la respuesta cruda** (`factus_response` JSON): oro para debug y soporte.
6. **Los errores de validación de terceros son datos**: el truco de parsear
   `"Esperado: X"` convirtió un error en autocorrección.
7. **Prueba contra el sandbox real con un script mínimo** antes de integrar: revela
   formatos exactos que la doc omite (descubrimos que price va sin IVA así).
8. **Integraciones opcionales**: si falta configuración, la app sigue funcionando.

---

## 6. Pendientes / mejoras futuras

- [ ] Notas crédito (anular facturas ya validadas por la DIAN)
- [ ] Webhook/encuesta de estado si Factus notifica cambios post-validación
- [ ] Reintentos con backoff para errores transitorios de red (hoy: 1 reintento solo por 401)
- [ ] Panel admin para rangos de numeración ya existe vía API; podría tener UI dedicada
- [ ] `uv lock` pendiente de ejecutar (httpx agregado a dependencias)

---

*Documento generado agosto 2026. Código relevante: `backend/app/services/factus.py`,
`backend/app/services/invoices.py`, `backend/app/routers/invoices.py`,
`src/api/invoices.ts`, `tests/test_factus.py`.*
