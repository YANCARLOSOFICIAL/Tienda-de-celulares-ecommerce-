from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.core.dependencies import AdminUser, CurrentUser, DbDep
from app.schemas.common import ApiResponse
from app.schemas.invoice import InvoiceApiResponse, InvoiceCreate, InvoiceOut
from app.services import factus, invoices as invoice_service

router = APIRouter(prefix="/invoices", tags=["Facturación electrónica"])


@router.get("/numbering-ranges", response_model=ApiResponse[dict], summary="Rangos de numeración (Factus)")
def get_numbering_ranges(_admin: AdminUser, page: int = 1) -> ApiResponse[dict]:
    data = factus.numbering_ranges(page=page)
    return ApiResponse(success=True, message="Rangos de numeración obtenidos", data=data)


@router.post("/orders/{order_id}", response_model=InvoiceApiResponse, status_code=201,
             summary="Emitir factura electrónica para un pedido (admin)")
def create_invoice(order_id: int, payload: InvoiceCreate, db: DbDep, admin: AdminUser) -> InvoiceApiResponse:
    invoice = invoice_service.create_invoice_for_order(db, admin, order_id, payload)
    return InvoiceApiResponse(
        success=True,
        message="Factura electrónica generada y validada correctamente",
        data=InvoiceOut.model_validate(invoice),
    )


@router.get("/orders/{order_id}", response_model=InvoiceApiResponse,
            summary="Consultar la factura electrónica de un pedido")
def get_invoice(order_id: int, db: DbDep, current_user: CurrentUser) -> InvoiceApiResponse:
    invoice = invoice_service.get_invoice_for_order(db, current_user, order_id)
    return InvoiceApiResponse(
        success=True,
        message="Factura obtenida correctamente",
        data=InvoiceOut.model_validate(invoice),
    )


@router.delete("/orders/{order_id}", response_model=ApiResponse[None],
               summary="Eliminar una factura NO validada por la DIAN")
def delete_invoice(order_id: int, db: DbDep, current_user: CurrentUser) -> ApiResponse[None]:
    invoice_service.delete_invoice(db, current_user, order_id)
    return ApiResponse(success=True, message="Factura eliminada correctamente")


@router.get("/{bill_number}/pdf", summary="Descargar PDF de la factura")
def download_pdf(bill_number: str, db: DbDep, current_user: CurrentUser) -> Response:
    invoice_service.get_invoice_for_download(db, current_user, bill_number)
    file_name, content = factus.download_pdf(bill_number)
    return StreamingResponse(
        BytesIO(content),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


@router.get("/{bill_number}/xml", summary="Descargar XML UBL de la factura")
def download_xml(bill_number: str, db: DbDep, current_user: CurrentUser) -> Response:
    invoice_service.get_invoice_for_download(db, current_user, bill_number)
    file_name, content = factus.download_xml(bill_number)
    return StreamingResponse(
        BytesIO(content),
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )
