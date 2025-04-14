import uuid

import pytest
import os

from app.common.db import get_session
from app.models import BookModel
from .test_db import init_test_db, get_test_db_session, drop_test_db, TestingSessionLocal

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    file_name = "test.db"  # Replace with the actual filename
    if os.path.exists(file_name):
        os.remove(file_name)

    app.dependency_overrides[get_session] = get_test_db_session

    await init_test_db()
    yield

    await drop_test_db()


@pytest.fixture(scope="function")
async def get_book():
    async with TestingSessionLocal() as session:
        book = BookModel(
            name="Test Book",
            author="Jane Doe",
            genre="Sci-Fi",
            available_copies=5
        )
        session.add(book)
        await session.commit()
        await session.refresh(book)

        yield book

        await session.delete(book)
        await session.commit()

