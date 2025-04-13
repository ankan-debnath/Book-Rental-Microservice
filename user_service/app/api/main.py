from fastapi import FastAPI

from app.api.v1.routes import router
from app.auth.auth_routes import router as t_router

from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    NoDataToUpdateException,
    BookNotFoundException,
    BookNotAvailableException,
    UserServiceException,
    BookServiceException,
    InvalidRentalReturnException
)
from app.exceptions.handlers import (
    user_already_exists_exception_handler, user_not_fount_exception_handler,
    no_data_to_update_exception,
    book_not_found_exception_handler,
    book_not_available_for_rent_handler,
    user_service_exception_handler,
    book_service_exception_handler,
    invalid_rental_return_exception_handler
)

app = FastAPI()

app.include_router(router)
app.include_router(t_router)

app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler) # type: ignore
app.add_exception_handler(UserNotFoundException, user_not_fount_exception_handler) # type: ignore
app.add_exception_handler(NoDataToUpdateException, no_data_to_update_exception) # type: ignore
app.add_exception_handler(BookNotFoundException, book_not_found_exception_handler) # type: ignore
app.add_exception_handler(BookNotAvailableException, book_not_available_for_rent_handler) # type: ignore
app.add_exception_handler(UserServiceException, user_service_exception_handler) # type: ignore
app.add_exception_handler(InvalidRentalReturnException, invalid_rental_return_exception_handler) # type: ignore
app.add_exception_handler(BookServiceException, book_service_exception_handler) # type: ignore


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")