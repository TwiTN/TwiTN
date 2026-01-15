from tests.conftest import login_client


def test_create_post_unauthenticated_fail(client):
    response = client.post(
        "/api/posts/",
        json={
            "title": "Test post",
            "body": "Hello world",
        },
    )
    assert response.status_code == 401


def test_create_post_authenticated(client, test_user):
    session = login_client(client, test_user)

    response = session.post(
        "/api/posts/",
        json={
            "title": "My first post",
            "body": "This is my post",
        },
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == "My first post"
    assert data["content"] == "This is my post"
    assert data["author"]["username"] == test_user["username"]


def test_get_posts(client):
    response = client.get("/api/posts/")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_post_by_id(client):
    posts_response = client.get("/api/posts/")
    post_id = posts_response.get_json()[0]["id"]

    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == post_id


def test_delete_post_another_user(client, test_user, test_post):
    session = login_client(client, test_user)
    assert test_post["author"]["username"] != test_user["username"]

    response = session.delete(f"/api/posts/{test_post['id']}")
    assert response.status_code == 403


def test_delete_post_unauthenticated(client, test_post):
    response = client.delete(f"/api/posts/{test_post['id']}")
    assert response.status_code == 401


def test_delete_post_owner(client, test_user2, test_post):
    session = login_client(client, test_user2)
    assert test_post["author"]["username"] == test_user2["username"]

    response = session.delete(f"/api/posts/{test_post['id']}")
    assert response.status_code == 204
