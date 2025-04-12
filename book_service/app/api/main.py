from fastapi import FastAPI

from app.api.v1.routes import router
from app.exceptions.custom_exceptions import BookNotFoundException
from app.exceptions.handlers import book_not_found_exception_handler

app = FastAPI()

app.include_router(router)

app.add_exception_handler(BookNotFoundException, book_not_found_exception_handler)  # type: ignore


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api.main:app", reload=True)