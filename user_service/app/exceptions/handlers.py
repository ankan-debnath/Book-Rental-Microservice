
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    NoDataToUpdateException,
    BookNotFoundException, BookNotAvailableException, BookServiceException, UserServiceException
)
from app.schemas.user import  ErrorResponse


async def user_already_exists_exception_handler(
        request: Request,
        exc: UserAlreadyExistsException
) -> JSONResponse:
    response = ErrorResponse(
        success=False,
        error_code=exc.error_code,
        message=exc.message,
        data=None
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=response.model_dump()
    )


async def user_not_fount_exception_handler(
        request: Request,
        exc: UserNotFoundException
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

async def book_not_available_for_rent_handler(
        request: Request,
        exc: BookNotAvailableException
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


async def book_service_exception_handler(
        request: Request,
        exc: BookServiceException
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


async def user_service_exception_handler(
        request: Request,
        exc: UserServiceException
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



async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    print(exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred.",
            "data": {},
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )
