from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas.books_schema import ErrorResponse
from .custom_exceptions import BookNotFoundException, NoDataToUpdateException

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

async def no_data_to_update_exception(
        request: Request,
        exc: NoDataToUpdateException
) -> JSONResponse:
    response = ErrorResponse(
        success=False,
        error_code=exc.error_code,
        message=exc.message,
        data=None
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )

