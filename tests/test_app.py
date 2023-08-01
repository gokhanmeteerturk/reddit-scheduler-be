import shutil
from fastapi import Path
from fastapi.testclient import TestClient
import sys
import os
import pytest
# Assuming your project root directory contains the main.py and settings.py files
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import settings
# Fixture to set the TESTING flag to True before running tests and reset it to False after tests
@pytest.fixture(autouse=True)
def set_testing_flag():
    settings.TESTING = True
    yield
    settings.TESTING = False


@pytest.fixture(autouse=True)
def delete_test_db_file():
    db_file_path = "db_test.sqlite3"
    if os.path.exists(db_file_path):
        os.remove(db_file_path)

# Fixture to create a TestClient for the FastAPI application
import pytest
from main import app
@pytest.fixture
def test_app():
    return TestClient(app)

# Fixture to create a mock implementation of check_key()
@pytest.fixture
def mock_check_key(monkeypatch):
    def mock_check_key(request):
        return True
    monkeypatch.setattr("main.check_key", mock_check_key)

def test_initialize(test_app):
    response = test_app.get("/init/")

    assert response.status_code in [200]
    assert "master_key" in response.json()
    assert isinstance(response.json()["master_key"], str)

def test_upload_image_invalid_image(test_app):
    filename = "invalid_file.txt"
    with open(f"tests/fixtures/{filename}", "rb") as file:
        response = test_app.post("/upload_image/", files={"file": (filename, file)})

    assert response.status_code == 415

