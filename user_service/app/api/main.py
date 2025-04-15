from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(title="Book Rental Microservice")

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing (change in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


PORT = 5000

@app.get("/")
def index():
    return JSONResponse(
        status_code=200,
        content=f"Server is running at port {PORT}"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")