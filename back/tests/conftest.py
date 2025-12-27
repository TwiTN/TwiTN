import pytest
from server import create_app
from db.api.Reaction import clear_reactions_for_post
from db import db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def test_user2(app, client):
    with app.app_context():
        db.session.rollback()

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
        json={"username": username, "password": password},
    )
    if response.status_code == 200:
        client.delete("/api/user/")
        with app.app_context():
            db.session.commit()


@pytest.fixture(scope="function")
def test_user(app, client):
    with app.app_context():
        db.session.rollback()

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
        json={"username": username, "password": password},
    )
    if response.status_code == 200:
        client.delete("/api/user/")
        with app.app_context():
            db.session.commit()


def login_client(client, login):
    response = client.post("/api/user/login", json=login)
    assert response.status_code == 200
    return client


def logout_client(client):
    response = client.post("/api/user/logout")
    assert response.status_code == 200
    return client


@pytest.fixture(scope="function")
def test_post(app, client, test_user2):
    client = login_client(client, test_user2)

    response = client.post(
        "/api/posts/",
        json={
            "title": "Test post for reactions",
            "body": "Hello world, this is a test post.",
        },
    )
    assert response.status_code == 201
    post_data = response.get_json()
    logout_client(client)

    yield post_data

    with app.app_context():
        clear_reactions_for_post(post_data["id"])
        db.session.commit()
