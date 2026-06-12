import pytest
from app import create_app, db as _db

TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
}

@pytest.fixture
def app():
    app = create_app(test_config=TEST_CONFIG)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    r = client.get("/items/health")
    assert r.status_code == 200

def test_get_empty(client):
    r = client.get("/items/")
    assert r.status_code == 200
    assert r.get_json() == []

def test_create_item(client):
    r = client.post("/items/", json={"name": "Laptop", "quantity": 5})
    assert r.status_code == 201
    data = r.get_json()
    assert data["name"] == "Laptop"
    assert data["quantity"] == 5

def test_create_missing_name(client):
    r = client.post("/items/", json={"quantity": 1})
    assert r.status_code == 400

def test_get_item(client):
    client.post("/items/", json={"name": "Mouse"})
    r = client.get("/items/1")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Mouse"

def test_update_item(client):
    client.post("/items/", json={"name": "Keyboard", "quantity": 10})
    r = client.put("/items/1", json={"quantity": 20})
    assert r.status_code == 200
    assert r.get_json()["quantity"] == 20

def test_delete_item(client):
    client.post("/items/", json={"name": "Monitor"})
    r = client.delete("/items/1")
    assert r.status_code == 200
    r = client.get("/items/1")
    assert r.status_code == 404
