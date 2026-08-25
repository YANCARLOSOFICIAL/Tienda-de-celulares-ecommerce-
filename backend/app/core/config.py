from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global de la aplicación, cargada desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Base de datos
    database_url: str = Field(
        default="postgresql+psycopg://tiendacell:tiendacell@localhost:5432/tiendacell",
        description="URL de conexión a PostgreSQL (SQLAlchemy).",
    )

    # Seguridad
    secret_key: str = Field(
        default="CHANGE-ME-in-production",
        description="Clave secreta para firmar tokens JWT. Nunca usar el valor por defecto en producción.",
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60 * 24, description="Minutos de validez del access token.")

    # CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"],
        description="Orígenes permitidos para CORS.",
    )

    # Seed (credenciales de desarrollo, jamás para producción)
    seed_admin_email: str = "admin@tiendacell.com"
    seed_admin_password: str = "Admin123!"
    seed_user_email: str = "usuario@tiendacell.com"
    seed_user_password: str = "Usuario123!"

    # API
    api_prefix: str = "/api"
    project_name: str = "Tienda Cell API"
    project_version: str = "1.0.0"

    # MercadoPago (opcional - si no se configura, se usa modo sandbox interno)
    mercadopago_access_token: str | None = Field(default=None, description="Access token de MercadoPago (opcional)")
    frontend_url: str = Field(default="http://localhost:5173", description="URL del frontend para back_urls")

    # Factus (facturación electrónica DIAN - opcional; si no se configura, la facturación queda deshabilitada)
    factus_base_url: str = Field(
        default="https://api-sandbox.factus.com.co",
        description="URL base de la API de Factus (sandbox o producción).",
    )
    factus_api_version: str = Field(
        default="v2",
        description="Versión de la API de Factus contratada por la empresa ('v1' o 'v2').",
    )
    factus_client_id: str | None = Field(default=None, description="Client ID OAuth de Factus.")
    factus_client_secret: str | None = Field(default=None, description="Client Secret OAuth de Factus.")
    factus_username: str | None = Field(default=None, description="Usuario (correo) de Factus.")
    factus_password: str | None = Field(default=None, description="Contraseña del usuario de Factus.")
    factus_numbering_range_id: int | None = Field(
        default=None,
        description="ID del rango de numeración activo. Si hay un solo rango, la API lo toma por defecto.",
    )
    factus_default_tax_rate: str = Field(
        default="19.00",
        description="Porcentaje de IVA por defecto aplicado a los productos al facturar.",
    )
    factus_timeout_seconds: float = Field(default=30.0, description="Timeout HTTP para llamadas a Factus.")

    @property
    def factus_configured(self) -> bool:
        return all(
            [self.factus_client_id, self.factus_client_secret, self.factus_username, self.factus_password]
        )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("["):
                return v
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def auth_url(self) -> str:
        return f"{self.api_prefix}/auth/login"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
