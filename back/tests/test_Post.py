from tests.conftest import login_client

def test_create_post_unauthenticated_fail(client):
    """Créer un post sans être connecté → 401"""
    response = client.post(
        "/api/posts/",
        json={
            "title": "Test post",
            "body": "Hello world",
        },
    )
    assert response.status_code == 401

def test_create_post_authenticated(client, test_user):
    """Créer un post en étant connecté"""
    
    # Login
    session = login_client(client, test_user)
    
    # Create post
    response = session.post(
        "/api/posts/",
        json={
            "title": "My first post",
            "body": "This is my post",
        },
    )
    assert response.status_code == 201
    
    # Check that it matches
    data = response.get_json()
    assert data["title"] == "My first post"
    assert data["content"] == "This is my post"
    assert data["author"]["username"] == test_user["username"]


def test_get_posts(client):
    """
    Lister les derniers posts
    """
    response = client.get("/api/posts/")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_post_by_id(client):
    """Récupérer un post existant"""
    posts_response = client.get("/api/posts/")
    post_id = posts_response.get_json()[0]["id"]

    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == post_id


def test_delete_post_another_user(
    client,
    test_user,
    test_post
):
    """Un autre utilisateur ne peut pas supprimer le post → 403"""
    session = login_client(client, test_user)
    assert test_post["author"]["username"] != test_user["username"]
    
    response = session.delete(f"/api/posts/{test_post['id']}")
    assert response.status_code == 403

def test_delete_post_unauthenticated(client, test_post):
    """Un utilisateur non authentifié ne peut pas supprimer le post → 401"""
    response = client.delete(f"/api/posts/{test_post['id']}")
    assert response.status_code == 401

def test_delete_post_owner(
    client,
    test_user2,
    test_post
):
    """Le propriétaire du post peut le supprimer"""
    session = login_client(client, test_user2)
    assert test_post["author"]["username"] == test_user2["username"]
    
    response = session.delete(f"/api/posts/{test_post['id']}")
    assert response.status_code == 204