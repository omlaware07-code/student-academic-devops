import pytest
from app import create_app
from database.db import db

@pytest.fixture
def client():
    db.reset()
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    db.reset()
