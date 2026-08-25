from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

from app.schemas.common import ApiResponse, ORMModel


class CustomerData(BaseModel):
    """Datos del adquiriente (cliente) exigidos por la DIAN.

    La API V2 usa códigos de las tablas de referencia de Factus:
    - identification_document_code: "13"=Cédula, "31"=NIT
    - legal_organization_code: "2"=Persona Natural, "1"=Persona Jurídica
    - tribute_code: "ZZ"=No aplica (consumidor final), "01"=IVA
    - municipality_code: código DANE del municipio (ej. "88000" para San Andrés)
    """

    identification: str = Field(..., min_length=3, max_length=50, description="Número de documento sin DV ni guiones")
    dv: int | None = Field(None, ge=0, le=9, description="Dígito de verificación (solo NIT)")
    names: str | None = Field(None, max_length=200, description="Nombres del cliente (persona natural)")
    company: str | None = Field(None, max_length=200, description="Razón social (persona jurídica)")
    trade_name: str | None = Field(None, max_length=200)
    address: str | None = Field(None, max_length=250)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=30)
    identification_document_code: str = Field("13", pattern=r"^\d{2}$", description='13=Cédula, 31=NIT...')
    legal_organization_code: str = Field("2", pattern=r"^\d$", description='1=Persona Jurídica, 2=Persona Natural')
    tribute_code: str = Field("ZZ", pattern=r"^[A-Z0-9]{2}$", description='ZZ=No aplica, 01=IVA, 04=Inc...')
    municipality_code: str | None = Field(None, pattern=r"^\d{5}$", description="Código DANE municipal")


class InvoiceCreate(BaseModel):
    customer: CustomerData
    payment_form: str = Field("1", pattern=r"^[12]$", description="1=Contado, 2=Crédito")
    payment_method_code: int = Field(10, description="10=Efectivo; ver tabla de métodos de pago Factus")
    observation: str | None = Field(None, max_length=250)
    send_email: bool = Field(True, description="Factus envía la factura al correo del cliente")


class InvoiceOut(ORMModel):
    id: int
    order_id: int
    reference_code: str
    bill_number: str | None = None
    cufe: str | None = None
    qr_url: str | None = None
    status: str
    total: Decimal
    customer_identification: str | None = None
    error_message: str | None = None
    validated_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class InvoiceSummary(ORMModel):
    """Datos mínimos de la factura para incrustarlos en las respuestas de pedidos."""

    bill_number: str | None = None
    status: str


class InvoiceApiResponse(ApiResponse[InvoiceOut]):
    data: InvoiceOut | None = None


class FactusProxyResponse(ApiResponse[dict]):
    """Respuesta genérica para proxies hacia catálogos de Factus."""
    data: dict | None = None
