import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from src.api.router import get_model
from unittest.mock import MagicMock

@pytest.fixture
def mock_model():
    model = MagicMock()
    model.encode.return_value = {"hello": 1.0, "world": 0.5}
    return model

@pytest.fixture
def client(mock_model):
    app = create_app()
    app.dependency_overrides[get_model] = lambda: mock_model
    with TestClient(app) as c:
        yield c
