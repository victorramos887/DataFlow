import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    os.environ.setdefault("POSTGRES_USER", "test_user")
    os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
    os.environ.setdefault("POSTGRES_DB", "test_db")
    os.environ.setdefault("POSTGRES_HOST", "localhost")
    os.environ.setdefault("POSTGRES_PORT", "5432")

    from app.main import app

    return TestClient(app)