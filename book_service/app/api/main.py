from fastapi import FastAPI

from app.api.v1.routes import router
from app.exceptions.custom_exceptions import (
    BookNotFoundException,
    NoDataToUpdateException,
    NegativeAvailabilityException
)
from app.exceptions.handlers import (
    book_not_found_exception_handler,
    no_data_to_update_exception,
    negative_availability_exception
)

app = FastAPI()

app.include_router(router)

app.add_exception_handler(BookNotFoundException, book_not_found_exception_handler)  # type: ignore
app.add_exception_handler(NoDataToUpdateException, no_data_to_update_exception)     # type: ignore
app.add_exception_handler(NegativeAvailabilityException, negative_availability_exception)     # type: ignore

PORT = 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")