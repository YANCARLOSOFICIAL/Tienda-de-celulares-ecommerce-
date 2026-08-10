from app.core.exceptions import AppException


def validate_page(page: int, page_size: int, max_page_size: int = 100) -> None:
    """Valida parámetros de paginación."""
    if page < 1:
        raise AppException(status_code=422, message="El parámetro 'page' debe ser mayor o igual a 1")
    if page_size < 1:
        raise AppException(status_code=422, message="El parámetro 'page_size' debe ser mayor o igual a 1")
    if page_size > max_page_size:
        raise AppException(
            status_code=422,
            message=f"El parámetro 'page_size' no puede superar {max_page_size}",
        )


def compute_pages(total: int, page_size: int) -> int:
    return max(1, (total + page_size - 1) // page_size)
