import pytest


@pytest.mark.order(1)
def test_create_post_unauthenticated(client):
    """Créer un post sans être connecté → 401"""
    response = client.post(
        "/api/posts/",
        json={
            "title": "Test post",
            "content": "Hello world",
        },
    )
    assert response.status_code == 401


@pytest.mark.order(2)
def test_create_post_authenticated(client):
    """Créer un post en étant connecté → 201"""
    # login
    client.post(
        "/api/user/login",
        json={
            "username": "test_user",
            "password": "password",
        },
    )

    response = client.post(
        "/api/posts/",
        json={
            "title": "My first post",
            "content": "This is my post",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "My first post"
    assert data["content"] == "This is my post"
    assert "author" in data


@pytest.mark.order(3)
def test_get_posts(client):
    """Lister les posts → 200"""
    response = client.get("/api/posts/")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.order(4)
def test_get_post_by_id(client):
    """Récupérer un post existant → 200"""
    posts_response = client.get("/api/posts/")
    post_id = posts_response.get_json()[0]["id"]

    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == post_id


@pytest.mark.order(5)
def test_delete_post_not_author(client):
    """Un autre utilisateur ne peut pas supprimer le post → 403"""
    posts_response = client.get("/api/posts/")
    post_id = posts_response.get_json()[0]["id"]

    # logout current user
    client.get("/api/user/logout")

    # create second user
    client.post(
        "/api/user/",
        json={
            "username": "other_user",
            "display_name": "Other",
            "email": "other@example.com",
            "password": "password",
        },
    )

    # login as second user
    client.post(
        "/api/user/login",
        json={
            "username": "other_user",
            "password": "password",
        },
    )

    response = client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 403


@pytest.mark.order(6)
def test_delete_post_author(client):
    """L’auteur peut supprimer son post → 204"""
    # logout
    client.get("/api/user/logout")

    # login as original author
    client.post(
        "/api/user/login",
        json={
            "username": "test_user",
            "password": "password",
        },
    )

    posts_response = client.get("/api/posts/")
    post_id = posts_response.get_json()[0]["id"]

    response = client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 204

    # verify post is gone
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 404
