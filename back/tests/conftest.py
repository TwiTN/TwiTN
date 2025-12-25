import pytest
from server import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def test_user2(client):
    """Créer un deuxième utilisateur de test avant chaque test"""
    username = "temp_user_post_test"
    password = "password"

    response = client.post(
        "/api/user/",
        json={
            "username": username,
            "display_name": "Temp User",
            "email": "temp_user@example.com",
            "password": password,
        },
    )
    assert response.status_code == 201

    yield {
        "username": username,
        "password": password,
    }

    response = client.post(
        "/api/user/login",
        json={
            "username": username,
            "password": password,
        },
    )

    if response.status_code == 200:
        response = client.delete("/api/user/")
        assert response.status_code == 204


@pytest.fixture(scope="function")
def test_user(client):
    """Créer un utilisateur de test avant chaque test"""

    username = "test_user_post_test"
    password = "password"

    response = client.post(
        "/api/user/",
        json={
            "username": username,
            "display_name": "Test User",
            "email": "test_user@example.com",
            "password": password,
        },
    )
    assert response.status_code == 201

    yield {
        "username": username,
        "password": password,
    }

    response = client.post(
        "/api/user/login",
        json={
            "username": username,
            "password": password,
        },
    )

    if response.status_code == 200:
        response = client.delete("/api/user/")
        assert response.status_code == 204


def login_client(client, login):
    """Helper to login a client session"""
    response = client.post(
        "/api/user/login",
        json=login,
    )
    assert response.status_code == 200
    return client


def logout_client(client):
    """Helper to logout a client session"""
    response = client.post("/api/user/logout")
    assert response.status_code == 200
    return client


@pytest.fixture(scope="function")
def test_post(client, test_user2):
    client = login_client(client, test_user2)
    response = client.post(
        "/api/posts/",
        json={
            "title": "Test post",
            "body": "Hello world",
        },
    )
    assert response.status_code == 201
    logout_client(client)
    yield response.get_json()
