from http.client import responses

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.custom_exceptions import UserAlreadyExistsException, UserNotFoundException
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


async def generic_exception_handler(request: Request, exc: Exception):
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
