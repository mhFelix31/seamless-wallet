import pytest


def test_login_returns_200_for_valid_credentials(default_client, user_factory):
    test_password = "test"
    user = user_factory(password=test_password)
    payload = {"username": user.email, "password": test_password}

    response = default_client.post("/login/", data=payload)

    assert response.status_code == 200


def test_login_returns_bearer_token(default_client, user_factory):
    test_password = "test"
    user = user_factory(password=test_password)
    payload = {"username": user.email, "password": test_password}

    response = default_client.post("/login/", data=payload)

    assert "bearer" in response.json()


@pytest.mark.parametrize(
    "payload",
    [
        {"username": "user@example.com", "password": "wrong-password"},
        {"username": "invalid@example.com", "password": "valid-password"},
        {"username": "invalid@example.com", "password": "wrong-password"},
    ],
)
def test_login_returns_401_for_invalid_credentials(
    default_client, payload, user_factory
):
    user_factory(email="user@example.com", password="valid-password")
    invalid_payload = payload

    response = default_client.post("/login/", data=invalid_payload)

    assert response.status_code == 401


def test_login_returns_invalid_credentials_message(default_client):
    payload = {"username": "user@example.com", "password": "wrong-password"}

    response = default_client.post("/login/", data=payload)

    assert response.json()["detail"] == "Invalid Credentials"