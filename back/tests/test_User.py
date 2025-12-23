import pytest

@pytest.mark.order(1)
def test_get_user_by_id(
    client,
):
    # First, create a user to ensure there is one to get
    response = client.get(
        "/api/user/test_user",
    )
    assert response.status_code == 200  # User should exist yet


@pytest.mark.order(2)
def test_create_user(
    client,
):
    response = client.post(
        "/api/user/",
        json={
            "username": "new_user",
            "display_name": "New User",
            "email": "new_user@example.com",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    
    get_user_response = client.get("/api/user/new_user")
    assert get_user_response.status_code == 200
    user_data = get_user_response.get_json()
    assert user_data["username"] == "new_user"
    assert user_data["display_name"] == "New User"
    assert user_data["email"] == "new_user@example.com"
    assert "password" not in user_data  # Ensure password is not returned
    
@pytest.mark.order(3)
def test_login_user(
    client,
):
    response = client.post(
        "/api/user/login",
        json={
            "username": "new_user",
            "password": "securepassword",
        },
    )
    assert response.status_code == 200
    user_data = response.get_json()
    assert user_data["username"] == "new_user"
    assert user_data["display_name"] == "New User"
    assert user_data["email"] == "new_user@example.com"
    
    response_current_user = client.get("/api/user/")
    assert response_current_user.status_code == 200
    current_user_data = response_current_user.get_json()
    assert current_user_data["username"] == "new_user"
    assert current_user_data["display_name"] == "New User"
    assert current_user_data["email"] == "new_user@example.com"
    
    # logout
    
    logout_response = client.get("/api/user/logout")
    assert logout_response.status_code == 200
    
    # verify current user is unauthorized now
    response_current_user = client.get("/api/user/")
    assert response_current_user.status_code == 401

@pytest.mark.order(4)
def test_delete_current_user(
    client,
):
    # login first to set the session
    client.post(
        "/api/user/login",
        json={
            "username": "new_user",
            "password": "securepassword",
        },
    )
    # Now, delete the current user
    delete_response = client.delete("/api/user/")
    assert delete_response.status_code == 204

    # Verify the user has been deleted
    get_user_response = client.get("/api/user/new_user")
    assert get_user_response.status_code == 404

