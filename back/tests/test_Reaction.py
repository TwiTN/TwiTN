from tests.conftest import login_client

def test_add_reaction_unauthenticated(client, test_post):
    """Tenter d'ajouter une réaction sans être connecté → 401"""
    response = client.post(f"/api/posts/{test_post['id']}/reactions/L")
    assert response.status_code == 401

def test_add_reaction_authenticated(client, test_user, test_post):
    """Ajouter une réaction en étant connecté → 201"""
    session = login_client(client, test_user)
    
    response = session.post(f"/api/posts/{test_post['id']}/reactions/L")
    assert response.status_code == 201

def test_get_reactions_aggregate(client, test_user, test_post):
    """Vérifier que le résumé (ton travail spécial) fonctionne → 200"""
    session = login_client(client, test_user)

    session.post(f"/api/posts/{test_post['id']}/reactions/L")
    
    response = client.get(f"/api/posts/{test_post['id']}/reactions")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["L"] == 1 

def test_remove_reaction(client, test_user, test_post):
    """Supprimer une réaction existante → 204"""
    session = login_client(client, test_user)
    
    session.post(f"/api/posts/{test_post['id']}/reactions/L")
    response = session.delete(f"/api/posts/{test_post['id']}/reactions/L")
    
    assert response.status_code == 204

def test_bulk_remove_reactions(client, test_user, test_post):
    """Supprimer toutes les réactions d'un type (Bulk) → 204"""
    session = login_client(client, test_user)
    
    response = session.delete(f"/api/posts/{test_post['id']}/reactions/L/bulk")
    assert response.status_code == 204