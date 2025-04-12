from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas.books_schema import ErrorResponse
from .custom_exceptions import BookNotFoundException

async def book_not_found_exception_handler(
        request: Request,
        exc: BookNotFoundException
) -> JSONResponse:
    response = ErrorResponse(
        success=False,
        message= exc.message,
        error_code=exc.error_code,
        data=None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )