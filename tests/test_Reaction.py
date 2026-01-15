from tests.conftest import login_client


def test_add_reaction_unauthenticated(client, test_post):
    response = client.post(f"/api/posts/{test_post['id']}/reactions/L")
    assert response.status_code == 401


def test_add_reaction_authenticated(client, test_user, test_post):
    session = login_client(client, test_user)
    response = session.post(f"/api/posts/{test_post['id']}/reactions/L")
    assert response.status_code == 201


def test_get_reactions_aggregate(client, test_user, test_post):
    session = login_client(client, test_user)
    session.post(f"/api/posts/{test_post['id']}/reactions/L")

    response = client.get(f"/api/posts/{test_post['id']}/reactions")
    assert response.status_code == 200
    assert response.get_json()["L"] == 1


def test_get_reactions_post_not_found(client):
    import uuid

    fake_id = uuid.uuid4()
    response = client.get(f"/api/posts/{fake_id}/reactions")
    assert response.status_code == 404


def test_remove_reaction(client, test_user, test_post):
    session = login_client(client, test_user)
    session.post(f"/api/posts/{test_post['id']}/reactions/L")
    response = session.delete(f"/api/posts/{test_post['id']}/reactions/L")
    assert response.status_code == 204


def test_bulk_remove_reactions(client, test_user2, test_post):
    session = login_client(client, test_user2)
    response = session.delete(f"/api/posts/{test_post['id']}/reactions/bulk")
    assert response.status_code == 204
