from fastapi import FastAPI

from app.api.v1.routes import router
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    NoDataToUpdateException
)
from app.exceptions.handlers import (
    user_already_exists_exception_handler, user_not_fount_exception_handler,
    no_data_to_update_exception
)

app = FastAPI()

app.include_router(router)

app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler) # type: ignore
app.add_exception_handler(UserNotFoundException, user_not_fount_exception_handler) # type: ignore
app.add_exception_handler(NoDataToUpdateException, no_data_to_update_exception) # type: ignore

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api.main:app", reload=True)