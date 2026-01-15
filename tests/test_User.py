from tests.conftest import login_client


def test_get_user_by_id(client, test_user):
    response = client.get(f"/api/user/{test_user['username']}")
    assert response.status_code == 200


def test_get_user_by_id_not_found(client):
    response = client.get("/api/user/non_existent_user")
    assert response.status_code == 404


def test_login_user(client, test_user):
    login_client(client, test_user)

    response = client.get("/api/user/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == test_user["username"]
    assert "password" not in data


def test_login_user_fail(client, test_user):
    response = client.post(
        "/api/user/login",
        json={
            "username": test_user["username"],
            "password": "wrong_password",
        },
    )
    assert response.status_code == 401


def test_logout_user(client, test_user):
    session = login_client(client, test_user)

    response = session.get("/api/user/")
    assert response.status_code == 200

    logout_response = session.post("/api/user/logout")
    assert logout_response.status_code == 200

    me_response = session.get("/api/user/")
    assert me_response.status_code == 401


def test_delete_current_user(
    client,
    test_user,
):
    session = login_client(client, test_user)

    delete_response = session.delete("/api/user/")
    assert delete_response.status_code == 204

    get_user_response = session.get(f"/api/user/{test_user['username']}")
    assert get_user_response.status_code == 404
