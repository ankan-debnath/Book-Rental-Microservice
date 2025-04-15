import uuid

import pytest
import os

from app.auth.password import get_password_hash
from app.common.db import get_session
from .test_db import init_test_db, get_test_db_session, drop_test_db, TestingSessionLocal

from fastapi.testclient import TestClient

from app.api.main import app
from app.api.main import PORT

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    file_name = "test.db"  # Replace with the actual filename
    if os.path.exists(file_name):
        os.remove(file_name)

    app.dependency_overrides[get_session] = get_test_db_session

    await init_test_db()
    yield

    await drop_test_db()



@pytest.fixture(scope="session", autouse=True)
async def get_book_id():

    book_id = str(uuid.uuid4())
    yield book_id
