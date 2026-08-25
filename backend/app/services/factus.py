"""Cliente HTTP para la API de Factus (facturación electrónica DIAN).

Documentación: https://developers.factus.com.co/

Flujo de autenticación OAuth2:
- POST /oauth/token con grant_type=password devuelve access_token + refresh_token.
- El token caduca (aprox. 1 hora); se refresca automáticamente con grant_type=refresh_token.
- Todas las peticiones requieren el encabezado Authorization: Bearer <access_token>.
"""

from __future__ import annotations

import base64
import threading
import time
from typing import Any

import httpx

from app.core.config import settings
from app.core.exceptions import AppException

_TOKEN_SAFETY_MARGIN_SECONDS = 60

_lock = threading.Lock()
_access_token: str | None = None
_refresh_token: str | None = None
_token_expires_at: float = 0.0

_http_client: httpx.Client | None = None


def _get_http_client() -> httpx.Client:
    """Cliente HTTP compartido; se puede reemplazar en pruebas vía set_http_client()."""
    global _http_client
    if _http_client is None:
        _http_client = httpx.Client(
            base_url=settings.factus_base_url,
            timeout=settings.factus_timeout_seconds,
        )
    return _http_client


def set_http_client(client: httpx.Client | None) -> None:
    """Inyecta un cliente HTTP (para pruebas) o None para restaurar el de por defecto."""
    global _http_client, _access_token, _refresh_token, _token_expires_at
    with _lock:
        _http_client = client
        _access_token = None
        _refresh_token = None
        _token_expires_at = 0.0


def reset_token_cache() -> None:
    """Olvida los tokens en caché (útil en pruebas o tras cambiar credenciales)."""
    global _access_token, _refresh_token, _token_expires_at
    with _lock:
        _access_token = None
        _refresh_token = None
        _token_expires_at = 0.0


def _require_configuration() -> None:
    if not settings.factus_configured:
        raise AppException(
            status_code=503,
            message=(
                "Factus no está configurado. Define FACTUS_CLIENT_ID, FACTUS_CLIENT_SECRET, "
                "FACTUS_USERNAME y FACTUS_PASSWORD en las variables de entorno."
            ),
        )


def _request_token(grant_type: str, extra_params: dict[str, str]) -> dict[str, Any]:
    """Solicita un token a POST /oauth/token enviando form-data."""
    data = {
        "grant_type": grant_type,
        "client_id": settings.factus_client_id,
        "client_secret": settings.factus_client_secret,
        **extra_params,
    }
    try:
        response = _get_http_client().post(
            "/oauth/token", data=data, headers={"Accept": "application/json"}
        )
    except httpx.HTTPError as exc:
        raise AppException(status_code=502, message=f"No se pudo conectar con Factus: {exc}") from exc

    if response.status_code != 200:
        detail = _extract_error_detail(response)
        raise AppException(
            status_code=502,
            message="Factus rechazó la autenticación",
            errors=[detail],
        )
    payload = response.json()
    if not payload.get("access_token"):
        raise AppException(status_code=502, message="Factus no devolvió un access_token válido")
    return payload


def _store_tokens(payload: dict[str, Any]) -> str:
    global _access_token, _refresh_token, _token_expires_at
    expires_in = int(payload.get("expires_in") or 3600)
    _access_token = payload["access_token"]
    if payload.get("refresh_token"):
        _refresh_token = payload["refresh_token"]
    _token_expires_at = time.monotonic() + max(expires_in - _TOKEN_SAFETY_MARGIN_SECONDS, 30)
    return _access_token


def get_access_token() -> str:
    """Devuelve un token vigente; lo renueva (password o refresh grant) cuando expira.

    La llamada HTTP ocurre dentro del lock para que múltiples hilos no pidan
    tokens simultáneamente; el coste es despreciable frente a la frecuencia de expiración.
    """
    _require_configuration()
    with _lock:
        if _access_token and time.monotonic() < _token_expires_at:
            return _access_token

        if _refresh_token:
            try:
                return _store_tokens(
                    _request_token("refresh_token", {"refresh_token": _refresh_token})
                )
            except AppException:
                pass  # refresh inválido o expirado: se intenta con credenciales completas

        return _store_tokens(
            _request_token(
                "password",
                {"username": settings.factus_username or "", "password": settings.factus_password or ""},
            )
        )


def force_refresh_token() -> None:
    """Invalida el token actual para forzar una renovación en la siguiente petición."""
    global _token_expires_at
    with _lock:
        _token_expires_at = 0.0


def _extract_error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return f"HTTP {response.status_code}: {response.text[:500]}"
    parts: list[str] = []
    for key in ("message", "error"):
        value = body.get(key)
        if isinstance(value, str) and value:
            parts.append(value)
    errors = body.get("errors")
    if isinstance(errors, list):
        parts.extend(str(e) for e in errors)
    elif isinstance(errors, dict):
        for field, msgs in errors.items():
            joined = ", ".join(str(m) for m in msgs) if isinstance(msgs, list) else str(msgs)
            parts.append(f"{field}: {joined}")
    detail = " | ".join(parts)
    return detail or f"HTTP {response.status_code}"


def _send(method: str, path: str, *, json_body: Any = None, retry_on_auth: bool = True) -> httpx.Response:
    """Ejecuta una petición autenticada; reintenta una vez si el token quedó inválido (401)."""
    headers = {"Authorization": f"Bearer {get_access_token()}", "Accept": "application/json"}
    if json_body is not None:
        headers["Content-Type"] = "application/json"
    try:
        response = _get_http_client().request(method, path, json=json_body, headers=headers)
    except httpx.HTTPError as exc:
        raise AppException(status_code=502, message=f"No se pudo conectar con Factus: {exc}") from exc

    if response.status_code == 401 and retry_on_auth:
        force_refresh_token()
        return _send(method, path, json_body=json_body, retry_on_auth=False)

    if response.status_code >= 400:
        raise AppException(
            status_code=502 if response.status_code < 500 else 504,
            message=f"Factus devolvió un error ({response.status_code})",
            errors=[_extract_error_detail(response)],
        )
    return response


# ---------------------------------------------------------------------------
# Endpoints de facturas (/{version}/bills)
# ---------------------------------------------------------------------------

def _api(path: str) -> str:
    """Prefija la ruta con la versión de API contratada (ej. /v2/bills/...)."""
    return f"/{settings.factus_api_version}{path}"


def validate_bill(payload: dict[str, Any]) -> dict[str, Any]:
    """Crea y valida una factura electrónica ante la DIAN (POST /bills/validate)."""
    response = _send("POST", _api("/bills/validate"), json_body=payload)
    return response.json()


def show_bill(bill_number: str) -> dict[str, Any]:
    """Consulta una factura por su número (GET /bills/{number})."""
    return _send("GET", _api(f"/bills/{bill_number}")).json()


def list_bills(page: int = 1, filters: dict[str, str] | None = None) -> dict[str, Any]:
    """Lista y filtra facturas (GET /bills?page=N&filter[...]=...)."""
    params = {"page": page}
    params.update({f"filter[{k}]": v for k, v in (filters or {}).items()})
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return _send("GET", _api(f"/bills?{query}")).json()


def destroy_bill(reference_code: str) -> dict[str, Any]:
    """Elimina una factura NO validada por la DIAN usando su reference_code."""
    path = _api(f"/bills/destroy/reference/{reference_code}")
    return _send("DELETE", path).json()


def download_pdf(bill_number: str) -> tuple[str, bytes]:
    """Descarga la representación PDF de la factura (llega Base64 dentro del JSON)."""
    data = _send("GET", _api(f"/bills/{bill_number}/download-pdf")).json().get("data", {})
    encoded = data.get("pdf_base_64_encoded")
    if not encoded:
        raise AppException(status_code=502, message="Factus no devolvió el contenido del PDF")
    return data.get("file_name") or f"{bill_number}.pdf", base64.b64decode(encoded)


def download_xml(bill_number: str) -> tuple[str, bytes]:
    """Descarga el XML UBL de la factura (llega Base64 dentro del JSON)."""
    data = _send("GET", _api(f"/bills/{bill_number}/download-xml")).json().get("data", {})
    encoded = data.get("xml_base_64_encoded")
    if not encoded:
        raise AppException(status_code=502, message="Factus no devolvió el contenido del XML")
    return data.get("file_name") or f"{bill_number}.xml", base64.b64decode(encoded)


# ---------------------------------------------------------------------------
# Catálogos de apoyo
# ---------------------------------------------------------------------------

def numbering_ranges(page: int = 1, only_active: bool = True) -> dict[str, Any]:
    """Lista los rangos de numeración disponibles (GET /numbering-ranges)."""
    params = [f"page={page}"]
    if only_active:
        params.append("filter[is_active]=1")
    query = "&".join(params)
    return _send("GET", _api(f"/numbering-ranges?{query}")).json()
